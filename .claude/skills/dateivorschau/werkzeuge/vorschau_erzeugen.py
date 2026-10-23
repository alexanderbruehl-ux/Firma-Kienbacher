"""Baut aus beliebigen Dateien (oder ganzen Projektordnern) eine
eigenstaendige HTML-Vorschau mit Ordnerbaum-Navigation, vollstaendiger
Lese-Ansicht je Datei und Download-Button.

    python vorschau_erzeugen.py datei1.pptx datei2.png ... --out vorschau.html
    python vorschau_erzeugen.py notes working source --out vorschau.html --titel "Dateien fuer Projekt: ..."

Argumente koennen einzelne Dateien oder Ordner sein. Ein Ordner wird
rekursiv nach fuer Menschen relevanten Dateien durchsucht (PPTX/DOCX/XLSX/
PDF/Bilder) - Quellcode, Skripte, `node_modules`, `.git` und Aehnliches
werden uebersprungen, damit das Projekt vollstaendig abgebildet wird statt
nur der gerade frisch gelieferten Dateien.

Kein Renderversuch ueber eine externe Office-Suite (LibreOffice haengt sich
in vielen Sandbox-Umgebungen ohne Fehlermeldung auf, auch bei trivialen
Dateien - und ein eingebettetes docProps/thumbnail.jpeg ist meist nur ein
leerer Platzhalter, kein echtes Abbild). Stattdessen:

- Bilder und PDFs werden inline angezeigt, weil Browser das nativ koennen.
- PPTX: jede Folie wird aus den tatsaechlichen Shapes (Position, Farbe, Text)
  nachgebaut und untereinander scrollbar dargestellt - echte Werte aus der
  Datei, kein Rendering-Dienst noetig.
- DOCX: der komplette Dokumentkoerper (Absaetze, Ueberschriften, Tabellen) in
  Original-Reihenfolge, scrollbar, reine Lese-Ansicht.
- Alles andere (XLSX, ZIP, ...) bekommt eine Karte mit Dateityp und Groesse.
- Bei mehreren Dateien: Ordnerbaum links (bzw. Auswahlliste auf schmalen
  Bildschirmen) zum Umschalten zwischen den Dateien.

Bearbeiten und Drucken passieren im jeweiligen Originalprogramm, nicht im
Browser - die Vorschau ist eine vollstaendige Lese-Ansicht, kein Editor.

Funktioniert nur als eigenstaendige Datei (lokal geoeffnet oder per Datei
weitergegeben) - in einer eingebetteten/sandboxed Ansicht (z. B. ein
Artifact-Link) sind von der Seite selbst ausgeloeste Downloads blockiert.

Benoetigt `python-pptx` fuer PPTX- und `python-docx` fuer DOCX-Vorschauen;
fehlen sie, faellt die Karte automatisch auf den reinen Dateityp-Hinweis
zurueck.
"""
from __future__ import annotations

import argparse
import base64
import mimetypes
import os
from pathlib import Path

try:
    from pptx import Presentation
    from pptx.enum.shapes import MSO_SHAPE_TYPE
    _PPTX_VERFUEGBAR = True
except ImportError:
    _PPTX_VERFUEGBAR = False

try:
    import docx as docx_lib
    from docx.oxml.ns import qn
    from docx.table import Table as DocxTable
    from docx.text.paragraph import Paragraph as DocxParagraph
    _DOCX_VERFUEGBAR = True
except ImportError:
    _DOCX_VERFUEGBAR = False

BILD_TYPEN = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}
PDF_TYPEN = {".pdf"}
DOKUMENT_TYPEN = {".pptx", ".ppt", ".docx", ".doc", ".xlsx", ".xls"}
RELEVANTE_ENDUNGEN = BILD_TYPEN | PDF_TYPEN | DOKUMENT_TYPEN
AUSSCHLUSS_ORDNER = {".git", "node_modules", "__pycache__", ".claude", ".venv", "venv"}
EMU_PER_PT = 12700
DOCX_ZEICHEN_LIMIT = 200_000

TYP_LABEL = {
    ".pptx": "PowerPoint", ".ppt": "PowerPoint",
    ".docx": "Word", ".doc": "Word",
    ".xlsx": "Excel", ".xls": "Excel",
    ".pdf": "PDF", ".zip": "ZIP-Archiv",
    ".png": "Bild (PNG)", ".jpg": "Bild (JPEG)", ".jpeg": "Bild (JPEG)",
    ".gif": "Bild (GIF)", ".webp": "Bild (WebP)", ".svg": "Vektorgrafik (SVG)",
    ".json": "JSON", ".md": "Markdown", ".txt": "Text",
}


def esc(t: str) -> str:
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def sammle_relevante_dateien(pfade: list[Path]) -> list[Path]:
    """Loest Ordner-Argumente rekursiv in relevante Dateien auf (Einzeldateien
    bleiben unveraendert), dedupliziert und ueberspringt Code-/Systemordner."""
    gesammelt: list[Path] = []
    gesehen: set[Path] = set()

    def hinzufuegen(datei: Path) -> None:
        resolved = datei.resolve()
        if resolved not in gesehen:
            gesehen.add(resolved)
            gesammelt.append(datei)

    for pfad in pfade:
        if pfad.is_dir():
            for datei in sorted(pfad.rglob("*")):
                if not datei.is_file():
                    continue
                if any(teil in AUSSCHLUSS_ORDNER for teil in datei.parts):
                    continue
                if datei.suffix.lower() in RELEVANTE_ENDUNGEN:
                    hinzufuegen(datei)
        else:
            hinzufuegen(pfad)
    return gesammelt


def _shape_rgb(fill_or_line) -> str | None:
    try:
        return str(fill_or_line.fore_color.rgb) if fill_or_line.type is not None else None
    except Exception:
        return None


def _slide_html(slide, sb_w: int, sb_h: int, breite_pt: float) -> str:
    def pct(v, ganz):
        return round((v or 0) / ganz * 100, 3)

    teile = []
    for shp in slide.shapes:
        links, oben = pct(shp.left, sb_w), pct(shp.top, sb_h)
        breite, hoehe = pct(shp.width, sb_w), pct(shp.height, sb_h)
        basis = f"left:{links}%;top:{oben}%;width:{breite}%;height:{hoehe}%;position:absolute;"

        if shp.shape_type == MSO_SHAPE_TYPE.PICTURE:
            try:
                bild = shp.image
                b64 = base64.b64encode(bild.blob).decode()
                teile.append(f'<img style="{basis}object-fit:contain;" '
                            f'src="data:{bild.content_type};base64,{b64}" alt="" />')
            except Exception:
                pass
            continue

        if shp.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE:
            try:
                fuellung = _shape_rgb(shp.fill)
            except Exception:
                fuellung = None
            if fuellung:
                teile.append(f'<div style="{basis}background:#{fuellung};"></div>')

        if getattr(shp, "has_text_frame", False) and shp.text_frame.text.strip():
            zeilen = []
            for para in shp.text_frame.paragraphs:
                stueck = []
                for run in para.runs:
                    if not run.text:
                        continue
                    grad_pt = run.font.size.pt if run.font.size else 12
                    grad_cqw = round(grad_pt / breite_pt * 100, 3)
                    fett = "700" if run.font.bold else "400"
                    farbe = _shape_rgb(run.font.color) if run.font.color else None
                    stil = f"font-size:{grad_cqw}cqw;font-weight:{fett};"
                    stil += f"color:#{farbe};" if farbe else ""
                    stueck.append(f'<span style="{stil}">{esc(run.text)}</span>')
                if stueck:
                    zeilen.append("<p style=\"margin:0;line-height:1.2;\">" + "".join(stueck) + "</p>")
            if zeilen:
                teile.append(f'<div style="{basis}overflow:hidden;">{"".join(zeilen)}</div>')

    return "".join(teile)


def pptx_vorschau_html(pfad: Path) -> str | None:
    """Baut jede Folie aus den echten Shapes nach - Position, Farbe und Text
    kommen direkt aus der Datei, kein Rendering-Dienst noetig. Alle Folien
    werden untereinander scrollbar dargestellt."""
    if not _PPTX_VERFUEGBAR:
        return None
    try:
        prs = Presentation(str(pfad))
        if not prs.slides:
            return None
        sb_w, sb_h = prs.slide_width, prs.slide_height
        if not sb_w or not sb_h:
            return None
        breite_pt = sb_w / EMU_PER_PT
        aspekt = round(sb_w / sb_h, 4)
    except Exception:
        return None

    folien = []
    for i, slide in enumerate(prs.slides, start=1):
        try:
            inhalt = _slide_html(slide, sb_w, sb_h, breite_pt)
        except Exception:
            inhalt = ""
        folien.append(
            f'<div class="pptx-folie-nr">Folie {i}</div>'
            f'<div class="pptx-slide" style="aspect-ratio:{aspekt};" '
            f'container-type="inline-size">{inhalt}</div>'
        )
    if not folien:
        return None
    return f'<div class="preview pptx-preview" style="container-type:inline-size;">{"".join(folien)}</div>'


def _docx_block_items(dok):
    body = dok.element.body
    for child in body.iterchildren():
        if child.tag == qn("w:p"):
            yield DocxParagraph(child, dok)
        elif child.tag == qn("w:tbl"):
            yield DocxTable(child, dok)


def _ist_listenpunkt(para: "DocxParagraph") -> bool:
    """Erkennt Aufzaehlungs-/Nummerierungs-Absaetze: massgeblich ist das
    tatsaechliche OOXML-Element <w:numPr> (direkt oder ueber die
    Absatzvorlage gesetzt) - funktioniert unabhaengig vom Namen der
    verwendeten Absatzformatvorlage (z. B. auch bei Word-Dokumenten, die
    Listen ohne die Vorlage "List Paragraph" formatieren). Der Vorlagen-
    name ("List ..." ) dient nur als Rueckfallebene."""
    try:
        pPr = para._p.find(qn("w:pPr"))
        if pPr is not None and pPr.find(qn("w:numPr")) is not None:
            return True
        if para.style is not None:
            style = para.style
            gesehen = set()
            while style is not None and id(style) not in gesehen:
                gesehen.add(id(style))
                style_pPr = style.element.find(qn("w:pPr"))
                if style_pPr is not None and style_pPr.find(qn("w:numPr")) is not None:
                    return True
                style = getattr(style, "base_style", None)
    except Exception:
        pass
    if para.style is not None and para.style.name and "List" in para.style.name:
        return True
    return False


def docx_vorschau_html(pfad: Path) -> str | None:
    """Der komplette Dokumentkoerper (Absaetze, Ueberschriften, Listen,
    Tabellen) in Original-Reihenfolge - vollstaendige Lese-Ansicht, keine
    Kuerzung (ausser bei sehr langen Dokumenten, als Schutz vor unhandlichen
    Dateigroessen). Aufzaehlungs-/Nummerierungs-Absaetze werden zu echten
    <ul>-Bloecken gruppiert statt als flache <p>-Absaetze zu erscheinen -
    sonst geht bei listenlastigen Dokumenten (z. B. Rollenbeschreibungen)
    die komplette sichtbare Struktur verloren."""
    if not _DOCX_VERFUEGBAR:
        return None
    try:
        dok = docx_lib.Document(str(pfad))
    except Exception:
        return None

    bloecke = []
    zeichen = 0
    gekuerzt = False
    liste_offen = False

    def liste_schliessen():
        nonlocal liste_offen
        if liste_offen:
            bloecke.append("</ul>")
            liste_offen = False

    for item in _docx_block_items(dok):
        if zeichen > DOCX_ZEICHEN_LIMIT:
            gekuerzt = True
            break
        if isinstance(item, DocxParagraph):
            text = item.text.strip()
            if not text:
                continue
            ist_ueberschrift = item.style is not None and "Heading" in (item.style.name or "")
            if not ist_ueberschrift and _ist_listenpunkt(item):
                if not liste_offen:
                    bloecke.append("<ul>")
                    liste_offen = True
                bloecke.append(f"<li>{esc(text)}</li>")
            else:
                liste_schliessen()
                tag = "h3" if ist_ueberschrift else "p"
                bloecke.append(f"<{tag}>{esc(text)}</{tag}>")
            zeichen += len(text)
        else:
            liste_schliessen()
            zeilen = []
            for zeile in item.rows:
                zellen = "".join(f'<td>{esc(z.text.strip())}</td>' for z in zeile.cells)
                zeilen.append(f'<tr>{zellen}</tr>')
                zeichen += sum(len(z.text) for z in zeile.cells)
            if zeilen:
                bloecke.append(f'<table>{"".join(zeilen)}</table>')
    liste_schliessen()
    if not bloecke:
        return None
    if gekuerzt:
        bloecke.append('<p class="fade-hint">&hellip; Dokument sehr lang, hier gekuerzt - '
                       'fuer den vollstaendigen Inhalt Original herunterladen.</p>')
    return f'<div class="docx-page">{"".join(bloecke)}</div>'


def groesse_lesbar(bytes_zahl: int) -> str:
    wert = float(bytes_zahl)
    for einheit in ("B", "KB", "MB", "GB"):
        if wert < 1024 or einheit == "GB":
            return f"{wert:.0f} {einheit}" if einheit == "B" else f"{wert:.1f} {einheit}"
        wert /= 1024
    return f"{wert:.1f} GB"


def rel_anzeige(pfad: Path) -> str:
    """Pfad relativ zum aktuellen Arbeitsverzeichnis, fuer die
    Ordnerbaum-Gruppierung. Liegt die Datei ausserhalb (z. B. /tmp), wird
    nur der Dateiname verwendet - kein Baum mit '..'-Eintraegen."""
    try:
        rel = os.path.relpath(pfad, Path.cwd())
    except ValueError:
        return pfad.name
    if rel.startswith(".."):
        return pfad.name
    return rel.replace(os.sep, "/")


def datei_panel(index: int, pfad: Path, aktiv: bool) -> tuple[str, str]:
    """Baut das Panel (Viewer-Ansicht) einer Datei. Gibt (anzeigename,
    panel_html) zurueck."""
    ext = pfad.suffix.lower()
    daten = pfad.read_bytes()
    b64 = base64.b64encode(daten).decode()
    mime = mimetypes.guess_type(pfad.name)[0] or "application/octet-stream"
    typ_label = TYP_LABEL.get(ext, ext.lstrip(".").upper() or "Datei")
    groesse = groesse_lesbar(len(daten))
    data_url = f"data:{mime};base64,{b64}"
    anzeigename = rel_anzeige(pfad)

    vorschau = None
    if ext in BILD_TYPEN:
        vorschau = f'<div class="preview img-preview"><img src="{data_url}" alt="{esc(pfad.name)}" /></div>'
    elif ext in PDF_TYPEN:
        vorschau = f'<div class="preview pdf-preview"><embed src="{data_url}" type="application/pdf" /></div>'
    elif ext == ".pptx":
        vorschau = pptx_vorschau_html(pfad)
    elif ext == ".docx":
        inhalt = docx_vorschau_html(pfad)
        if inhalt:
            vorschau = f'<div class="preview docx-preview">{inhalt}</div>'

    if vorschau is None:
        vorschau = f'<div class="preview no-preview"><span class="file-badge">{esc(typ_label)}</span></div>'

    aktiv_klasse = " active" if aktiv else ""
    panel = f'''
<section class="file-panel{aktiv_klasse}" id="panel-{index}">
  <div class="panel-header">
    <h2>{esc(pfad.name)}</h2>
    <p class="sub">{esc(typ_label)} &middot; {groesse}</p>
    <a class="btn" href="{data_url}" download="{esc(pfad.name)}">Herunterladen</a>
  </div>
  {vorschau}
</section>'''
    return anzeigename, panel


def _baum_einfuegen(baum: dict, teile: list[str], index: int) -> None:
    if len(teile) == 1:
        baum.setdefault("__dateien__", []).append((teile[0], index))
        return
    unterordner = baum.setdefault("__ordner__", {}).setdefault(teile[0], {})
    _baum_einfuegen(unterordner, teile[1:], index)


def _baum_rendern(baum: dict) -> str:
    teile = []
    for name, unterbaum in sorted(baum.get("__ordner__", {}).items()):
        teile.append(f'<li class="folder"><span class="folder-label">{esc(name)}</span>'
                     f'<ul>{_baum_rendern(unterbaum)}</ul></li>')
    for name, index in sorted(baum.get("__dateien__", []), key=lambda t: t[0].lower()):
        teile.append(f'<li><button type="button" class="tree-file" data-target="panel-{index}">'
                     f'{esc(name)}</button></li>')
    return "".join(teile)


def ableiten_name(titel: str) -> str:
    """Kurzer Artifact-Name (Browser-Tab/Galerie) aus der Seitenueberschrift
    ableiten: das generische Praefix "Dateien fuer Projekt: " abschneiden,
    denn der Artifact-Name soll der Projektname selbst sein, kein Label plus
    Doppelpunkt plus Erklaerung."""
    praefix = "Dateien für Projekt: "
    if titel.startswith(praefix):
        return titel[len(praefix):].strip()
    return titel


def bauen(pfade: list[Path], titel: str, artifact_name: str | None = None) -> str:
    panels = []
    namen = []
    for i, p in enumerate(pfade):
        name, panel = datei_panel(i, p, aktiv=(i == 0))
        namen.append(name)
        panels.append(panel)

    if len(pfade) <= 1:
        navigation = ""
        klasse_browser = "browser single"
    else:
        baum = {}
        for i, name in enumerate(namen):
            _baum_einfuegen(baum, name.split("/"), i)
        baum_html = _baum_rendern(baum)

        optionen = "".join(
            f'<option value="panel-{i}"{" selected" if i == 0 else ""}>{esc(name)}</option>'
            for i, name in enumerate(namen)
        )
        navigation = f'''
    <select id="dateiauswahl" class="mobile-nav" aria-label="Datei auswaehlen">{optionen}</select>
    <nav class="tree"><ul>{baum_html}</ul></nav>'''
        klasse_browser = "browser"

    script = ""
    if len(pfade) > 1:
        script = '''
<script>
  function zeigeDatei(id) {
    document.querySelectorAll('.file-panel').forEach(function (p) { p.classList.toggle('active', p.id === id); });
    document.querySelectorAll('.tree-file').forEach(function (b) { b.classList.toggle('active', b.dataset.target === id); });
    var auswahl = document.getElementById('dateiauswahl');
    if (auswahl) { auswahl.value = id; }
  }
  document.querySelectorAll('.tree-file').forEach(function (btn) {
    btn.addEventListener('click', function () { zeigeDatei(btn.dataset.target); });
  });
  var auswahl = document.getElementById('dateiauswahl');
  if (auswahl) { auswahl.addEventListener('change', function (e) { zeigeDatei(e.target.value); }); }
  var ersterTreeFile = document.querySelector('.tree-file');
  if (ersterTreeFile) { ersterTreeFile.classList.add('active'); }
</script>'''

    return TEMPLATE.format(
        titel=esc(titel),
        name=esc(artifact_name or ableiten_name(titel)),
        klasse_browser=klasse_browser,
        navigation=navigation,
        panels="\n".join(panels),
        script=script,
    )


TEMPLATE = '''<meta charset="utf-8">
<title>{name}</title>
<meta name="description" content="Vollstaendige Lese-Ansicht, zum Herunterladen fuer Original-Bearbeitung im jeweiligen Programm." />
<style>
  :root {{ --bg:#EFEEEA; --panel:#FFFFFF; --ink:#1B1F22; --muted:#6B6F73; --accent:#0079A7; --accent-ink:#00435C; --line:#D8DBDD; }}
  @media (prefers-color-scheme: dark) {{
    :root:not([data-theme="light"]) {{ --bg:#14171A; --panel:#1D2124; --ink:#EDEFF1; --muted:#9BA0A5; --accent:#4DB8E0; --accent-ink:#7FD1EE; --line:#33383C; }}
  }}
  :root[data-theme="dark"] {{ --bg:#14171A; --panel:#1D2124; --ink:#EDEFF1; --muted:#9BA0A5; --accent:#4DB8E0; --accent-ink:#7FD1EE; --line:#33383C; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; padding-inline:16px; padding-block:24px; background:var(--bg); color:var(--ink); font-family:Arial, Helvetica, sans-serif; }}
  .wrap {{ max-width:1180px; margin:0 auto; }}
  h1 {{ font-size:clamp(20px,4vw,28px); color:var(--accent-ink); margin:0 0 6px; text-wrap:balance; }}
  .sub-page {{ color:var(--muted); font-size:14px; margin:0 0 20px; max-width:70ch; }}
  .browser {{ display:grid; grid-template-columns:240px 1fr; gap:18px; align-items:start; }}
  .browser.single {{ grid-template-columns:1fr; }}
  .mobile-nav {{ display:none; width:100%; padding:10px 12px; border-radius:8px; border:1px solid var(--line); background:var(--panel); color:var(--ink); font-size:14px; margin-bottom:12px; }}
  .tree {{ background:var(--panel); border:1px solid var(--line); border-radius:10px; padding:10px 6px; max-height:75vh; overflow:auto; }}
  .tree ul {{ list-style:none; margin:0; padding-left:14px; }}
  .tree > ul {{ padding-left:4px; }}
  .tree li {{ margin:2px 0; }}
  .folder-label {{ display:block; padding:6px 8px; font-size:13px; font-weight:700; color:var(--muted); }}
  .tree-file {{ display:block; width:100%; text-align:left; background:none; border:none; padding:7px 8px; border-radius:6px; font-size:13px; color:var(--ink); cursor:pointer; word-break:break-word; }}
  .tree-file:hover {{ background:var(--bg); }}
  .tree-file.active {{ background:var(--accent); color:#FFFFFF; }}
  .viewer {{ min-width:0; }}
  .file-panel {{ display:none; background:var(--panel); border:1px solid var(--line); border-radius:10px; overflow:hidden; }}
  .file-panel.active {{ display:block; }}
  .panel-header {{ padding:16px 18px 14px; border-bottom:1px solid var(--line); display:flex; flex-wrap:wrap; align-items:baseline; gap:4px 14px; }}
  .panel-header h2 {{ font-size:16px; margin:0; word-break:break-word; color:var(--ink); flex:1 1 auto; }}
  .panel-header .sub {{ font-size:12px; color:var(--muted); margin:0; }}
  .btn {{ padding:8px 14px; border-radius:6px; background:var(--accent); color:#FFFFFF; font-weight:700; font-size:13px; text-decoration:none; white-space:nowrap; }}
  .preview {{ background:var(--bg); }}
  .img-preview {{ padding:14px; text-align:center; }}
  .img-preview img {{ max-width:100%; max-height:75vh; object-fit:contain; }}
  .pdf-preview embed {{ width:100%; height:75vh; display:block; }}
  .no-preview {{ padding:28px; text-align:center; }}
  .pptx-preview {{ padding:14px; max-height:75vh; overflow:auto; display:flex; flex-direction:column; gap:10px; }}
  .pptx-folie-nr {{ font-size:12px; color:var(--muted); font-weight:700; }}
  .pptx-slide {{ position:relative; width:100%; background:#FFFFFF; border:1px solid var(--line); border-radius:4px; overflow:hidden; color:#1B1F22; font-family:Arial, Helvetica, sans-serif; flex:none; }}
  .docx-preview {{ padding:16px; max-height:75vh; overflow:auto; }}
  .docx-page {{
    width:100%; background:#FFFFFF; border:1px solid var(--line); border-radius:4px;
    padding:20px 24px; font-family:Georgia, 'Times New Roman', serif; color:#1B1F22;
  }}
  .docx-page h3 {{ font-size:16px; margin:18px 0 8px; }}
  .docx-page h3:first-child {{ margin-top:0; }}
  .docx-page p {{ font-size:14px; line-height:1.55; margin:0 0 10px; color:#2A2D30; }}
  .docx-page ul {{ margin:0 0 12px; padding-left:22px; }}
  .docx-page li {{ font-size:14px; line-height:1.55; margin:0 0 5px; color:#2A2D30; }}
  .docx-page table {{ border-collapse:collapse; width:100%; margin:0 0 14px; font-size:13px; }}
  .docx-page td {{ border:1px solid #C7CACD; padding:5px 8px; vertical-align:top; }}
  .docx-page .fade-hint {{ color:var(--muted); font-style:italic; }}
  .file-badge {{ display:inline-block; padding:6px 12px; border-radius:6px; background:var(--accent); color:#FFFFFF; font-size:12px; font-weight:700; letter-spacing:.02em; }}
  footer {{ margin-top:28px; padding-top:14px; border-top:1px solid var(--line); font-size:12px; color:var(--muted); }}
  @media (max-width: 680px) {{
    .browser {{ grid-template-columns:1fr; }}
    .tree {{ display:none; }}
    .mobile-nav {{ display:block; }}
  }}
</style>
<div class="wrap">
  <header>
    <h1>{titel}</h1>
    <p class="sub-page">Vollstaendige Lese-Ansicht zum Durchscrollen. Bearbeiten und Drucken passiert im jeweiligen Originalprogramm - dafuer die Datei ueber den Button herunterladen.</p>
  </header>
  <div class="{klasse_browser}">
    {navigation}
    <div class="viewer">{panels}</div>
  </div>
  <footer>Kienbacher &middot; Datei-Vorschau</footer>
</div>
{script}
'''


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dateien", type=Path, nargs="+",
                        help="Dateien und/oder Ordner (Ordner werden rekursiv nach relevanten Dateien durchsucht)")
    parser.add_argument("--out", type=Path, default=Path("vorschau.html"))
    parser.add_argument("--titel", default="Dateien",
                        help='Seitenueberschrift (H1), z. B. "Dateien für Projekt: <Projektname>"')
    parser.add_argument("--name", default=None,
                        help="Kurzer Artifact-Name (Browser-Tab/Galerie) - nur der Projektname, "
                             "ohne Praefix. Weggelassen: wird aus --titel abgeleitet.")
    args = parser.parse_args()

    dateien = sammle_relevante_dateien(args.dateien)
    if not dateien:
        print("Keine relevanten Dateien gefunden.")
        return 1

    html = bauen(dateien, args.titel, args.name)
    args.out.write_text(html, encoding="utf-8")
    print(f"Vorschau erzeugt: {args.out} ({len(html)} Bytes, {len(dateien)} Dateien)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
