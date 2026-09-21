"""Kienbacher-CI, Raster und Schriftgrade der Regelkarte.

Einzige Quelle dieser Werte im Code. Die lesbare Fassung mit Begruendung steht
in ../../regelkarten-design/references/raster.md - wird hier etwas geaendert,
gehoert es auch dorthin.
"""
from __future__ import annotations

# ---------------------------------------------------------------- Masseinheiten

EMU_JE_MM = 36000
PT_JE_MM = 72 / 25.4


def mm(wert: float) -> int:
    """Millimeter -> EMU (English Metric Units), die Einheit von OOXML."""
    return int(round(wert * EMU_JE_MM))


def mm_aus_pt(punkt: float) -> float:
    return punkt / PT_JE_MM


def pt_aus_mm(millimeter: float) -> float:
    return millimeter * PT_JE_MM


# ---------------------------------------------------------------------- Seite

SEITE_B_MM = 210.0
SEITE_H_MM = 297.0

RAND_MM = 10.0
SATZ_X_MM = RAND_MM
SATZ_B_MM = SEITE_B_MM - 2 * RAND_MM          # 190.0

KOPF_H_MM = 32.0        # Mindesthoehe; das Band waechst mit dem Titel
KOPF_H_MAX_MM = 44.0    # darueber ist der Titel zu lang, nicht das Band zu klein
INHALT_Y_MM = 40.0
FUSS_LINIE_Y_MM = 278.0
FUSS_Y_MM = 280.0

# Der Raum, in dem der Ablauf Platz finden muss.
INHALT_H_MM = FUSS_LINIE_Y_MM - INHALT_Y_MM - 6.0   # 232.0

SPALTE_L_X_MM = SATZ_X_MM                      # 10.0
SPALTE_B_MM = 91.5
SPALTE_R_X_MM = 108.5
SPALTE_L_MITTE_MM = SPALTE_L_X_MM + SPALTE_B_MM / 2     # 55.75
SPALTE_R_MITTE_MM = SPALTE_R_X_MM + SPALTE_B_MM / 2     # 154.25
SEITE_MITTE_MM = SEITE_B_MM / 2                          # 105.0

ROLLE_X_MM = 14.5
ROLLE_B_MM = 54.0
AUFGABE_X_MM = 70.0
AUFGABE_B_MM = 125.5

# --------------------------------------------------------------- Abstaende

POLSTER_X_MM = 4.5      # Innenabstand Farbflaeche -> Text, links/rechts
POLSTER_Y_MM = 3.5      # dto. oben/unten
ABSTAND_BLOCK_MM = 5.0
ABSTAND_ABSCHNITT_MM = 8.0
ABSTAND_TITEL_TEXT_MM = 1.8
ECKRADIUS_MM = 3.0

LOGO_H_MM = 12.0        # Bildmarke oben rechts auf der Eyebrow-Zeile
LOGO_Y_MM = 4.5
LOGO_PLATZ_MM = 14.0    # Breite, die der Titel dafuer freihaelt

# ----------------------------------------------------------------- Farben
# Ausschliesslich Kienbacher-CI: Blau #0079A7, Grau #7B7C7E und Toene daraus.
# Die Kontrastwerte in den Kommentaren sind nachgerechnet (WCAG 2.1) und werden
# von pruefung.py bei jedem Lauf erneut geprueft.

CI_BLAU = "0079A7"          # Kopfband, Rahmen, Linien, JA-Chip
CI_GRAU = "7B7C7E"          # Flaechen und Rahmen - nie fuer Text
WEISS = "FFFFFF"

TEXT = "00435C"             # aller Text auf hellem Grund; 10.73:1 auf Weiss
TEXT_INVERS = WEISS         # auf Blau 4.89:1, auf CHIP_GRAU 6.60:1

FLAECHE_BLAU_1 = "E6F2F6"   # normaler Ablaufschritt
FLAECHE_BLAU_2 = "D9EBF2"   # JA-Zweig, hervorgehobener Schritt
FLAECHE_GRAU_1 = "F2F2F2"   # neutrales Panel, "Wer macht was?"
FLAECHE_GRAU_2 = "EBEBEC"

CHIP_GRAU = "5C5D5E"        # NEIN- und AUSNAHME-Chip, weisse Schrift
FUSS_TEXT = "5C5D5F"        # 6.59:1 - CI_GRAU waere mit 4.18:1 zu schwach
LINIE_LEICHT = "D1D1D2"

WARNUNG = "B22F22"          # nur echter Sicherheitshinweis, sonst nie

# ------------------------------------------------------------- Schriftgrade

SCHRIFT_KOPF = "Track"      # nur Eyebrow und Titel - kein Fettschnitt vorhanden
SCHRIFT_TEXT = "Arial"      # alles Uebrige, auf jedem Arbeitsplatz vorhanden

GRAD_EYEBROW = 9.0
GRAD_TITEL_STUFEN = (24.0, 22.0, 20.0)
GRAD_UNTERTITEL = 11.0

# Stufen der Fallback-Kaskade: (Abschnittstitel, Fliesstext, Rolle, Chip)
GRAD_STUFEN = (
    (14.0, 12.0, 11.0, 14.0),
    (13.0, 11.0, 10.5, 13.0),
    (12.0, 10.0, 10.0, 12.0),
)
GRAD_FUSS = 8.0

# Absolute Zeilenhoehe als Vielfaches des Schriftgrads. Wird in OOXML als
# spcPts gesetzt, also als fester Punktwert - damit haengt die Hoehe eines
# Blocks NICHT von der Schrift ab, die auf dem oeffnenden Rechner installiert
# ist. Genau daran zerbrechen solche Karten sonst auf einem fremden PC.
ZEILENFAKTOR = 1.30

# Gemessene Breiten werden damit multipliziert. Deckt GPOS-Kerning, das wir
# nicht auswerten, Hinting-Rundungen und die Frage ab, ob PowerPoint das
# letzte Leerzeichen einer Zeile mitrechnet.
SICHERHEIT = 1.02


def zeilenhoehe_mm(grad_pt: float) -> float:
    return mm_aus_pt(grad_pt * ZEILENFAKTOR)


def eckradius_adj(breite_mm: float, hoehe_mm: float) -> float:
    """Adjust-Wert fuer roundRect, so dass der Eckradius absolut konstant bleibt.

    PowerPoint rechnet adj relativ zur kuerzeren Seite. Ohne Umrechnung haetten
    ein flaches Band und ein hoher Kasten sichtbar verschiedene Rundungen.
    Rueckgabe als Anteil (0..0.5), wie python-pptx ihn erwartet.
    """
    kurz = max(min(breite_mm, hoehe_mm), 0.1)
    return max(0.0, min(0.5, ECKRADIUS_MM / kurz))
