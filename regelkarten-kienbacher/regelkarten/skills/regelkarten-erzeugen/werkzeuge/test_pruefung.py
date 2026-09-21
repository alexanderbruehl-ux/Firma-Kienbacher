"""Regressionstest: Die Pruefung muss die Fehler finden, die eine Karte
unbrauchbar machen - und die fehlerfreie Karte in Ruhe lassen.

    python test_pruefung.py

Ohne Testrahmen, damit er auf jedem Rechner laeuft, auf dem der Generator
laeuft. Rueckgabewert 0 heisst bestanden.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HIER = Path(__file__).resolve().parent
if str(HIER) not in sys.path:
    sys.path.insert(0, str(HIER))

import ci                     # noqa: E402
import karte_bauen as kb      # noqa: E402
import layout                 # noqa: E402
import pruefung               # noqa: E402
import textmass as tm         # noqa: E402
from rahmen import Flaeche, Linie, Seite, Text   # noqa: E402


def text(x, y, b, inhalt, grad=11.0, farbe=ci.TEXT, gruppe="b0", fett=False):
    return Text(x=x, y=y, b=b, inhalt=inhalt,
                zeilen=tm.umbruch(inhalt, "Arial", grad, b, fett),
                schrift="Arial", grad_pt=grad, fett=fett, farbe=farbe,
                gruppe=gruppe)


def defekte_seiten():
    """Je ein Fall, der auf einer gedruckten Karte wirklich schadet."""
    faelle = {}

    s = Seite()
    s.dazu(Flaeche(10, 50, 190, 30, ci.FLAECHE_BLAU_1, gruppe="b0"),
           Flaeche(10, 70, 190, 30, ci.FLAECHE_GRAU_1, gruppe="b1"))
    faelle["ueberlappung"] = ("zwei Bloecke ueberlappen", s)

    # Genau der Fehler der Bestandskarten: der Ast endet 4 mm vor dem Kasten.
    s = Seite()
    s.dazu(Flaeche(10, 100, 91.5, 30, ci.FLAECHE_BLAU_2, gruppe="b0"),
           Linie(55.75, 80, 55.75, 96.0, ci.CI_BLAU, 2.25, "b0"))
    faelle["freies_linienende"] = ("Verzweigungslinie endet im Nichts", s)

    s = Seite()
    s.dazu(Flaeche(10, 50, 190, 14, ci.FLAECHE_BLAU_1, gruppe="b0"),
           text(14.5, 53, 181,
                "Ein Text, der viel zu lang ist fuer diesen flachen Kasten und "
                "deshalb ueber die Unterkante hinauslaeuft, was auf der "
                "gedruckten Karte niemand mehr lesen kann."))
    faelle["textueberlauf"] = ("Text laeuft aus seinem Kasten", s)

    # CI-Grau als Textfarbe erreicht auf Weiss nur 4,18:1.
    s = Seite()
    s.dazu(text(10, 50, 190, "Grauer Text auf weissem Grund", farbe=ci.CI_GRAU))
    faelle["kontrast"] = ("Textfarbe zu schwach", s)

    s = Seite()
    s.dazu(text(10, 50, 190, "Zu kleiner Fliesstext", grad=8.5))
    faelle["schriftgrad"] = ("Fliesstext unter 10 pt", s)

    s = Seite()
    s.dazu(Flaeche(4, 50, 200, 20, ci.FLAECHE_BLAU_1, gruppe="b0"))
    faelle["satzspiegel"] = ("Block ragt in den Aussenrand", s)

    return faelle


def beispielseite():
    quelle = HIER.parent / "beispiele" / "werkzeugbruch.json"
    d = json.loads(quelle.read_text(encoding="utf-8"))
    kopf = {
        "kopf": d["kopf"], "id": "RK-010", "revision": "0.1",
        "datum_anzeige": "16.09.2026", "status_anzeige": "Entwurf",
        "verfasser": "M. Tillian", "pruefer": None, "freigeber": None,
    }
    logo = str(kb.LOGO_WEISS) if kb.LOGO_WEISS.exists() else None
    seite, _ = layout.setzen(kopf, kb.nummerieren(d["bloecke"]), logo)
    return seite


def main() -> int:
    fehler = 0

    for regel, (beschreibung, seite) in defekte_seiten().items():
        befunde = pruefung.pruefen(seite)
        gefunden = {b.regel for b in befunde}
        if regel in gefunden:
            print("  ok       {:20s} {}".format(regel, beschreibung))
        else:
            print("  FEHLER   {:20s} nicht erkannt: {}".format(regel, beschreibung))
            fehler += 1

    befunde = pruefung.pruefen(beispielseite())
    if befunde:
        print("  FEHLER   Beispielkarte meldet Befunde:")
        for b in befunde:
            print("             " + str(b))
        fehler += 1
    else:
        print("  ok       beispielkarte        laeuft ohne Befund durch")

    # Der Umbruch darf nie eine Zeile liefern, die breiter ist als ihre Spalte.
    proben = [
        ("Betriebsdatenerfassungsterminal", 11.0, 25.0),
        ("Erststueckfreigabe-Pruefung durch PQB/Teamleader", 10.0, 45.0),
        ("Auftragsmenge auf dem Auftrag lesen und in BARI pruefen.", 11.0, 82.5),
    ]
    mass = tm.schrift("Arial")
    for inhalt, grad, breite in proben:
        zu_breit = [z for z in tm.umbruch(inhalt, "Arial", grad, breite)
                    if mass.breite_mm(z, grad) > breite + 0.01]
        if zu_breit:
            print("  FEHLER   umbruch              zu breite Zeile: " + zu_breit[0])
            fehler += 1
    if not fehler:
        print("  ok       umbruch              keine Zeile breiter als ihre Spalte")

    print()
    print("bestanden" if fehler == 0 else "{} Fehler".format(fehler))
    return 1 if fehler else 0


if __name__ == "__main__":
    raise SystemExit(main())
