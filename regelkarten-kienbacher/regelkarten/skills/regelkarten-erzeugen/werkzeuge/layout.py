"""Setzt die Bloecke einer Regelkarte auf die Seite.

Grundsatz: Jeder Block baut sich selbst ab einer uebergebenen Oberkante, und
seine Hoehe wird aus den tatsaechlich gebauten Rahmen abgelesen - nicht getrennt
geschaetzt. So koennen Messung und Darstellung nicht auseinanderlaufen.
"""
from __future__ import annotations

import ci
import textmass as tm
from rahmen import Bild, Flaeche, Linie, Seite, Text


class Grade:
    """Die Schriftgrade einer Stufe der Fallback-Kaskade."""

    def __init__(self, stufe: int):
        self.stufe = stufe
        titel, text, rolle, chip = ci.GRAD_STUFEN[stufe]
        self.titel = titel
        self.text = text
        self.rolle = rolle
        self.chip = chip


class PasstNicht(RuntimeError):
    """Die Karte laesst sich auf einer A4-Seite nicht lesbar unterbringen."""

    def __init__(self, meldung, ueberschuss_mm, groesste):
        super().__init__(meldung)
        self.ueberschuss_mm = ueberschuss_mm
        self.groesste = groesste


# ------------------------------------------------------------------ Bausteine


def _text(x, y, b, inhalt, grad, fett=False, farbe=ci.TEXT,
          schrift=ci.SCHRIFT_TEXT, sperrung=0.0, ausrichtung="links", gruppe=""):
    return Text(
        x=x, y=y, b=b,
        inhalt=tm.bereinigen(inhalt),
        zeilen=tm.umbruch(inhalt, schrift, grad, b, fett),
        schrift=schrift, grad_pt=grad, fett=fett, farbe=farbe,
        sperrung=sperrung, ausrichtung=ausrichtung, gruppe=gruppe,
    )


def _kasten(x, y, b, titel=None, inhalt=None, g=None, fuellung=None, rand=None,
            randstaerke=0.0, nummer=None, rolle=None, chip=None,
            kantenmarke=None, gruppe=""):
    """Eine Farbflaeche mit darueberliegenden, eigenstaendigen Textrahmen.

    Der Text liegt bewusst nicht in der Flaeche selbst. So bleibt jeder Absatz
    ein eigenes verschiebbares Objekt, und PowerPoint kann die Flaeche nicht
    automatisch auf den Text schrumpfen.
    """
    innen_x = x + ci.POLSTER_X_MM
    innen_b = b - 2 * ci.POLSTER_X_MM
    lauf = y + ci.POLSTER_Y_MM
    texte = []
    chipflaeche = None

    if chip is not None:
        beschriftung, chipfarbe = chip
        chip_b, chip_h = 20.0, 7.0
        chipflaeche = Flaeche(innen_x, lauf, chip_b, chip_h, chipfarbe,
                              gerundet=True, gruppe=gruppe)
        texte.append(_text(innen_x, lauf + (chip_h - ci.zeilenhoehe_mm(g.chip)) / 2,
                           chip_b, beschriftung, g.chip, fett=True,
                           farbe=ci.TEXT_INVERS, ausrichtung="mitte", gruppe=gruppe))
        lauf += chip_h + 2.0

    kopfzeile = " ".join(
        t for t in ((str(nummer) if nummer is not None else None), titel) if t
    )
    if kopfzeile:
        # Die ausfuehrende Rolle steht rechts auf der Titelzeile, nicht darunter.
        # Das spart je Schritt eine Zeile - bei fuenf Schritten rund 25 mm, und
        # genau daran scheitert eine Karte sonst an der Seitenhoehe.
        rollen_b = 48.0 if rolle else 0.0
        titel_b = innen_b - (rollen_b + 3.0 if rolle else 0.0)
        kopf = _text(innen_x, lauf, titel_b, kopfzeile, g.titel, fett=True,
                     gruppe=gruppe)
        texte.append(kopf)
        hoehe_zeile = kopf.h
        if rolle:
            rt = _text(innen_x + innen_b - rollen_b, lauf, rollen_b, rolle,
                       g.rolle, fett=True, ausrichtung="rechts", gruppe=gruppe)
            texte.append(rt)
            hoehe_zeile = max(hoehe_zeile, rt.h)
        lauf += hoehe_zeile + ci.ABSTAND_TITEL_TEXT_MM
    elif rolle:
        t = _text(innen_x, lauf, innen_b, rolle, g.rolle, fett=True, gruppe=gruppe)
        texte.append(t)
        lauf += t.h + 0.8

    if inhalt:
        t = _text(innen_x, lauf, innen_b, inhalt, g.text, gruppe=gruppe)
        texte.append(t)
        lauf += t.h

    hoehe = lauf - y + ci.POLSTER_Y_MM
    flaeche = Flaeche(x, y, b, hoehe, fuellung, rand, randstaerke,
                      gerundet=True, gruppe=gruppe)

    ergebnis = [flaeche]
    if kantenmarke:
        # Schmale Marke an der linken Kante. Sie traegt die Unterscheidung
        # auch dann, wenn die Karte schwarz-weiss kopiert wird.
        ergebnis.append(Flaeche(x, y + 1.0, 3.0, hoehe - 2.0, kantenmarke,
                                gerundet=False, gruppe=gruppe))
    if chipflaeche is not None:
        ergebnis.append(chipflaeche)
    ergebnis.extend(texte)
    return ergebnis


def _hoehe_von(rahmen, y0):
    unten = y0
    for r in rahmen:
        if isinstance(r, Linie):
            unten = max(unten, r.y1, r.y2)
        else:
            unten = max(unten, r.y + r.h)
    return unten - y0


def _auf_hoehe_ziehen(satz, hoehe):
    """Zieht Flaeche und Kantenmarke eines Kastens auf eine Zielhoehe."""
    satz[0].h = hoehe
    for r in satz[1:]:
        if isinstance(r, Flaeche) and not r.gerundet:
            r.h = hoehe - 2.0


# -------------------------------------------------------------------- Bloecke


def bau_anlass(block, g, y, gruppe):
    return _kasten(
        ci.SATZ_X_MM, y, ci.SATZ_B_MM,
        titel=block.get("label", "WENN"), inhalt=block["text"], g=g,
        fuellung=ci.FLAECHE_BLAU_1, rand=ci.CI_BLAU, randstaerke=0.75, gruppe=gruppe,
    )


def bau_schritt(block, g, y, gruppe):
    return _kasten(
        ci.SATZ_X_MM, y, ci.SATZ_B_MM,
        titel=block["titel"], inhalt=block.get("text"), g=g,
        fuellung=ci.FLAECHE_GRAU_1, nummer=block.get("nummer"),
        rolle=block.get("rolle"), gruppe=gruppe,
    )


def bau_hinweis(block, g, y, gruppe):
    stark = block.get("gewicht") == "stark"
    return _kasten(
        ci.SATZ_X_MM, y, ci.SATZ_B_MM,
        titel=block.get("titel"), inhalt=block["text"], g=g,
        fuellung=ci.WEISS if stark else ci.FLAECHE_BLAU_1,
        rand=ci.CI_BLAU, randstaerke=2.25 if stark else 0.75, gruppe=gruppe,
    )


def bau_entscheidung(block, g, y, gruppe):
    rahmen = []
    frage = _text(ci.SATZ_X_MM, y, ci.SATZ_B_MM, block["frage"], g.titel,
                  fett=True, gruppe=gruppe)
    rahmen.append(frage)

    y_stamm = y + frage.h + 2.0
    y_quer = y_stamm + 5.0
    y_boxen = y_quer + 5.0

    ja = block["ja"]
    nein = block["nein"]

    links = _kasten(
        ci.SPALTE_L_X_MM, y_boxen, ci.SPALTE_B_MM,
        titel=ja.get("titel"), inhalt=ja.get("text"), g=g,
        fuellung=ci.FLAECHE_BLAU_2, rand=ci.CI_BLAU, randstaerke=2.25,
        chip=(ja.get("label", "JA"), ci.CI_BLAU), gruppe=gruppe + "ja",
    )
    rechts = _kasten(
        ci.SPALTE_R_X_MM, y_boxen, ci.SPALTE_B_MM,
        titel=nein.get("titel"), inhalt=nein.get("text"), g=g,
        fuellung=ci.WEISS, rand=ci.CI_GRAU, randstaerke=1.5,
        chip=(nein.get("label", "NEIN"), ci.CHIP_GRAU),
        kantenmarke=ci.CI_GRAU, gruppe=gruppe + "nein",
    )

    # Beide Kaesten auf die gleiche Hoehe, damit die Aeste sauber enden
    # und die Zweige optisch gleichwertig sind.
    hoehe = max(links[0].h, rechts[0].h)
    _auf_hoehe_ziehen(links, hoehe)
    _auf_hoehe_ziehen(rechts, hoehe)

    rahmen.extend(links)
    rahmen.extend(rechts)

    # Vier Linien. Jede beginnt und endet an einem Element - keine frei
    # endenden Stuecke. Genau das ist der Fehler der Bestandskarten.
    rahmen.extend([
        Linie(ci.SEITE_MITTE_MM, y_stamm, ci.SEITE_MITTE_MM, y_quer,
              ci.CI_BLAU, 1.5, gruppe),
        Linie(ci.SPALTE_L_MITTE_MM, y_quer, ci.SPALTE_R_MITTE_MM, y_quer,
              ci.CI_BLAU, 1.5, gruppe),
        Linie(ci.SPALTE_L_MITTE_MM, y_quer, ci.SPALTE_L_MITTE_MM, y_boxen,
              ci.CI_BLAU, 2.25, gruppe),
        Linie(ci.SPALTE_R_MITTE_MM, y_quer, ci.SPALTE_R_MITTE_MM, y_boxen,
              ci.CI_GRAU, 1.0, gruppe),
    ])
    return rahmen


def bau_zwei_spalten(block, g, y, gruppe):
    links = _kasten(
        ci.SPALTE_L_X_MM, y, ci.SPALTE_B_MM,
        titel=block["links"].get("titel"), inhalt=block["links"].get("text"), g=g,
        fuellung=ci.FLAECHE_BLAU_1, rand=ci.CI_BLAU, randstaerke=1.0,
        gruppe=gruppe + "l",
    )
    rechts = _kasten(
        ci.SPALTE_R_X_MM, y, ci.SPALTE_B_MM,
        titel=block["rechts"].get("titel"), inhalt=block["rechts"].get("text"), g=g,
        fuellung=ci.FLAECHE_BLAU_1, rand=ci.CI_BLAU, randstaerke=1.0,
        gruppe=gruppe + "r",
    )
    hoehe = max(links[0].h, rechts[0].h)
    _auf_hoehe_ziehen(links, hoehe)
    _auf_hoehe_ziehen(rechts, hoehe)
    return links + rechts


def bau_wer_macht_was(block, g, y, gruppe):
    zeilen = block["zeilen"]
    titel = _text(ci.ROLLE_X_MM, y + ci.POLSTER_Y_MM,
                  ci.SATZ_B_MM - 2 * ci.POLSTER_X_MM,
                  block.get("titel", "WER MACHT WAS?"), g.titel, fett=True,
                  gruppe=gruppe)
    lauf = titel.y + titel.h + 2.5
    texte = [titel]
    trenner = []

    for i, zeile in enumerate(zeilen):
        rolle = _text(ci.ROLLE_X_MM, lauf, ci.ROLLE_B_MM, zeile["rolle"],
                      g.rolle, fett=True, gruppe=gruppe)
        aufgabe = _text(ci.AUFGABE_X_MM, lauf, ci.AUFGABE_B_MM, zeile["aufgabe"],
                        g.text, gruppe=gruppe)
        texte.extend([rolle, aufgabe])
        lauf += max(rolle.h, aufgabe.h)
        if i < len(zeilen) - 1:
            lauf += 1.5
            trenner.append(Linie(ci.ROLLE_X_MM, lauf,
                                 ci.SATZ_X_MM + ci.SATZ_B_MM - ci.POLSTER_X_MM,
                                 lauf, ci.LINIE_LEICHT, 0.5, gruppe))
            lauf += 1.5

    gesamt = lauf - y + ci.POLSTER_Y_MM
    flaeche = Flaeche(ci.SATZ_X_MM, y, ci.SATZ_B_MM, gesamt, ci.FLAECHE_GRAU_1,
                      ci.CI_BLAU, 1.0, gerundet=True, gruppe=gruppe)
    return [flaeche] + trenner + texte


def bau_abschluss(block, g, y, gruppe):
    """Abschlussband: Ueberschrift links, Kriterien rechts daneben.

    Nebeneinander statt untereinander - das Band bleibt flach, und die Karte
    gewinnt die Millimeter, an denen sie sonst scheitert.
    """
    kriterien = block["kriterien"]
    if len(kriterien) > 1:
        inhalt = chr(10).join("- " + k for k in kriterien)
    else:
        inhalt = kriterien[0]

    innen_x = ci.SATZ_X_MM + ci.POLSTER_X_MM
    innen_b = ci.SATZ_B_MM - 2 * ci.POLSTER_X_MM
    label_b = 60.0
    oben = y + ci.POLSTER_Y_MM

    label = _text(innen_x, oben, label_b, block["label"], g.titel, fett=True,
                  gruppe=gruppe)
    text = _text(innen_x + label_b + 4.0, oben, innen_b - label_b - 4.0,
                 inhalt, g.text, gruppe=gruppe)

    hoehe = max(label.h, text.h) + 2 * ci.POLSTER_Y_MM
    flaeche = Flaeche(ci.SATZ_X_MM, y, ci.SATZ_B_MM, hoehe, ci.FLAECHE_BLAU_2,
                      ci.CI_BLAU, 1.0, gerundet=True, gruppe=gruppe)
    return [flaeche, label, text]


BAUER = {
    "anlass": bau_anlass,
    "schritt": bau_schritt,
    "hinweis": bau_hinweis,
    "entscheidung": bau_entscheidung,
    "zwei_spalten": bau_zwei_spalten,
    "wer_macht_was": bau_wer_macht_was,
    "abschluss": bau_abschluss,
}


# ----------------------------------------------------------------- Kopf, Fuss


def bau_kopf(kopf, logo_pfad):
    """Baut das Kopfband und gibt (Rahmen, Bandhoehe) zurueck.

    Die Bandhoehe ist nicht fest: Der Titel ist das Erkennungsmerkmal der Karte
    und wird nicht kleingerechnet, damit er in ein Band passt - das Band waechst
    mit. Genau so halten es auch die Bestandskarten (30 bis 38 mm).

    Gemessen wird gegen die BREITERE von Track und Arial Bold. Track ist rund
    18 Prozent breiter als Arial; wer nur gegen die Ersatzschrift misst, baut
    einen Titel, der beim Ersteller ueberlaeuft.
    """
    breite = ci.SATZ_B_MM - (ci.LOGO_PLATZ_MM if logo_pfad else 0.0)

    def titelbreite(text, grad):
        return max(tm.schrift(ci.SCHRIFT_KOPF).breite_mm(text, grad),
                   tm.schrift("Arial", True).breite_mm(text, grad))

    # Erst der groesste Grad, der EINZEILIG passt - ein einzeiliger Titel liest
    # sich auf Distanz deutlich besser. Geht das bei keinem Grad, bleibt es beim
    # kleinsten, und das Band nimmt die zweite Zeile auf.
    grad = ci.GRAD_TITEL_STUFEN[-1]
    for kandidat in ci.GRAD_TITEL_STUFEN:
        if titelbreite(kopf["titel"], kandidat) <= breite:
            grad = kandidat
            break

    eyebrow = _text(ci.SATZ_X_MM, 6.0, breite, kopf["eyebrow"], ci.GRAD_EYEBROW,
                    farbe=ci.TEXT_INVERS, schrift=ci.SCHRIFT_KOPF,
                    sperrung=1.2, gruppe="kopf")
    titel = _text(ci.SATZ_X_MM, eyebrow.y + eyebrow.h + 1.5, breite,
                  kopf["titel"], grad, farbe=ci.TEXT_INVERS,
                  schrift=ci.SCHRIFT_KOPF, gruppe="kopf")

    texte = [eyebrow, titel]
    unten = titel.y + titel.h
    if kopf.get("untertitel"):
        unter = _text(ci.SATZ_X_MM, unten + 1.2, breite, kopf["untertitel"],
                      ci.GRAD_UNTERTITEL, farbe=ci.TEXT_INVERS,
                      schrift=ci.SCHRIFT_KOPF, gruppe="kopf")
        texte.append(unter)
        unten = unter.y + unter.h

    bandhoehe = max(ci.KOPF_H_MM, unten + 4.0)
    if bandhoehe > ci.KOPF_H_MAX_MM:
        raise PasstNicht(
            "Der Kartentitel ist zu lang für das Kopfband." + chr(10)
            + "  '" + kopf["titel"] + "'" + chr(10)
            + "  Er braucht {:.0f} mm, das Band darf höchstens {:.0f} mm hoch sein.".format(
                bandhoehe, ci.KOPF_H_MAX_MM) + chr(10)
            + "  Den Titel kürzen - er soll aus zwei Metern Entfernung die Frage" + chr(10)
            + "  beantworten, ob das die richtige Karte ist.",
            bandhoehe - ci.KOPF_H_MAX_MM, [("kopf", bandhoehe)])

    rahmen = [Flaeche(0, 0, ci.SEITE_B_MM, bandhoehe, ci.CI_BLAU,
                      gerundet=False, gruppe="kopf")]
    if logo_pfad:
        rahmen.append(Bild(ci.SEITE_B_MM - ci.RAND_MM - ci.LOGO_H_MM, ci.LOGO_Y_MM,
                           ci.LOGO_H_MM, ci.LOGO_H_MM, logo_pfad, gruppe="kopf"))
    rahmen.extend(texte)
    return rahmen, bandhoehe


def bau_fusszeile(karte):
    def oder_strich(wert):
        return wert if wert else "_______________"

    links = "{}   /   Revision {}   /   {}   /   {}".format(
        karte["id"], karte["revision"], karte["datum_anzeige"],
        karte["status_anzeige"])
    mitte = "Verfasser: {}     Prüfer: {}     Freigeber: {}".format(
        karte["verfasser"], oder_strich(karte.get("pruefer")),
        oder_strich(karte.get("freigeber")))
    return [
        Linie(ci.SATZ_X_MM, ci.FUSS_LINIE_Y_MM, ci.SATZ_X_MM + ci.SATZ_B_MM,
              ci.FUSS_LINIE_Y_MM, ci.LINIE_LEICHT, 0.5, "fuss"),
        _text(ci.SATZ_X_MM, ci.FUSS_Y_MM, ci.SATZ_B_MM, links, ci.GRAD_FUSS,
              farbe=ci.FUSS_TEXT, gruppe="fuss"),
        _text(ci.SATZ_X_MM, ci.FUSS_Y_MM + 4.2, ci.SATZ_B_MM, mitte, ci.GRAD_FUSS,
              farbe=ci.FUSS_TEXT, gruppe="fuss"),
        _text(ci.SATZ_X_MM, ci.FUSS_Y_MM + 8.4, ci.SATZ_B_MM, "A4 Hochformat",
              ci.GRAD_FUSS, farbe=ci.FUSS_TEXT, ausrichtung="rechts", gruppe="fuss"),
    ]


# -------------------------------------------------------------------- Aufbau


def _bloecke_setzen(bloecke, g, abstand, y_start):
    rahmen = []
    groessen = []
    y = y_start
    for i, block in enumerate(bloecke):
        bauer = BAUER.get(block["typ"])
        if bauer is None:
            raise ValueError("Unbekannter Blocktyp: " + str(block["typ"]))
        teil = bauer(block, g, y, "b{}".format(i))
        hoehe = _hoehe_von(teil, y)
        groessen.append((block["typ"], hoehe))
        rahmen.extend(teil)
        y += hoehe + abstand
    return rahmen, y - abstand, groessen


def setzen(karte, bloecke, logo_pfad):
    """Baut die Seite und faellt notfalls stufenweise auf engere Grade zurueck.

    Reihenfolge der Massnahmen: erst der Blockabstand, dann der Schriftgrad.
    Ein Gradsprung ueber die ganze Karte kostet mehr Lesbarkeit als ein
    Millimeter weniger Luft zwischen zwei Kaesten.

    Die letzte Stufe setzt den Fliesstext auf 10 pt - das ist die in den
    Gestaltungsregeln festgelegte Untergrenze fuer eine Karte, die im Stehen
    an der Maschine gelesen wird. Danach wird nicht weiter verkleinert,
    sondern abgebrochen.
    """
    grenze = ci.FUSS_LINIE_Y_MM - 4.0
    kopfrahmen, bandhoehe = bau_kopf(karte["kopf"], logo_pfad)
    y_start = bandhoehe + ci.ABSTAND_ABSCHNITT_MM
    letzte = None

    for stufe in range(len(ci.GRAD_STUFEN)):
        g = Grade(stufe)
        for abstand in (ci.ABSTAND_BLOCK_MM, 4.0):
            rahmen, unterkante, groessen = _bloecke_setzen(bloecke, g, abstand, y_start)
            letzte = (unterkante, g, groessen)
            if unterkante <= grenze:
                seite = Seite()
                seite.dazu(*kopfrahmen)
                seite.dazu(*rahmen)
                seite.dazu(*bau_fusszeile(karte))
                return seite, {
                    "stufe": stufe,
                    "fliesstext_pt": g.text,
                    "blockabstand_mm": abstand,
                    "kopfband_mm": round(bandhoehe, 1),
                    "hoehe_genutzt_mm": round(unterkante - y_start, 1),
                    "hoehe_verfuegbar_mm": round(grenze - y_start, 1),
                }

    unterkante, g, groessen = letzte
    ueberschuss = unterkante - grenze
    groessen.sort(key=lambda p: -p[1])
    liste = chr(10).join(
        "    {:16s} {:6.1f} mm".format(typ, h) for typ, h in groessen[:4])
    meldung = (
        "Die Karte passt nicht auf eine A4-Seite." + chr(10)
        + "  verfuegbar   {:6.1f} mm".format(grenze - y_start) + chr(10)
        + "  benoetigt    {:6.1f} mm".format(unterkante - y_start) + chr(10)
        + "  Überschuss  {:6.1f} mm  (rund {:.1f} Zeilen zu {:.0f} pt)".format(
            ueberschuss, ueberschuss / ci.zeilenhoehe_mm(g.text), g.text) + chr(10)
        + chr(10) + "  Größte Blöcke:" + chr(10) + liste + chr(10) + chr(10)
        + "  Kürzen oder den Prozess auf zwei Karten teilen. Den Schriftgrad" + chr(10)
        + "  weiter zu senken ist keine Lösung - die Karte wird an der" + chr(10)
        + "  Maschine gelesen, nicht am Bildschirm."
    )
    raise PasstNicht(meldung, ueberschuss, groessen)
