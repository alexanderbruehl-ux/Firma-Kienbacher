"""Schreibt den Karteninhalt als Markdown neben die PPTX.

Aus derselben Definition erzeugt, also nie abweichend. Der Zwilling traegt
zusaetzlich, was auf der Karte nichts zu suchen hat: die offenen fachlichen
Fragen und die Messwerte des Laufs.
"""
from __future__ import annotations

from pathlib import Path


def _abschnitt(zeilen: list[str], block: dict) -> None:
    typ = block["typ"]

    if typ == "anlass":
        zeilen += ["## " + block.get("label", "WENN"), "", block["text"], ""]

    elif typ == "schritt":
        kopf = "{}. **{}**".format(block.get("nummer", "-"), block["titel"])
        if block.get("rolle"):
            kopf += "  _({})_".format(block["rolle"])
        zeilen += [kopf, ""]
        if block.get("text"):
            zeilen += ["   " + block["text"], ""]

    elif typ == "entscheidung":
        zeilen += ["## Entscheidung: " + block["frage"], ""]
        for zweig in ("ja", "nein"):
            teil = block[zweig]
            zeilen.append("- **{} - {}:** {}".format(
                teil.get("label", zweig.upper()), teil.get("titel", ""),
                teil.get("text", "")))
        zeilen.append("")

    elif typ == "hinweis":
        marke = "**!**" if block.get("gewicht") == "stark" else ""
        zeilen += ["> {} **{}** {}".format(marke, block.get("titel", "Hinweis"),
                                           block["text"]), ""]

    elif typ == "zwei_spalten":
        for seite in ("links", "rechts"):
            teil = block[seite]
            zeilen += ["- **{}:** {}".format(teil.get("titel", ""),
                                             teil.get("text", ""))]
        zeilen.append("")

    elif typ == "wer_macht_was":
        zeilen += ["## " + block.get("titel", "WER MACHT WAS?"), "",
                   "| Wer? | Was macht diese Rolle? |", "|---|---|"]
        for z in block["zeilen"]:
            zeilen.append("| {} | {} |".format(z["rolle"], z["aufgabe"]))
        zeilen.append("")

    elif typ == "abschluss":
        zeilen += ["## " + block["label"], ""]
        for k in block["kriterien"]:
            zeilen.append("- " + k)
        zeilen.append("")


def zwilling_schreiben(daten: dict, kopfdaten: dict, lauf: dict, ziel: Path) -> Path:
    karte = daten["karte"]
    kopf = daten["kopf"]

    zeilen = [
        "# {} - {}".format(karte["id"], kopf["titel"]),
        "",
        "Revision {} · {} · Status: {}".format(
            karte["revision"], kopfdaten["datum_anzeige"],
            kopfdaten["status_anzeige"]),
        "",
        "| | |",
        "|---|---|",
        "| Bereich | {} |".format(karte.get("bereich") or "-"),
        "| Verfasser | {} |".format(karte.get("verfasser") or "-"),
        "| Prüfer | {} |".format(karte.get("pruefer") or "_offen_"),
        "| Freigeber | {} |".format(karte.get("freigeber") or "_offen_"),
        "",
    ]
    if kopf.get("untertitel"):
        zeilen += ["_{}_".format(kopf["untertitel"]), ""]

    for block in daten["bloecke"]:
        _abschnitt(zeilen, block)

    offene = karte.get("offene_fragen") or []
    if offene:
        zeilen += [
            "## Offene fachliche Fragen",
            "",
            "Diese Punkte sind **nicht bestätigt** und stehen deshalb nicht auf",
            "der Karte. Vor einer Freigabe zu klären.",
            "",
        ]
        for frage in offene:
            zeilen.append("- " + frage)
        zeilen.append("")

    rest = lauf["hoehe_verfuegbar_mm"] - lauf["hoehe_genutzt_mm"]
    zeilen += [
        "## Erzeugung",
        "",
        "- Fließtext {:.0f} pt (Stufe {}), Blockabstand {:.1f} mm".format(
            lauf["fliesstext_pt"], lauf["stufe"] + 1, lauf["blockabstand_mm"]),
        "- Höhe genutzt {:.1f} von {:.1f} mm, frei {:.1f} mm".format(
            lauf["hoehe_genutzt_mm"], lauf["hoehe_verfuegbar_mm"], rest),
        "- Kopfbereich in der Schrift **Track**. Sie liegt im Plugin unter",
        "  `skills/regelkarten-erzeugen/assets/Track.ttf` und ist vor dem",
        "  Bearbeiten zu installieren. Fehlt sie, wird der Titel in Arial",
        "  dargestellt - das Layout bleibt gültig.",
        "",
    ]
    if rest < 10:
        zeilen += [
            "> Nur noch {:.1f} mm frei. Jede Textergänzung sprengt die Seite -".format(rest),
            "> dann muss gekürzt oder der Prozess geteilt werden.",
            "",
        ]

    ziel.parent.mkdir(parents=True, exist_ok=True)
    ziel.write_text(chr(10).join(zeilen), encoding="utf-8")
    return ziel
