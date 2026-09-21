"""Baut aus fertigen Regelkarten-PPTX eine einzelne, eigenstaendige HTML-Vorschau.

    python vorschau_erzeugen.py RK-012.pptx RK-013.pptx ... --out vorschau.html

Liest Position, Farbe, Schrift und Text direkt aus den PPTX-Dateien (nicht aus
der JSON-Definition) - die Vorschau zeigt also exakt das, was auch tatsaechlich
erzeugt wurde. Track.ttf und das Logo werden aus den Plugin-Assets eingebettet,
Arial bleibt Systemschrift (wie auf der echten Karte auch) - die Datei ist
trotzdem ohne weitere Abhaengigkeiten in jedem Browser lauffaehig und lasst
sich direkt an Kolleginnen und Kollegen weitergeben (E-Mail, OneDrive, Chat),
auch ohne Claude-Zugang.

Kein Ersatz fuer die Sichtpruefung in PowerPoint aus `regelkarten-erzeugen` -
nur eine schnelle, teilbare Ansicht mehrerer Karten nebeneinander. Bearbeiten
und Drucken passiert im Original: jede Karte hat einen Download-Button fuer
die PPTX, kein Inline-Druck (serverseitiges PPTX-Rendering ist in dieser
Umgebung nicht verlaesslich moeglich, und ein Druck aus dem Browser heraus
war in der eingebetteten Ansicht blockiert - siehe `dateivorschau` fuer die
allgemeine, projektunabhaengige Variante desselben Download-Ansatzes).
"""
from __future__ import annotations

import argparse
import base64
import json
from pathlib import Path

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

HIER = Path(__file__).resolve().parent
ASSETS = HIER.parent.parent / "regelkarten-erzeugen" / "assets"
TRACK_TTF = ASSETS / "Track.ttf"
LOGO_PNG = ASSETS / "logo_weiss.png"

EMU_PER_MM = 36000
ALIGN = {"LEFT (1)": "left", "CENTER (2)": "center", "RIGHT (3)": "right", None: "left"}


def mm(v) -> float:
    return round((v or 0) / EMU_PER_MM, 3)


def rgb(fill) -> str | None:
    try:
        return str(fill.fore_color.rgb) if fill.type is not None else None
    except Exception:
        return None


def karte_lesen(pfad: Path) -> dict:
    prs = Presentation(str(pfad))
    slide = prs.slides[0]
    shapes = []
    for shp in slide.shapes:
        item = {"type": str(shp.shape_type), "x": mm(shp.left), "y": mm(shp.top),
                "w": mm(shp.width), "h": mm(shp.height)}
        if shp.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE:
            item["autoshape"] = str(shp.auto_shape_type)
            item["fill"] = rgb(shp.fill)
            try:
                item["line_color"] = str(shp.line.color.rgb) if shp.line.color.type is not None else None
                item["line_w_pt"] = shp.line.width.pt if shp.line.width else 0
            except Exception:
                item["line_color"], item["line_w_pt"] = None, 0
        elif shp.shape_type == MSO_SHAPE_TYPE.LINE:
            try:
                item["line_color"] = str(shp.line.color.rgb) if shp.line.color.type is not None else None
                item["line_w_pt"] = shp.line.width.pt if shp.line.width else 0
            except Exception:
                item["line_color"], item["line_w_pt"] = None, 0
        elif shp.shape_type == MSO_SHAPE_TYPE.PICTURE:
            item["is_logo"] = True
        if shp.has_text_frame:
            tf = shp.text_frame
            item["anchor"] = str(tf.vertical_anchor) if tf.vertical_anchor is not None else None
            paras = []
            for para in tf.paragraphs:
                runs = []
                for run in para.runs:
                    if not run.text:
                        continue
                    try:
                        color = str(run.font.color.rgb)
                    except Exception:
                        color = None
                    runs.append({"text": run.text, "size": run.font.size.pt if run.font.size else 11,
                                "bold": bool(run.font.bold), "color": color, "font": run.font.name})
                paras.append({"runs": runs, "align": str(para.alignment) if para.alignment is not None else None})
            item["paragraphs"] = paras
        shapes.append(item)
    return {"width_mm": mm(prs.slide_width), "height_mm": mm(prs.slide_height), "shapes": shapes}


def esc(t: str) -> str:
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def shape_html(s: dict, logo_b64: str) -> str:
    x, y, w, h = s["x"], s["y"], s["w"], s["h"]
    base = f"left:{x}mm;top:{y}mm;width:{w}mm;height:{h}mm;"
    out = []

    if s["type"] == "AUTO_SHAPE (1)":
        radius = "3mm" if "ROUNDED" in (s.get("autoshape") or "") else "0"
        style = base + f"position:absolute;border-radius:{radius};"
        style += f'background:#{s["fill"]};' if s.get("fill") else "background:transparent;"
        if s.get("line_color") and s.get("line_w_pt"):
            style += f'border:{s["line_w_pt"]}pt solid #{s["line_color"]};box-sizing:border-box;'
        out.append(f'<div class="shape" style="{style}"></div>')
    elif s["type"] == "LINE (9)":
        lw, color = s.get("line_w_pt") or 0.5, s.get("line_color") or "7B7C7E"
        if w <= h:
            style = f"position:absolute;left:{x}mm;top:{y}mm;width:0;height:{h}mm;border-left:{lw}pt solid #{color};"
        else:
            style = f"position:absolute;left:{x}mm;top:{y}mm;width:{w}mm;height:0;border-top:{lw}pt solid #{color};"
        out.append(f'<div class="line" style="{style}"></div>')
    elif s["type"] == "PICTURE (13)":
        out.append(f'<img class="logo" src="data:image/png;base64,{logo_b64}" '
                   f'style="{base}position:absolute;" alt="Kienbacher" />')

    if s.get("paragraphs"):
        justify = "center" if s.get("anchor") == "MIDDLE (3)" else "flex-start"
        style = base + f"position:absolute;display:flex;flex-direction:column;justify-content:{justify};box-sizing:border-box;"
        lines = []
        for p in s["paragraphs"]:
            align = ALIGN.get(p["align"], "left")
            runs = []
            for r in p["runs"]:
                fam = "'Track', Arial, sans-serif" if r["font"] == "Track" else "Arial, Helvetica, sans-serif"
                runs.append(f'<span style="font-family:{fam};font-weight:{700 if r["bold"] else 400};'
                           f'color:#{r["color"] or "000000"};font-size:{r["size"]}pt;">{esc(r["text"])}</span>')
            if runs:
                lines.append(f'<p style="margin:0;text-align:{align};line-height:1.15;">{"".join(runs)}</p>')
        out.append(f'<div class="text" style="{style}">{"".join(lines)}</div>')
    return "\n".join(out)


PPTX_MIME = "application/vnd.openxmlformats-officedocument.presentationml.presentation"


def bauen(pfade: list[Path], titel: str, mit_download: bool = True) -> str:
    track_b64 = base64.b64encode(TRACK_TTF.read_bytes()).decode() if TRACK_TTF.exists() else ""
    logo_b64 = base64.b64encode(LOGO_PNG.read_bytes()).decode() if LOGO_PNG.exists() else ""

    karten = [(p.stem, p, karte_lesen(p)) for p in pfade]
    tabs, sections = [], []
    for i, (name, pfad, karte) in enumerate(karten):
        aktiv = " active" if i == 0 else ""
        ausgewaehlt = "true" if i == 0 else "false"
        tabs.append(f'<button class="tab" role="tab" data-target="card-{name}" '
                   f'aria-selected="{ausgewaehlt}">{esc(name)}</button>')
        shapes = "\n".join(shape_html(s, logo_b64) for s in karte["shapes"])

        toolbar = '<div class="toolbar">'
        if mit_download:
            pptx_b64 = base64.b64encode(pfad.read_bytes()).decode()
            toolbar += (f'<a class="btn" download="{esc(pfad.name)}" '
                       f'href="data:{PPTX_MIME};base64,{pptx_b64}">PPTX herunterladen</a>')
            toolbar += '<span class="print-hint">Bearbeiten und Drucken in PowerPoint</span>'
        else:
            toolbar += '<span class="print-hint">Download nur in der eigenstaendigen HTML-Datei verfuegbar</span>'
        toolbar += '</div>'

        sections.append(f'''
<section class="card-block{aktiv}" id="card-{name}">
  {toolbar}
  <div class="sheet-outer">
    <div class="sheet" style="width:{karte["width_mm"]}mm;height:{karte["height_mm"]}mm;">
      {shapes}
    </div>
  </div>
</section>''')

    return TEMPLATE.format(titel=esc(titel), track_b64=track_b64,
                           tabs="\n".join(tabs), sections="\n".join(sections))


TEMPLATE = '''<title>{titel}</title>
<meta name="description" content="Facsimile-Vorschau von Kienbacher-Regelkarten im Originalformat." />
<style>
  @font-face {{ font-family: 'Track'; src: url(data:font/ttf;base64,{track_b64}) format('truetype'); font-display: swap; }}
  :root {{ --bg:#EFEEEA; --panel:#FFFFFF; --ink:#1B1F22; --muted:#6B6F73; --accent:#0079A7; --accent-ink:#00435C; --line:#D8DBDD; }}
  @media (prefers-color-scheme: dark) {{
    :root:not([data-theme="light"]) {{ --bg:#14171A; --panel:#1D2124; --ink:#EDEFF1; --muted:#9BA0A5; --accent:#4DB8E0; --accent-ink:#7FD1EE; --line:#33383C; }}
  }}
  :root[data-theme="dark"] {{ --bg:#14171A; --panel:#1D2124; --ink:#EDEFF1; --muted:#9BA0A5; --accent:#4DB8E0; --accent-ink:#7FD1EE; --line:#33383C; }}
  * {{ box-sizing: border-box; }}
  body {{ margin:0; padding-inline:16px; padding-block:24px; background:var(--bg); color:var(--ink); font-family: Arial, Helvetica, sans-serif; }}
  .wrap {{ max-width:900px; margin:0 auto; }}
  h1 {{ font-family:'Track', Arial, sans-serif; font-size:clamp(22px,4vw,30px); letter-spacing:.02em; color:var(--accent-ink); margin:0 0 6px; text-wrap:balance; }}
  .sub {{ color:var(--muted); font-size:14px; margin:0; max-width:60ch; }}
  .tabs {{ display:flex; gap:6px; margin:22px 0 14px; border-bottom:1px solid var(--line); overflow-x:auto; }}
  .tab {{ flex:none; padding:9px 16px; font-size:13px; font-weight:700; letter-spacing:.02em; color:var(--muted); background:none; border:none; border-bottom:2px solid transparent; cursor:pointer; font-family:inherit; }}
  .tab[aria-selected="true"] {{ color:var(--accent-ink); border-bottom-color:var(--accent); }}
  .card-block {{ display:none; }}
  .card-block.active {{ display:block; }}
  .toolbar {{ display:flex; gap:8px; margin-bottom:10px; flex-wrap:wrap; }}
  .btn {{
    font-family:inherit; font-size:13px; font-weight:700; letter-spacing:.01em;
    padding:8px 14px; border-radius:6px; border:1px solid var(--accent);
    background:var(--accent); color:#FFFFFF; text-decoration:none; cursor:pointer;
    display:inline-flex; align-items:center; gap:6px;
  }}
  .btn[aria-disabled="true"] {{ opacity:.5; cursor:not-allowed; pointer-events:none; }}
  .sheet-outer {{ background:var(--panel); border:1px solid var(--line); border-radius:8px; box-shadow:0 8px 28px -14px rgba(0,0,0,.35); overflow:hidden; padding:14px; }}
  .sheet {{ position:relative; background:#FFFFFF; transform-origin:top left; margin:0 auto; }}
  .print-hint {{ font-size:12px; color:var(--muted); align-self:center; }}
  footer {{ margin-top:26px; padding-top:14px; border-top:1px solid var(--line); font-size:12px; color:var(--muted); }}
</style>
<div class="wrap">
  <header>
    <h1>{titel}</h1>
    <p class="sub">Facsimile der Regelkarten im Kienbacher-CI, originalgetreu aus den PPTX-Dateien nachgebaut. Ersetzt nicht die Sichtpruefung in PowerPoint. Bearbeiten und Drucken passiert in PowerPoint selbst - siehe Download-Button je Karte.</p>
  </header>
  <div class="tabs" role="tablist">
    {tabs}
  </div>
  {sections}
  <footer>Kienbacher Akademie - Regelkarten-Plugin (Rudi)</footer>
</div>
<script>
(function() {{
  var blocks = document.querySelectorAll('.card-block');
  var tabs = document.querySelectorAll('.tab');
  function activate(id) {{
    blocks.forEach(function(b) {{ b.classList.toggle('active', b.id === id); }});
    tabs.forEach(function(t) {{ t.setAttribute('aria-selected', t.dataset.target === id ? 'true' : 'false'); }});
    fitAll();
  }}
  tabs.forEach(function(t) {{ t.addEventListener('click', function() {{ activate(t.dataset.target); }}); }});

  function fitAll() {{
    document.querySelectorAll('.card-block.active .sheet-outer').forEach(function(outer) {{
      var sheet = outer.querySelector('.sheet');
      if (!sheet) return;
      sheet.style.transform = 'scale(1)';
      var naturalW = sheet.offsetWidth, naturalH = sheet.offsetHeight;
      var scale = Math.min(1, (outer.clientWidth - 28) / naturalW);
      sheet.style.transform = 'scale(' + scale + ')';
      outer.style.height = Math.round(naturalH * scale + 28) + 'px';
    }});
  }}
  window.addEventListener('resize', fitAll);
  window.addEventListener('load', fitAll);
  fitAll();
  setTimeout(fitAll, 300);
}})();
</script>
'''


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("karten", type=Path, nargs="+", help="Eine oder mehrere Karten-PPTX")
    parser.add_argument("--out", type=Path, default=Path("vorschau.html"))
    parser.add_argument("--titel", default="Regelkarten Vorschau")
    parser.add_argument("--ohne-download", action="store_true",
                        help="Keine PPTX-Downloadlinks einbetten - fuer gehostete "
                             "Ansichten (z. B. Artifact), in denen Downloads aus der "
                             "Seite heraus ohnehin blockiert sind.")
    args = parser.parse_args()

    html = bauen(args.karten, args.titel, mit_download=not args.ohne_download)
    args.out.write_text(html, encoding="utf-8")
    print(f"Vorschau erzeugt: {args.out} ({len(html)} Bytes, {len(args.karten)} Karten)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
