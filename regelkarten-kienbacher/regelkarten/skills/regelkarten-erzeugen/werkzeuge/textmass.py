"""Schriftvermessung und Umbruchsimulation.

Der Generator muss vor dem Setzen wissen, wie viele Zeilen ein Text bei
gegebener Boxbreite belegt - sonst laesst sich nicht pruefen, ob die Karte auf
eine A4-Seite passt. Gemessen wird gegen die echten Schriftdateien.
"""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from fontTools.ttLib import TTFont

import ci

ASSETS = Path(__file__).resolve().parent.parent / "assets"

WINDOWS_FONTS = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts"

SCHRIFTDATEIEN = {
    ("Arial", False): WINDOWS_FONTS / "arial.ttf",
    ("Arial", True): WINDOWS_FONTS / "arialbd.ttf",
    ("Track", False): ASSETS / "Track.ttf",
    ("Track", True): ASSETS / "Track.ttf",   # Track hat keinen Fettschnitt
}

# Zeichen, die Track nicht kennt, aber im Deutschen leicht entstehen.
# Sie werden ersetzt, statt als Ersatzkaestchen auf der Karte zu landen.
ERSATZ = {
    "\u2013": "-",    # en dash
    "\u2014": "-",    # em dash
    "\u2192": "->",   # Pfeil
    "\u00a0": " ",    # geschuetztes Leerzeichen
    "\u2212": "-",    # Minus
}

# Nach diesen Zeichen darf umgebrochen werden, auch ohne Leerzeichen.
# Ohne das brechen Woerter wie "Erststueckfreigabe-Pruefung" oder
# "PQB/Teamleader" in der 54 mm schmalen Rollenspalte mitten im Wort.
TRENNZEICHEN = "-/)\u2013"


class Schriftfehlt(RuntimeError):
    pass


class Schriftmass:
    """Misst Textbreiten in em anhand der Vorschubweiten der Schriftdatei."""

    def __init__(self, pfad: Path):
        if not pfad.exists():
            raise Schriftfehlt(
                f"Schriftdatei nicht gefunden: {pfad}\n"
                f"Arial wird unter {WINDOWS_FONTS} erwartet, Track unter {ASSETS}."
            )
        self.pfad = pfad
        self._font = TTFont(str(pfad), lazy=True)
        self.upm = self._font["head"].unitsPerEm
        self.cmap = self._font.getBestCmap()
        self._hmtx = self._font["hmtx"]
        self._kern = self._kernpaare()
        self._ersatzglyph = self.cmap.get(ord("?"))

    def _kernpaare(self) -> dict[tuple[str, str], int]:
        """Paare aus der 'kern'-Tabelle. GPOS bleibt unausgewertet - der
        Unterschied liegt unter einem halben Prozent und wird vom
        Sicherheitszuschlag in ci.SICHERHEIT mit abgedeckt."""
        if "kern" not in self._font:
            return {}
        paare: dict[tuple[str, str], int] = {}
        for tabelle in self._font["kern"].kernTables:
            paare.update(tabelle.kernTable)
        return paare

    def _glyph(self, zeichen: str) -> str | None:
        return self.cmap.get(ord(zeichen), self._ersatzglyph)

    def kennt(self, zeichen: str) -> bool:
        return ord(zeichen) in self.cmap

    def fehlende_zeichen(self, text: str) -> list[str]:
        return sorted({z for z in text if not z.isspace() and not self.kennt(z)})

    def breite_em(self, text: str) -> float:
        summe = 0
        vorher: str | None = None
        for zeichen in text:
            glyph = self._glyph(zeichen)
            if glyph is None:
                continue
            summe += self._hmtx[glyph][0]
            if vorher is not None:
                summe += self._kern.get((vorher, glyph), 0)
            vorher = glyph
        return summe / self.upm

    def breite_mm(self, text: str, grad_pt: float) -> float:
        return ci.mm_aus_pt(self.breite_em(text) * grad_pt) * ci.SICHERHEIT


@lru_cache(maxsize=None)
def schrift(name: str, fett: bool = False) -> Schriftmass:
    schluessel = (name, fett)
    if schluessel not in SCHRIFTDATEIEN:
        raise Schriftfehlt(f"Unbekannte Schrift: {name} (fett={fett})")
    return Schriftmass(SCHRIFTDATEIEN[schluessel])


def bereinigen(text: str) -> str:
    """Ersetzt Zeichen, die Track nicht kennt, und normalisiert Leerraum."""
    for alt, neu in ERSATZ.items():
        text = text.replace(alt, neu)
    return text


def _teilstuecke(wort: str) -> list[str]:
    """Zerlegt ein Wort an zulaessigen Trennstellen, Trennzeichen bleibt vorn."""
    stuecke: list[str] = []
    aktuell = ""
    for zeichen in wort:
        aktuell += zeichen
        if zeichen in TRENNZEICHEN and aktuell.strip(TRENNZEICHEN):
            stuecke.append(aktuell)
            aktuell = ""
    if aktuell:
        stuecke.append(aktuell)
    return stuecke or [wort]


def _notumbruch(zeile: str, mass: "Schriftmass", grad_pt: float,
                breite_mm: float) -> list[str]:
    """Zerlegt eine Zeile, die auch als Ganzes nicht passt, zeichenweise.

    Greift nur bei Woertern, die breiter sind als ihre Spalte - etwa
    "Betriebsdatenerfassungsterminal" in der 54 mm schmalen Rollenspalte.
    """
    ergebnis: list[str] = []
    rest = zeile
    while rest and mass.breite_mm(rest, grad_pt) > breite_mm and len(rest) > 1:
        schnitt = len(rest) - 1
        while schnitt > 1 and mass.breite_mm(rest[:schnitt], grad_pt) > breite_mm:
            schnitt -= 1
        ergebnis.append(rest[:schnitt])
        rest = rest[schnitt:]
    ergebnis.append(rest)
    return ergebnis


def umbruch(
    text: str,
    schriftname: str,
    grad_pt: float,
    breite_mm: float,
    fett: bool = False,
) -> list[str]:
    """Simuliert den Zeilenumbruch von PowerPoint.

    Bewusst gierig und ohne Silbentrennung - genau so bricht PowerPoint auch um.
    Eine eigene deutsche Trennung wuerde dort nicht nachvollzogen und die
    Rechnung dadurch erst falsch machen.
    """
    mass = schrift(schriftname, fett)
    text = bereinigen(text)
    zeilen: list[str] = []

    for absatz in text.split(chr(10)):
        absatz = absatz.strip()
        if not absatz:
            zeilen.append("")
            continue

        # (Text, davor ein Leerzeichen?) - nach einem Bindestrich oder
        # Schraegstrich wird ohne Leerzeichen angesetzt.
        stuecke: list[tuple[str, bool]] = []
        for wort in absatz.split():
            for i, teil in enumerate(_teilstuecke(wort)):
                stuecke.append((teil, i == 0))

        aktuell = ""
        for teil, mit_leerzeichen in stuecke:
            trenner = " " if (mit_leerzeichen and aktuell) else ""
            kandidat = aktuell + trenner + teil
            if not aktuell or mass.breite_mm(kandidat, grad_pt) <= breite_mm:
                aktuell = kandidat
            else:
                zeilen.extend(_notumbruch(aktuell, mass, grad_pt, breite_mm))
                aktuell = teil
        zeilen.extend(_notumbruch(aktuell, mass, grad_pt, breite_mm))

    return zeilen


def zeilenzahl(text: str, schriftname: str, grad_pt: float, breite_mm: float,
               fett: bool = False) -> int:
    return len(umbruch(text, schriftname, grad_pt, breite_mm, fett))


def texthoehe_mm(text: str, schriftname: str, grad_pt: float, breite_mm: float,
                 fett: bool = False) -> float:
    return zeilenzahl(text, schriftname, grad_pt, breite_mm, fett) * ci.zeilenhoehe_mm(grad_pt)
