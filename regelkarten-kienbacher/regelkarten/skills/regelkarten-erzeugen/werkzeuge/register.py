"""Kartenregister: vergibt IDs, fuehrt Revisionen und haelt den Freigabestand.

Master ist eine JSON-Datei. Daneben wird bei jedem Lauf eine Markdown-Fassung
geschrieben, die man ohne Werkzeug lesen kann - Einbahnstrasse, damit niemand
in der Markdown-Datei editiert und es beim naechsten Lauf verliert.
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

STATUS_ANZEIGE = {
    "entwurf": "Entwurf",
    "in_pruefung": "in Prüfung",
    "freigegeben": "freigegeben",
    "zurueckgezogen": "zurückgezogen",
    "bestand": "Bestand",
}

# RK-001 bis RK-006 sind gesperrt: Aus den Versuchskarten ist belegt, dass
# RK-007 bis RK-009 vergeben wurden. Ob die Nummern davor benutzt sind, ist
# nicht geklaert - also werden sie nicht neu vergeben.
GESPERRT = {"RK-{:03d}".format(n) for n in range(1, 7)}

VORBELEGT = [
    {"id": "RK-007", "titel": "Ist die Produktion fertig?",
     "bereich": "PRODUKTION", "revision": "0.8", "datum": "2026-09-14",
     "status": "bestand", "verfasser": None, "pruefer": None, "freigeber": None,
     "bemerkung": "Versuchskarte, gruene Farbwelt, vor Umstellung auf das CI"},
    {"id": "RK-008", "titel": "Was mache ich, wenn Material fehlt?",
     "bereich": "PRODUKTION", "revision": "0.1", "datum": "2026-09-14",
     "status": "bestand", "verfasser": None, "pruefer": None, "freigeber": None,
     "bemerkung": "Versuchskarte, gruene Farbwelt, vor Umstellung auf das CI"},
    {"id": "RK-009", "titel": "Was mache ich bei einer Maschinenstörung?",
     "bereich": "PRODUKTION", "revision": "0.1", "datum": "2026-09-14",
     "status": "bestand", "verfasser": None, "pruefer": None, "freigeber": None,
     "bemerkung": "Versuchskarte, gruene Farbwelt, vor Umstellung auf das CI"},
]


class RegisterFehler(RuntimeError):
    pass


def _leer() -> dict:
    return {"schema_version": 1, "karten": list(VORBELEGT)}


def laden(pfad: Path) -> dict:
    if not pfad.exists():
        return _leer()
    return json.loads(pfad.read_text(encoding="utf-8"))


def naechste_id(register: dict) -> str:
    belegt = {k["id"] for k in register["karten"]} | GESPERRT
    nummer = 1
    while "RK-{:03d}".format(nummer) in belegt:
        nummer += 1
    return "RK-{:03d}".format(nummer)


def eintrag(register: dict, karten_id: str) -> dict | None:
    for k in register["karten"]:
        if k["id"] == karten_id:
            return k
    return None


def karte_mit_titel(register: dict, titel: str) -> dict | None:
    """Sucht eine bereits eingetragene Karte mit demselben Titel."""
    schlank = " ".join(titel.lower().split())
    for k in register["karten"]:
        if " ".join(str(k["titel"]).lower().split()) == schlank:
            return k
    return None


def pruefe_id(register: dict, karten_id: str, titel: str) -> None:
    if karten_id in GESPERRT:
        raise RegisterFehler(
            "{} ist gesperrt. RK-001 bis RK-006 sind nicht geklärt und werden "
            "nicht neu vergeben. Freie ID wäre {}.".format(
                karten_id, naechste_id(register)))
    vorhanden = eintrag(register, karten_id)
    if vorhanden and vorhanden["titel"] != titel:
        raise RegisterFehler(
            "{} ist bereits vergeben an '{}'. Für eine neue Karte "
            "{} verwenden.".format(karten_id, vorhanden["titel"],
                                   naechste_id(register)))

    # Zweimal dieselbe Regel unter verschiedenen IDs ist schlimmer als gar
    # keine Karte: In der Halle haengen dann zwei Blaetter, und niemand weiss,
    # welches gilt. Passiert leicht, wenn jemand den Generator zweimal laufen
    # laesst, ohne die ID einzutragen.
    doppelt = karte_mit_titel(register, titel)
    if doppelt and doppelt["id"] != karten_id:
        raise RegisterFehler(
            "Zu '{}' gibt es bereits die Karte {}.{}"
            "  Soll das eine neue Fassung werden, trag '{}' als id ein und "
            "erhöhe die Revision.{}"
            "  Soll es wirklich eine zweite, eigenständige Karte sein, "
            "ändere den Titel - sonst hängen zwei Blätter mit derselben "
            "Überschrift an der Maschine.".format(
                titel, doppelt["id"], chr(10), doppelt["id"], chr(10)))


def fortschreiben(register: dict, karte: dict, lauf: dict) -> dict:
    """Traegt die Karte ein oder erhoeht ihre Revision."""
    vorhanden = eintrag(register, karte["id"])
    neu = {
        "id": karte["id"],
        "titel": karte["titel"],
        "bereich": karte.get("bereich"),
        "revision": karte["revision"],
        "datum": karte["datum"],
        "status": karte["status"],
        "verfasser": karte.get("verfasser"),
        "pruefer": karte.get("pruefer"),
        "freigeber": karte.get("freigeber"),
        "offene_fragen": len(karte.get("offene_fragen") or []),
        "datei": lauf.get("datei"),
        "erzeugt_am": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "fliesstext_pt": lauf.get("fliesstext_pt"),
        "hoehe_genutzt_mm": lauf.get("hoehe_genutzt_mm"),
        "hoehe_verfuegbar_mm": lauf.get("hoehe_verfuegbar_mm"),
    }
    if vorhanden:
        historie = vorhanden.get("historie", [])
        ohne = {k: v for k, v in vorhanden.items() if k != "historie"}
        historie.append(ohne)
        neu["historie"] = historie
        register["karten"] = [neu if k["id"] == karte["id"] else k
                              for k in register["karten"]]
    else:
        neu["historie"] = []
        register["karten"].append(neu)
    register["karten"].sort(key=lambda k: k["id"])
    return register


def status_pruefen(karte: dict) -> None:
    status = karte["status"]
    if status not in STATUS_ANZEIGE:
        raise RegisterFehler("Unbekannter Status: " + str(status))
    if status == "freigegeben":
        namen = {"pruefer": "Prüfer", "freigeber": "Freigeber"}
        fehlend = [namen[n] for n in namen if not karte.get(n)]
        if fehlend:
            raise RegisterFehler(
                "Status 'freigegeben' verlangt " + " und ".join(fehlend) + ".")
        if karte.get("offene_fragen"):
            raise RegisterFehler(
                "Status 'freigegeben' bei {} offenen fachlichen Fragen ist nicht "
                "zulässig. Erst klären, dann freigeben.".format(
                    len(karte["offene_fragen"])))


def schreiben(register: dict, pfad: Path) -> None:
    pfad.parent.mkdir(parents=True, exist_ok=True)
    pfad.write_text(json.dumps(register, indent=2, ensure_ascii=False) + chr(10),
                    encoding="utf-8")
    _markdown_schreiben(register, pfad.with_suffix(".md"))


def _markdown_schreiben(register: dict, pfad: Path) -> None:
    zeilen = [
        "# Kartenregister",
        "",
        "Erzeugt aus `kartenregister.json`. **Nicht von Hand ändern** - die Datei",
        "wird bei jedem Kartenlauf neu geschrieben.",
        "",
        "RK-001 bis RK-006 sind gesperrt: ob sie vergeben sind, ist nicht geklärt.",
        "",
        "| ID | Titel | Bereich | Rev. | Datum | Status | Verfasser | Prüfer | Freigeber | Offen |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for k in register["karten"]:
        zeilen.append("| {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(
            k["id"], k["titel"], k.get("bereich") or "-", k["revision"],
            k["datum"], STATUS_ANZEIGE.get(k["status"], k["status"]),
            k.get("verfasser") or "-", k.get("pruefer") or "-",
            k.get("freigeber") or "-", k.get("offene_fragen") or 0))
    pfad.write_text(chr(10).join(zeilen) + chr(10), encoding="utf-8")
