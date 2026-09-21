"""Prueft die fertige Seite, bevor eine Datei entsteht.

Die Rahmenliste beschreibt die Seite vollstaendig - die meisten Fehler lassen
sich daran feststellen, ohne etwas zu rendern. Schlaegt eine dieser Pruefungen
an, wird keine PPTX geschrieben. Lieber eine klare Fehlermeldung als eine
Karte mit abgeschnittenem Text an der Maschine.
"""
from __future__ import annotations

import ci
from rahmen import Bild, Flaeche, Linie, Seite, Text

TOLERANZ = 0.05        # mm
MIN_GRAD_FLIESSTEXT = 10.0


class Befund:
    def __init__(self, regel: str, meldung: str):
        self.regel = regel
        self.meldung = meldung

    def __str__(self) -> str:
        return "[{}] {}".format(self.regel, self.meldung)


# ------------------------------------------------------------------- Kontrast


def _kanal(wert: int) -> float:
    anteil = wert / 255
    return anteil / 12.92 if anteil <= 0.03928 else ((anteil + 0.055) / 1.055) ** 2.4


def _leuchtdichte(hex_wert: str) -> float:
    r, g, b = (int(hex_wert[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _kanal(r) + 0.7152 * _kanal(g) + 0.0722 * _kanal(b)


def kontrast(vorne: str, hinten: str) -> float:
    a, b = _leuchtdichte(vorne), _leuchtdichte(hinten)
    hell, dunkel = (a, b) if a > b else (b, a)
    return (hell + 0.05) / (dunkel + 0.05)


def _grosser_text(r: Text) -> bool:
    """WCAG: ab 18 pt, fett ab 14 pt gilt der mildere Schwellwert 3:1."""
    return r.grad_pt >= 18.0 or (r.fett and r.grad_pt >= 14.0)


# ------------------------------------------------------------------ Geometrie


def _rechteck(r):
    return (r.x, r.y, r.x + r.b, r.y + r.h)


def _ueberlappt(a, b) -> bool:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    return (ax1 < bx2 - TOLERANZ and bx1 < ax2 - TOLERANZ
            and ay1 < by2 - TOLERANZ and by1 < ay2 - TOLERANZ)


def _grund_unter(seite: Seite, r: Text) -> str:
    """Die oberste Farbflaeche unter der Mitte des Textrahmens."""
    mx = r.x + r.b / 2
    my = r.y + max(r.h, 1.0) / 2
    grund = ci.WEISS
    for f in seite.rahmen:
        if not isinstance(f, Flaeche) or not f.fuellung:
            continue
        if f.x - TOLERANZ <= mx <= f.x + f.b + TOLERANZ and \
           f.y - TOLERANZ <= my <= f.y + f.h + TOLERANZ:
            grund = f.fuellung
    return grund


def _linie_schneidet(linie: Linie, rechteck) -> bool:
    """Nur waagrechte und senkrechte Linien - mehr kommt auf der Karte nicht vor."""
    x1, y1, x2, y2 = rechteck
    lx1, lx2 = sorted((linie.x1, linie.x2))
    ly1, ly2 = sorted((linie.y1, linie.y2))
    return (lx1 < x2 - TOLERANZ and x1 < lx2 - TOLERANZ
            and ly1 < y2 - TOLERANZ and y1 < ly2 - TOLERANZ)


# -------------------------------------------------------------------- Regeln


def pruefen(seite: Seite) -> list[Befund]:
    befunde: list[Befund] = []
    flaechen = [r for r in seite.rahmen if isinstance(r, Flaeche)]
    texte = [r for r in seite.rahmen if isinstance(r, Text)]
    linien = [r for r in seite.rahmen if isinstance(r, Linie)]

    # 1 - nichts ragt ueber das Blatt hinaus
    for r in seite.rahmen:
        if isinstance(r, Linie):
            punkte = [(r.x1, r.y1), (r.x2, r.y2)]
        else:
            punkte = [(r.x, r.y), (r.x + r.b, r.y + r.h)]
        for x, y in punkte:
            if x < -TOLERANZ or x > ci.SEITE_B_MM + TOLERANZ or \
               y < -TOLERANZ or y > ci.SEITE_H_MM + TOLERANZ:
                befunde.append(Befund(
                    "seitengrenze",
                    "{} liegt bei ({:.1f}|{:.1f}) ausserhalb des Blattes".format(
                        type(r).__name__, x, y)))

    # 2 - Inhalt haelt den Satzspiegel ein (Kopfband und Logo ausgenommen)
    for r in seite.rahmen:
        if isinstance(r, Linie) or getattr(r, "gruppe", "") == "kopf":
            continue
        if isinstance(r, Bild):
            continue
        if r.x < ci.RAND_MM - TOLERANZ or \
           r.x + r.b > ci.SEITE_B_MM - ci.RAND_MM + TOLERANZ:
            befunde.append(Befund(
                "satzspiegel",
                "{} '{}' von {:.1f} bis {:.1f} mm verlaesst den Satzspiegel".format(
                    type(r).__name__, getattr(r, "gruppe", ""), r.x, r.x + r.b)))

    # 3 - keine zwei Farbflaechen verschiedener Bloecke ueberlappen
    for i, a in enumerate(flaechen):
        for b in flaechen[i + 1:]:
            if a.gruppe == b.gruppe or a.gruppe == "kopf" or b.gruppe == "kopf":
                continue
            if _ueberlappt(_rechteck(a), _rechteck(b)):
                befunde.append(Befund(
                    "ueberlappung",
                    "Flaechen '{}' und '{}' ueberlappen".format(a.gruppe, b.gruppe)))

    # 4 - jeder Text bleibt in der Flaeche seines Blocks
    nach_gruppe: dict[str, Flaeche] = {}
    for f in flaechen:
        if f.gruppe and (f.gruppe not in nach_gruppe or f.b > nach_gruppe[f.gruppe].b):
            nach_gruppe[f.gruppe] = f
    for t in texte:
        kasten = nach_gruppe.get(t.gruppe)
        if kasten is None:
            continue
        # Im Kopfband sitzt der Text ohne das uebliche Innenpolster.
        spielraum = 1.0 if t.gruppe == "kopf" else ci.POLSTER_Y_MM - 1.0
        if t.y + t.h > kasten.y + kasten.h - spielraum:
            befunde.append(Befund(
                "textueberlauf",
                "Text in '{}' reicht bis {:.1f} mm, Kasten endet bei {:.1f} mm".format(
                    t.gruppe, t.y + t.h, kasten.y + kasten.h)))

    # 5 - keine Zeile ist breiter als ihr Rahmen
    import textmass as tm
    for t in texte:
        mass = tm.schrift(t.schrift, t.fett)
        for zeile in t.zeilen:
            if mass.breite_mm(zeile, t.grad_pt) > t.b + TOLERANZ:
                befunde.append(Befund(
                    "zeilenbreite",
                    "Zeile in '{}' ist breiter als ihr Rahmen: '{}'".format(
                        t.gruppe, zeile[:40])))
                break

    # 6 - keine Linie laeuft durch Text
    for linie in linien:
        for t in texte:
            if t.gruppe == "fuss" and linie.gruppe == "fuss":
                continue
            if _linie_schneidet(linie, _rechteck(t)):
                befunde.append(Befund(
                    "linie_durch_text",
                    "Linie in '{}' kreuzt Text in '{}'".format(linie.gruppe, t.gruppe)))

    # 7 - Verzweigungslinien enden an einer Flaeche oder an einer anderen Linie
    enden = []
    for linie in linien:
        if linie.gruppe == "fuss" or linie.staerke_pt < 1.0:
            continue
        enden.append((linie, (linie.x2, linie.y2)))
    for linie, (x, y) in enden:
        trifft = any(
            f.x - 1.0 <= x <= f.x + f.b + 1.0 and f.y - 1.0 <= y <= f.y + f.h + 1.0
            for f in flaechen
        ) or any(
            abs(a.x1 - x) + abs(a.y1 - y) < 1.0 or abs(a.x2 - x) + abs(a.y2 - y) < 1.0
            or (min(a.x1, a.x2) - 1.0 <= x <= max(a.x1, a.x2) + 1.0
                and min(a.y1, a.y2) - 1.0 <= y <= max(a.y1, a.y2) + 1.0)
            for a in linien if a is not linie
        )
        if not trifft:
            befunde.append(Befund(
                "freies_linienende",
                "Linie in '{}' endet frei bei ({:.1f}|{:.1f})".format(
                    linie.gruppe, x, y)))

    # 8 - Schriftgrad und Kontrast
    # Die Untergrenze gilt dem Fliesstext im Ablauf. Eyebrow-Zeile und
    # Fusszeile sind Beschriftungen, keine Arbeitsanweisung - sie duerfen
    # kleiner sein, ohne dass jemand an der Maschine etwas verpasst.
    for t in texte:
        inhaltstext = t.gruppe.startswith("b")
        if inhaltstext and t.grad_pt < MIN_GRAD_FLIESSTEXT - 0.01:
            befunde.append(Befund(
                "schriftgrad",
                "Text in '{}' ist {:.1f} pt - unter der Grenze von {:.0f} pt".format(
                    t.gruppe, t.grad_pt, MIN_GRAD_FLIESSTEXT)))
        grund = _grund_unter(seite, t)
        wert = kontrast(t.farbe, grund)
        schwelle = 3.0 if _grosser_text(t) else 4.5
        if wert < schwelle:
            befunde.append(Befund(
                "kontrast",
                "#{} auf #{} in '{}' erreicht nur {:.2f}:1, noetig {:.1f}:1".format(
                    t.farbe, grund, t.gruppe, wert, schwelle)))

    # 9 - der Inhalt endet vor der Fusszeile
    for r in seite.rahmen:
        if getattr(r, "gruppe", "") in ("fuss", "kopf") or isinstance(r, Linie):
            continue
        unten = r.y + r.h
        if unten > ci.FUSS_LINIE_Y_MM - TOLERANZ:
            befunde.append(Befund(
                "fussbereich",
                "'{}' reicht bis {:.1f} mm und ueberlagert die Fusszeile".format(
                    getattr(r, "gruppe", ""), unten)))

    return befunde
