"""Die Zwischendarstellung zwischen Layout und PPTX.

Eine Karte ist an dieser Stelle eine flache Liste von Rahmen in Millimetern.
Damit laesst sich die Geometrie pruefen (pruefung.py) und rendern
(karte_bauen.py), ohne dass eine Datei entstehen muss.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Flaeche:
    x: float
    y: float
    b: float
    h: float
    fuellung: str | None
    rand: str | None = None
    randstaerke_pt: float = 0.0
    gerundet: bool = True
    gruppe: str = ""


@dataclass
class Text:
    """Ein Textrahmen.

    ``inhalt`` ist der ungebrochene Originaltext - genau der wird in die PPTX
    geschrieben, damit PowerPoint selbst umbricht und der Absatz beim Bearbeiten
    zusammenbleibt. ``zeilen`` ist nur das Messergebnis und dient allein der
    Hoehenrechnung.
    """

    x: float
    y: float
    b: float
    inhalt: str
    zeilen: list[str]
    schrift: str
    grad_pt: float
    fett: bool = False
    farbe: str = "00435C"
    sperrung: float = 0.0          # zusaetzlicher Zeichenabstand in pt
    ausrichtung: str = "links"     # links | mitte | rechts
    gruppe: str = ""

    @property
    def h(self) -> float:
        import ci
        return len(self.zeilen) * ci.zeilenhoehe_mm(self.grad_pt)


@dataclass
class Linie:
    x1: float
    y1: float
    x2: float
    y2: float
    farbe: str
    staerke_pt: float = 1.0
    gruppe: str = ""


@dataclass
class Bild:
    x: float
    y: float
    b: float
    h: float
    pfad: str
    gruppe: str = ""


Rahmen = Flaeche | Text | Linie | Bild


@dataclass
class Seite:
    rahmen: list[Rahmen] = field(default_factory=list)

    def dazu(self, *neue: Rahmen) -> None:
        self.rahmen.extend(neue)

    def unterkante(self) -> float:
        unten = 0.0
        for r in self.rahmen:
            if isinstance(r, Linie):
                unten = max(unten, r.y1, r.y2)
            else:
                unten = max(unten, r.y + r.h)
        return unten
