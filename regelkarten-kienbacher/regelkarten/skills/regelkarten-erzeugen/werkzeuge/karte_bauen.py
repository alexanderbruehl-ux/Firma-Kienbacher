"""Erzeugt aus einer Kartendefinition (JSON) eine Regelkarte.

    python karte_bauen.py karte.json --projekt "D:\\...\\Regelkarten"

Ergebnis je Lauf:
    karten/RK-0xx_kurztitel_r01.pptx    bearbeitbar, jedes Element ein Objekt
    karten/RK-0xx_kurztitel_r01.md      derselbe Inhalt als Text
    karten/RK-0xx_kurztitel_r01.json    die Definition, Grundlage der naechsten Revision
    register/kartenregister.json|.md    fortgeschrieben
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

HIER = Path(__file__).resolve().parent
if str(HIER) not in sys.path:
    sys.path.insert(0, str(HIER))

import ci                      # noqa: E402
import layout                  # noqa: E402
import pruefung                # noqa: E402
import register as reg         # noqa: E402
import textmass as tm          # noqa: E402
from markdown_zwilling import zwilling_schreiben   # noqa: E402
from pptx_schreiben import schreiben as pptx_schreiben   # noqa: E402

ASSETS = HIER.parent / "assets"
LOGO_WEISS = ASSETS / "logo_weiss.png"

# .../Regelkarten/regelkarten/skills/regelkarten-erzeugen/werkzeuge/karte_bauen.py
#     [4]         [3]         [2]    [1]                  [0]
PLUGIN_WURZEL = HIER.parents[2]
NEBEN_PLUGIN = HIER.parents[3]


def projekt_finden(vorgabe: Path | None) -> Path:
    """Findet den Projektordner mit karten/ und register/.

    Ein Kollege ruft /regelkarte irgendwo auf - meist nicht im richtigen
    Ordner. Ohne diese Aufloesung landet die Karte im aktuellen Verzeichnis
    und das Kartenregister spaltet sich in zwei Staende auf. Das faellt
    erst auf, wenn zwei Karten dieselbe ID tragen.
    """
    if vorgabe is not None:
        return vorgabe.resolve()

    aus_umgebung = os.environ.get("REGELKARTEN_PROJEKT")
    if aus_umgebung:
        return Path(aus_umgebung).resolve()

    # Liegt das Plugin im Projektordner (lokale Einbindung), ist dessen
    # Elternordner die richtige Wahl.
    if (NEBEN_PLUGIN / "register").exists() or (NEBEN_PLUGIN / "karten").exists():
        return NEBEN_PLUGIN.resolve()

    return Path.cwd().resolve()


UMLAUTE = {"ä": "ae", "ö": "oe", "ü": "ue", "Ä": "ae", "Ö": "oe", "Ü": "ue",
           "ß": "ss"}


class Abbruch(RuntimeError):
    pass


def kurztitel(titel: str) -> str:
    text = titel.lower()
    for alt, neu in UMLAUTE.items():
        text = text.replace(alt.lower(), neu)
    erlaubt = [z if z.isalnum() else "-" for z in text]
    kurz = "".join(erlaubt)
    while "--" in kurz:
        kurz = kurz.replace("--", "-")
    return kurz.strip("-")[:40]


def revision_nummer(revision: str) -> int:
    ziffern = "".join(z for z in str(revision) if z.isdigit())
    return int(ziffern) if ziffern else 1


def nummerieren(bloecke: list[dict]) -> list[dict]:
    """Nummeriert die Ablaufschritte durch.

    Im JSON steht keine Nummer - sonst muesste sie beim Einfuegen eines
    Schrittes von Hand nachgezogen werden, und genau dort entstehen Fehler.

    Bei nur einem Schritt wird NICHT nummeriert. Eine "1" ohne "2" ordnet
    nichts, und wenn der Titel selbst mit einer Zahl beginnt ("2. Schicht"),
    steht dort sonst "1 2. Schicht".
    """
    anzahl = sum(1 for b in bloecke if b["typ"] == "schritt")
    zaehler = 0
    ergebnis = []
    for block in bloecke:
        block = dict(block)
        if block["typ"] == "schritt" and anzahl > 1:
            zaehler += 1
            block["nummer"] = zaehler
        ergebnis.append(block)
    return ergebnis


def zeichen_pruefen(kopf: dict) -> list[str]:
    """Der Kopf wird in Track gesetzt - die Schrift kennt nicht jedes Zeichen."""
    track = tm.schrift(ci.SCHRIFT_KOPF)
    fehlend = []
    for feld in ("eyebrow", "titel", "untertitel"):
        wert = kopf.get(feld)
        if wert:
            fehlend.extend(track.fehlende_zeichen(tm.bereinigen(wert)))
    return sorted(set(fehlend))


def pflicht_pruefen(daten: dict) -> None:
    if "kopf" not in daten:
        raise Abbruch("Die Definition hat keinen 'kopf' mit Eyebrow und Titel.")
    typen = [b["typ"] for b in daten.get("bloecke", [])]
    if "wer_macht_was" not in typen:
        raise Abbruch(
            "Der Bereich 'Wer macht was?' fehlt. Er ist auf jeder Regelkarte\n"
            "Pflicht - Rollennamen in den Schritten ersetzen ihn nicht.")
    if "abschluss" not in typen:
        raise Abbruch(
            "Das Abschlusskriterium fehlt ('WEITERARBEITEN WENN' bei einer\n"
            "Unterbrechung oder Entscheidung, 'FERTIG WENN' bei einer\n"
            "abgeschlossenen Tätigkeit).")
    entscheidungen = typen.count("entscheidung")
    if entscheidungen > 2:
        raise Abbruch(
            "{} Entscheidungen auf einer Karte. Mehr als zwei sind auf A4 nicht\n"
            "mehr lesbar - den Prozess auf zwei Karten teilen.".format(entscheidungen))


def definition_laden(quelle: Path) -> dict:
    """Laedt die Kartendefinition mit verstaendlichen Fehlermeldungen.

    Wer eine Karte schreibt, ist nicht zwingend Programmierer - ein Traceback
    hilft an dieser Stelle niemandem.
    """
    if not quelle.exists():
        raise Abbruch("Die Kartendefinition gibt es nicht: {}".format(quelle))
    try:
        text = quelle.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raise Abbruch(
            "{} ist nicht UTF-8 kodiert. Die Datei in UTF-8 speichern - "
            "sonst gehen die Umlaute verloren.".format(quelle.name))
    try:
        return json.loads(text)
    except json.JSONDecodeError as fehler:
        raise Abbruch(
            "{} ist kein gültiges JSON.{}"
            "  Zeile {}, Spalte {}: {}{}"
            "  Meist fehlt ein Komma zwischen zwei Blöcken, oder es steht "
            "eines zu viel vor der schließenden Klammer.".format(
                quelle.name, chr(10), fehler.lineno, fehler.colno,
                fehler.msg, chr(10)))


def bauen(quelle: Path, projekt: Path, ohne_logo: bool = False) -> dict:
    daten = definition_laden(quelle)
    if "karte" not in daten:
        raise Abbruch("Der Abschnitt 'karte' mit Revision, Datum und Status fehlt.")
    karte = daten["karte"]
    pflicht_pruefen(daten)

    fehlend = zeichen_pruefen(daten["kopf"])
    if fehlend:
        raise Abbruch(
            "Der Kopfbereich wird in Track gesetzt, und diese Zeichen kennt die\n"
            "Schrift nicht: {}\n"
            "Ersetzen oder umformulieren - sonst steht auf der Karte ein\n"
            "Ersatzkästchen.".format(" ".join(fehlend)))

    registerdatei = projekt / "register" / "kartenregister.json"
    register = reg.laden(registerdatei)

    if not karte.get("id"):
        karte["id"] = reg.naechste_id(register)
    reg.pruefe_id(register, karte["id"], daten["kopf"]["titel"])
    reg.status_pruefen(karte)

    datum = datetime.strptime(karte["datum"], "%Y-%m-%d")
    kopfdaten = {
        "kopf": daten["kopf"],
        "id": karte["id"],
        "revision": karte["revision"],
        "datum_anzeige": datum.strftime("%d.%m.%Y"),
        "status_anzeige": reg.STATUS_ANZEIGE[karte["status"]],
        "verfasser": karte.get("verfasser") or "_______________",
        "pruefer": karte.get("pruefer"),
        "freigeber": karte.get("freigeber"),
    }

    logo = None if ohne_logo else str(LOGO_WEISS)
    if logo and not LOGO_WEISS.exists():
        raise Abbruch(
            "Das Logo fehlt unter {}.\n"
            "Einmal 'python logo_erzeugen.py' ausführen.".format(LOGO_WEISS))

    bloecke = nummerieren(daten["bloecke"])
    seite, lauf = layout.setzen(kopfdaten, bloecke, logo)

    befunde = pruefung.pruefen(seite)
    if befunde:
        text = chr(10).join("  " + str(b) for b in befunde)
        raise Abbruch(
            "Die Karte haelt die Gestaltungsregeln nicht ein. Es wurde keine\n"
            "Datei geschrieben.\n" + text)

    name = "{}_{}_r{:02d}".format(karte["id"], kurztitel(daten["kopf"]["titel"]),
                                  revision_nummer(karte["revision"]))
    ziel = projekt / "karten"
    ziel.mkdir(parents=True, exist_ok=True)

    pptx = pptx_schreiben(seite, ziel / (name + ".pptx"))
    # Die nummerierten Bloecke, nicht die Rohfassung - sonst fehlt im
    # Zwilling die Schrittnummer.
    zwilling_schreiben(dict(daten, bloecke=bloecke), kopfdaten, lauf,
                       ziel / (name + ".md"))
    shutil.copyfile(quelle, ziel / (name + ".json"))

    lauf["datei"] = str(pptx.relative_to(projekt)).replace("\\", "/")
    reg.fortschreiben(register, {
        "id": karte["id"], "titel": daten["kopf"]["titel"],
        "bereich": karte.get("bereich"), "revision": karte["revision"],
        "datum": karte["datum"], "status": karte["status"],
        "verfasser": karte.get("verfasser"), "pruefer": karte.get("pruefer"),
        "freigeber": karte.get("freigeber"),
        "offene_fragen": karte.get("offene_fragen") or [],
    }, lauf)
    reg.schreiben(register, registerdatei)

    lauf["pptx"] = str(pptx)
    lauf["markdown"] = str(ziel / (name + ".md"))
    lauf["id"] = karte["id"]
    return lauf


def main(argv=None) -> int:
    # Windows gibt standardmaessig in cp1252 aus - Umlaute in Fehlermeldungen
    # kaemen dann als Fragezeichen an, und genau die Meldungen muss jemand
    # lesen koennen.
    for strom in (sys.stdout, sys.stderr):
        try:
            strom.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass

    parser = argparse.ArgumentParser(description="Erzeugt eine Kienbacher-Regelkarte.")
    parser.add_argument("quelle", type=Path, help="Kartendefinition als JSON")
    parser.add_argument("--projekt", type=Path, default=None,
                        help="Projektordner mit karten/ und register/ "
                             "(sonst automatisch gefunden)")
    parser.add_argument("--ohne-logo", action="store_true",
                        help="Kopfband ohne Bildmarke (nur zum Prüfen)")
    args = parser.parse_args(argv)

    try:
        projekt = projekt_finden(args.projekt)
        lauf = bauen(args.quelle, projekt, args.ohne_logo)
    except (Abbruch, layout.PasstNicht, reg.RegisterFehler) as fehler:
        print(str(fehler), file=sys.stderr)
        return 1

    print("Karte erzeugt: " + lauf["id"])
    print("  PPTX      " + lauf["pptx"])
    print("  Markdown  " + lauf["markdown"])
    print("  Fließtext {:.0f} pt, Höhe {:.1f} von {:.1f} mm genutzt".format(
        lauf["fliesstext_pt"], lauf["hoehe_genutzt_mm"], lauf["hoehe_verfuegbar_mm"]))
    rest = lauf["hoehe_verfuegbar_mm"] - lauf["hoehe_genutzt_mm"]
    if rest < 10:
        print("  Hinweis: nur noch {:.1f} mm frei - jede Ergänzung sprengt die "
              "Seite.".format(rest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
