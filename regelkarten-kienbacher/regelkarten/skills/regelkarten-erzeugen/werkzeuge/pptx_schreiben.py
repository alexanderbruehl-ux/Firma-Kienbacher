"""Schreibt eine Rahmenliste als PPTX im A4-Hochformat.

Jede Flaeche, jeder Text und jede Linie wird ein eigenes Objekt. Die Karte ist
nie ein flaches Bild - wer sie oeffnet, kann jedes Element anfassen.
"""
from __future__ import annotations

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.util import Emu, Pt

import ci
from rahmen import Bild, Flaeche, Linie, Seite, Text

AUSRICHTUNG = {
    "links": PP_ALIGN.LEFT,
    "mitte": PP_ALIGN.CENTER,
    "rechts": PP_ALIGN.RIGHT,
}


def _farbe(hex_wert: str) -> RGBColor:
    return RGBColor.from_string(hex_wert)


def _flaeche_setzen(folie, r: Flaeche) -> None:
    form = MSO_SHAPE.ROUNDED_RECTANGLE if r.gerundet else MSO_SHAPE.RECTANGLE
    shape = folie.shapes.add_shape(
        form, ci.mm(r.x), ci.mm(r.y), ci.mm(r.b), ci.mm(r.h))
    # Ohne das erben die Formen den Schlagschatten des Office-Themes - auf einer
    # Arbeitsanweisung sieht das unruhig aus und kostet im Druck Kontrast.
    shape.shadow.inherit = False
    shape.name = "flaeche-" + (r.gruppe or "x")

    if r.gerundet:
        # Adjust so setzen, dass der Eckradius absolut konstant bleibt.
        shape.adjustments[0] = ci.eckradius_adj(r.b, r.h)

    if r.fuellung:
        shape.fill.solid()
        shape.fill.fore_color.rgb = _farbe(r.fuellung)
    else:
        shape.fill.background()

    if r.rand and r.randstaerke_pt > 0:
        shape.line.color.rgb = _farbe(r.rand)
        shape.line.width = Pt(r.randstaerke_pt)
    else:
        shape.line.fill.background()

    # Die Flaeche traegt keinen Text - der liegt in eigenen Rahmen darueber.
    shape.text_frame.text = ""


def _text_setzen(folie, r: Text) -> None:
    # Halbe Zeile Reserve: Weicht PowerPoints Umbruch um eine Zeile von unserer
    # Messung ab, bleibt sie sichtbar statt aus dem Rahmen zu fallen.
    hoehe = r.h + ci.zeilenhoehe_mm(r.grad_pt) * 0.5
    kasten = folie.shapes.add_textbox(
        ci.mm(r.x), ci.mm(r.y), ci.mm(r.b), ci.mm(hoehe))
    kasten.name = "text-" + (r.gruppe or "x")

    tf = kasten.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.vertical_anchor = MSO_ANCHOR.TOP
    # Pflicht: PowerPoint setzt sonst 2,54 mm Innenabstand links und rechts.
    # Die Messung ginge dann um rund 6 % daneben - regelmaessig eine Zeile.
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

    absaetze = r.inhalt.split(chr(10)) or [""]
    for i, zeile in enumerate(absaetze):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = AUSRICHTUNG.get(r.ausrichtung, PP_ALIGN.LEFT)
        # Absolute Zeilenhoehe in Punkt. Dadurch haengt die Hoehe des Blocks
        # nicht davon ab, welche Schrift auf dem oeffnenden Rechner liegt.
        p.line_spacing = Pt(r.grad_pt * ci.ZEILENFAKTOR)
        p.space_before = Pt(0)
        p.space_after = Pt(0)

        lauf = p.add_run()
        lauf.text = zeile
        schrift = lauf.font
        schrift.name = r.schrift
        schrift.size = Pt(r.grad_pt)
        schrift.bold = r.fett
        schrift.color.rgb = _farbe(r.farbe)

        if r.sperrung:
            # Zeichenabstand kennt python-pptx nicht - direkt ins XML.
            lauf._r.get_or_add_rPr().set("spc", str(int(round(r.sperrung * 100))))

        # Ersatzschrift steuern: Was PowerPoint nicht aufloesen kann, soll auf
        # Arial fallen und nicht auf die Theme-Schrift Calibri.
        rpr = lauf._r.get_or_add_rPr()
        for kennung in ("a:ea", "a:cs"):
            from pptx.oxml.ns import qn
            element = rpr.makeelement(qn(kennung), {"typeface": ci.SCHRIFT_TEXT})
            rpr.append(element)


def _linie_setzen(folie, r: Linie) -> None:
    shape = folie.shapes.add_connector(
        MSO_CONNECTOR.STRAIGHT,
        ci.mm(r.x1), ci.mm(r.y1), ci.mm(r.x2), ci.mm(r.y2))
    shape.name = "linie-" + (r.gruppe or "x")
    shape.line.color.rgb = _farbe(r.farbe)
    shape.line.width = Pt(r.staerke_pt)
    shape.shadow.inherit = False


def _bild_setzen(folie, r: Bild) -> None:
    shape = folie.shapes.add_picture(
        r.pfad, ci.mm(r.x), ci.mm(r.y), ci.mm(r.b), ci.mm(r.h))
    shape.name = "logo"


def schreiben(seite: Seite, ziel: Path) -> Path:
    praesentation = Presentation()
    praesentation.slide_width = Emu(ci.mm(ci.SEITE_B_MM))
    praesentation.slide_height = Emu(ci.mm(ci.SEITE_H_MM))

    leeres_layout = praesentation.slide_layouts[6]
    folie = praesentation.slides.add_slide(leeres_layout)

    hintergrund = folie.background
    hintergrund.fill.solid()
    hintergrund.fill.fore_color.rgb = _farbe(ci.WEISS)

    # Reihenfolge der Liste ist die Stapelreihenfolge: Flaechen zuerst, Texte
    # darueber. Das leistet layout.py bereits, hier wird nur ausgegeben.
    for r in seite.rahmen:
        if isinstance(r, Flaeche):
            _flaeche_setzen(folie, r)
        elif isinstance(r, Text):
            _text_setzen(folie, r)
        elif isinstance(r, Linie):
            _linie_setzen(folie, r)
        elif isinstance(r, Bild):
            _bild_setzen(folie, r)
        else:
            raise TypeError("Unbekannter Rahmentyp: " + type(r).__name__)

    ziel.parent.mkdir(parents=True, exist_ok=True)
    praesentation.save(str(ziel))
    return ziel
