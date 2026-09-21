"""Erzeugt aus der Kienbacher-Bildmarke (SVG) die beiden PNG, die der
Kartengenerator einbettet:

    logo_farbe.png   Originalfarben, transparenter Hintergrund
    logo_weiss.png   alle Pfade weiss (Knockout fuer das blaue Kopfband)

Wird VON HAND aufgerufen, nicht bei jedem Kartenlauf. Damit bleibt der
Produktivpfad frei von svglib, reportlab und pypdfium2 - faellt eine dieser
Bibliotheken auf einem anderen Rechner aus, laesst sich trotzdem eine Karte
erzeugen. Ausserdem ist das eingebettete Bild so auf jedem Rechner byteidentisch.

Aufruf:  python logo_erzeugen.py
"""
from __future__ import annotations

import hashlib
import io
import re
import sys
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"
QUELLE = ASSETS / "kienbacher_bildmarke.svg"
SKALA = 8  # ergibt rund 2400 px Breite - genug fuer 300 dpi bei 22 mm Breite

CI_BLAU = "#0079a7"
CI_GRAU = "#7b7c7e"


def svg_zu_png(svg_text: str, skala: int = SKALA) -> bytes:
    """SVG -> ReportLab-Drawing -> PDF -> pypdfium2 -> PNG mit Alphakanal.

    Der Umweg ueber PDF ist Absicht: svglib.renderPM braucht den Backend
    rlPyCairo, der hier fehlt und eine C-Bibliothek nachzieht. renderPDF
    braucht keinen Rasterisierer, und pypdfium2 bringt seinen eigenen mit.
    """
    from reportlab.graphics import renderPDF
    from svglib.svglib import svg2rlg
    import pypdfium2 as pdfium

    # bytes, nicht str: lxml lehnt einen str mit XML-Encoding-Deklaration ab
    zeichnung = svg2rlg(io.BytesIO(svg_text.encode("utf-8")))
    if zeichnung is None:
        raise RuntimeError("svglib konnte die SVG nicht lesen")
    pdf_bytes = renderPDF.drawToString(zeichnung)

    seite = pdfium.PdfDocument(pdf_bytes)[0]
    bitmap = seite.render(scale=skala, fill_color=(255, 255, 255, 0))
    bild = bitmap.to_pil().convert("RGBA")

    # Auf den sichtbaren Inhalt beschneiden. Die SVG-viewBox ist deutlich
    # groesser als die Bildmarke; ohne Beschnitt haengt unsichtbarer Rand am
    # Bild und die Platzierung im Kopfband stimmt nicht mit der Angabe ueberein.
    kasten = bild.getbbox()
    if kasten is None:
        raise RuntimeError("Gerendertes Logo ist leer")
    bild = bild.crop(kasten)

    puffer = io.BytesIO()
    bild.save(puffer, format="PNG", optimize=True)
    return puffer.getvalue()


def einfaerben_weiss(svg_text: str) -> str:
    """Ersetzt beide CI-Farben durch Weiss.

    Ueber den SVG-Text, nicht ueber das gerenderte Bild: wer das Bild
    nachtraeglich einfaerbt, bekommt an den Antialiasing-Kanten graue Saeume,
    die auf dem blauen Kopfband sichtbar werden.
    """
    return re.sub(
        r"#(?:0079a7|7b7c7e)",
        "#ffffff",
        svg_text,
        flags=re.IGNORECASE,
    )


def main() -> int:
    if not QUELLE.exists():
        print(f"FEHLER: {QUELLE} fehlt", file=sys.stderr)
        return 1

    svg_text = QUELLE.read_text(encoding="utf-8")

    if CI_BLAU not in svg_text.lower() or CI_GRAU not in svg_text.lower():
        print(
            "FEHLER: Die SVG enthaelt nicht beide CI-Farben. Entweder ist es die "
            "falsche Datei, oder das Logo wurde geaendert - dann ist die "
            "Weiss-Variante von Hand zu pruefen.",
            file=sys.stderr,
        )
        return 1

    ergebnisse = {
        "logo_farbe.png": svg_zu_png(svg_text),
        "logo_weiss.png": svg_zu_png(einfaerben_weiss(svg_text)),
    }

    zeilen = []
    for name, daten in ergebnisse.items():
        ziel = ASSETS / name
        ziel.write_bytes(daten)
        pruefsumme = hashlib.sha256(daten).hexdigest()
        zeilen.append(f"{pruefsumme}  {name}")
        print(f"  {name:16s} {len(daten):7d} Bytes")

    quell_summe = hashlib.sha256(QUELLE.read_bytes()).hexdigest()
    zeilen.append(f"{quell_summe}  {QUELLE.name}")
    (ASSETS / "logo.sha256").write_text("\n".join(zeilen) + "\n", encoding="utf-8")
    print(f"  logo.sha256      geschrieben")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
