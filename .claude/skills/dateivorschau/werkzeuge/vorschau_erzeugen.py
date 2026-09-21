"""Baut aus beliebigen Dateien eine eigenstaendige HTML-Uebersicht mit
Download-Button je Datei.

    python vorschau_erzeugen.py datei1.pptx datei2.png ... --out vorschau.html

Kein Renderversuch des Originalformats (PPTX/DOCX/XLSX lassen sich in dieser
Umgebung nicht zuverlaessig serverseitig rendern - LibreOffice haengt sich in
der Sandbox ohne Fehlermeldung auf, auch bei trivialen Dateien). Stattdessen:
Bilder und PDFs werden inline angezeigt, weil Browser das nativ koennen.
Alles andere (PPTX, DOCX, XLSX, ZIP, ...) bekommt eine Karte mit Dateityp,
Groesse und einem Download-Button - Oeffnen, Bearbeiten und Drucken passiert
im jeweiligen Originalprogramm (PowerPoint, Word, ...), nicht im Browser.

Funktioniert nur als eigenstaendige Datei (lokal geoeffnet oder per Datei
weitergegeben) - in einer eingebetteten/sandboxed Ansicht (z. B. ein
Artifact-Link) sind von der Seite selbst ausgeloeste Downloads blockiert.
"""
from __future__ import annotations

import argparse
import base64
import mimetypes
from pathlib import Path

BILD_TYPEN = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}
PDF_TYPEN = {".pdf"}

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


def groesse_lesbar(bytes_zahl: int) -> str:
    wert = float(bytes_zahl)
    for einheit in ("B", "KB", "MB", "GB"):
        if wert < 1024 or einheit == "GB":
            return f"{wert:.0f} {einheit}" if einheit == "B" else f"{wert:.1f} {einheit}"
        wert /= 1024
    return f"{wert:.1f} GB"


def datei_karte(pfad: Path) -> str:
    ext = pfad.suffix.lower()
    daten = pfad.read_bytes()
    b64 = base64.b64encode(daten).decode()
    mime = mimetypes.guess_type(pfad.name)[0] or "application/octet-stream"
    typ_label = TYP_LABEL.get(ext, ext.lstrip(".").upper() or "Datei")
    groesse = groesse_lesbar(len(daten))
    data_url = f"data:{mime};base64,{b64}"

    vorschau = ""
    if ext in BILD_TYPEN:
        vorschau = f'<div class="preview img-preview"><img src="{data_url}" alt="{esc(pfad.name)}" /></div>'
    elif ext in PDF_TYPEN:
        vorschau = f'<div class="preview pdf-preview"><embed src="{data_url}" type="application/pdf" /></div>'
    else:
        vorschau = f'<div class="preview no-preview"><span class="file-badge">{esc(typ_label)}</span></div>'

    return f'''
<article class="card">
  {vorschau}
  <div class="meta">
    <h2>{esc(pfad.name)}</h2>
    <p class="sub">{esc(typ_label)} &middot; {groesse}</p>
  </div>
  <a class="btn" href="{data_url}" download="{esc(pfad.name)}">Herunterladen</a>
</article>'''


def bauen(pfade: list[Path], titel: str) -> str:
    karten = "\n".join(datei_karte(p) for p in pfade)
    return TEMPLATE.format(titel=esc(titel), karten=karten)


TEMPLATE = '''<title>{titel}</title>
<meta name="description" content="Dateien im Original herunterladen - zum Oeffnen, Bearbeiten und Drucken im jeweiligen Programm." />
<style>
  :root {{ --bg:#EFEEEA; --panel:#FFFFFF; --ink:#1B1F22; --muted:#6B6F73; --accent:#0079A7; --accent-ink:#00435C; --line:#D8DBDD; }}
  @media (prefers-color-scheme: dark) {{
    :root:not([data-theme="light"]) {{ --bg:#14171A; --panel:#1D2124; --ink:#EDEFF1; --muted:#9BA0A5; --accent:#4DB8E0; --accent-ink:#7FD1EE; --line:#33383C; }}
  }}
  :root[data-theme="dark"] {{ --bg:#14171A; --panel:#1D2124; --ink:#EDEFF1; --muted:#9BA0A5; --accent:#4DB8E0; --accent-ink:#7FD1EE; --line:#33383C; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; padding-inline:16px; padding-block:24px; background:var(--bg); color:var(--ink); font-family:Arial, Helvetica, sans-serif; }}
  .wrap {{ max-width:960px; margin:0 auto; }}
  h1 {{ font-size:clamp(20px,4vw,28px); color:var(--accent-ink); margin:0 0 6px; text-wrap:balance; }}
  .sub-page {{ color:var(--muted); font-size:14px; margin:0 0 24px; max-width:65ch; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(240px,1fr)); gap:16px; }}
  .card {{ background:var(--panel); border:1px solid var(--line); border-radius:10px; overflow:hidden; display:flex; flex-direction:column; box-shadow:0 6px 20px -14px rgba(0,0,0,.3); }}
  .preview {{ background:var(--bg); display:flex; align-items:center; justify-content:center; min-height:140px; border-bottom:1px solid var(--line); }}
  .img-preview img {{ width:100%; height:140px; object-fit:contain; }}
  .pdf-preview embed {{ width:100%; height:180px; }}
  .no-preview {{ padding:20px; }}
  .file-badge {{ display:inline-block; padding:6px 12px; border-radius:6px; background:var(--accent); color:#FFFFFF; font-size:12px; font-weight:700; letter-spacing:.02em; }}
  .meta {{ padding:12px 14px 4px; flex:1; }}
  .meta h2 {{ font-size:14px; margin:0 0 4px; word-break:break-word; color:var(--ink); }}
  .meta .sub {{ font-size:12px; color:var(--muted); margin:0; }}
  .btn {{ margin:12px 14px 14px; text-align:center; padding:9px 14px; border-radius:6px; background:var(--accent); color:#FFFFFF; font-weight:700; font-size:13px; text-decoration:none; }}
  footer {{ margin-top:28px; padding-top:14px; border-top:1px solid var(--line); font-size:12px; color:var(--muted); }}
</style>
<div class="wrap">
  <header>
    <h1>{titel}</h1>
    <p class="sub-page">Original-Dateien zum Herunterladen. Oeffnen, Bearbeiten und Drucken passiert im jeweiligen Programm (PowerPoint, Word, Bildbetrachter, ...), nicht in dieser Seite.</p>
  </header>
  <div class="grid">{karten}</div>
  <footer>Kienbacher &middot; Datei-Vorschau</footer>
</div>
'''


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dateien", type=Path, nargs="+")
    parser.add_argument("--out", type=Path, default=Path("vorschau.html"))
    parser.add_argument("--titel", default="Dateien")
    args = parser.parse_args()

    html = bauen(args.dateien, args.titel)
    args.out.write_text(html, encoding="utf-8")
    print(f"Vorschau erzeugt: {args.out} ({len(html)} Bytes, {len(args.dateien)} Dateien)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
