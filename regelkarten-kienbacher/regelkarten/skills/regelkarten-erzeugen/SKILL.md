---
name: regelkarten-erzeugen
description: Erzeugt aus einer Kartendefinition die fertige Regelkarte als bearbeitbare A4-PPTX samt Markdown-Zwilling und Registereintrag, und prüft sie am gerenderten Bild. Nutze diese Skill, wenn eine Regelkarte gebaut, neu erzeugt, geprüft, als Datei ausgegeben oder auf eine neue Revision gehoben werden soll, sowie bei Fragen zum Kartenregister, zu Karten-IDs oder zum JSON-Aufbau einer Karte.
user-invocable: false
---

# Die Karte erzeugen

Der Generator liegt unter `${CLAUDE_PLUGIN_ROOT}/skills/regelkarten-erzeugen/werkzeuge`.
Er nimmt eine Kartendefinition als JSON und schreibt die PPTX — aber nur, wenn
Inhalt und Geometrie stimmen. Schlägt eine Prüfung an, entsteht **keine Datei**.

## Ablauf

### 1. Definition schreiben

Aufbau: `schema/karte.schema.json`, vollständiges Muster:
`beispiele/werkzeugbruch.json`.

Im JSON stehen **keine Farben, keine Koordinaten, keine Schriftgrade**. Das ist
Absicht: Wer Inhalt pflegt, kann das Layout nicht beschädigen, und eine
CI-Änderung ist eine Änderung an einer Datei.

Ebenso stehen dort **keine Schrittnummern** — die zählt der Generator durch.
Sonst müsste man sie beim Einfügen eines Schrittes von Hand nachziehen, und
genau dort entstehen Fehler.

### 2. Bauen

```
python werkzeuge/karte_bauen.py <karte.json> --projekt <Projektordner>
```

Ergebnis in `karten/`:

| Datei | Zweck |
|---|---|
| `RK-0xx_kurztitel_r01.pptx` | die Karte, jedes Element ein eigenes Objekt |
| `RK-0xx_kurztitel_r01.md` | derselbe Inhalt als Text, plus offene Fragen und Messwerte |
| `RK-0xx_kurztitel_r01.json` | die Definition, Grundlage der nächsten Revision |

Dazu fortgeschrieben: `register/kartenregister.json` und `.md`.

### 3. Ansehen

```
powershell -ExecutionPolicy Bypass -File werkzeuge/vorschau.ps1 -Pptx <karte.pptx>
```

Exportiert die Folie als PNG. **Sieh dir das Bild an** — nicht die Definition,
das Bild. Die Prüfliste steht in `regelkarten-design`, Abschnitt „Bevor du eine
Karte als fertig meldest".

Das Skript öffnet aus einer lokalen Kopie (aus OneDrive heraus landet die Datei
sonst in der geschützten Ansicht) und beendet eine bereits laufende
PowerPoint-Sitzung des Benutzers nicht.

### 4. Übergeben

PPTX mit `SendUserFile` schicken. Dazu in zwei Sätzen: welche Revision, was noch
offen ist (Prüfer, Freigeber, fachliche Fragen), und wie viel Platz auf der
Seite noch frei ist.

## Was der Generator von sich aus ablehnt

| Abbruch | Grund |
|---|---|
| „Der Bereich 'Wer macht was?' fehlt" | Pflichtabschnitt |
| „Das Abschlusskriterium fehlt" | Pflichtabschnitt |
| mehr als zwei Entscheidungen | auf A4 nicht mehr lesbar — Prozess teilen |
| Zeichen, die **Track** nicht kennt | im Kopfbereich; sonst stünde dort ein Ersatzkästchen |
| „Die Karte passt nicht auf eine A4-Seite" | mit Angabe, welcher Block wie viel zu lang ist |
| Karten-ID gesperrt oder belegt | RK-001 bis RK-006 sind ungeklärt, RK-007 bis RK-009 vergeben |
| Status `freigegeben` ohne Prüfer, Freigeber oder mit offenen Fragen | eine Freigabe über offene Punkte hinweg gibt es nicht |
| Geometriebefund | Überlappung, Textüberlauf, frei endende Linie, zu kleiner Schriftgrad, zu schwacher Kontrast |

**Diese Abbrüche sind das Werkzeug, nicht das Hindernis.** Gib die Meldung an
den Ersteller weiter und mach einen konkreten Kürzungsvorschlag. Dreh nicht am
Layout, um eine überladene Karte doch noch unterzubringen.

## Schriftgrad-Kaskade

Passt der Inhalt nicht, versucht der Generator in dieser Reihenfolge:

1. Blockabstand von 5,0 auf 4,0 mm
2. Fließtext 12 → 11 pt
3. Fließtext 11 → 10 pt (die Untergrenze)

Danach bricht er ab. **10 pt ist die Grenze**, weil die Karte im Stehen an der
Maschine gelesen wird, nicht am Bildschirm.

Der Markdown-Zwilling protokolliert, welche Stufe gegriffen hat und wie viele
Millimeter noch frei sind. Steht dort „noch 3 mm frei", weiß man beim nächsten
Mal, dass jede Ergänzung die Seite sprengt.

## Register und IDs

`register/kartenregister.json` ist der Master, die `.md` daneben wird bei jedem
Lauf neu daraus erzeugt — **nicht von Hand ändern**, sonst ist die Änderung beim
nächsten Lauf weg.

Ohne `id` in der Definition vergibt der Generator die nächste freie. RK-001 bis
RK-006 bleiben gesperrt, bis geklärt ist, ob sie vergeben sind.

Bei einer bestehenden ID wird die Revision erhöht und der bisherige Stand in die
Historie geschrieben. **Alte Dateien werden nie überschrieben.**

## Track und das Logo

`assets/Track.ttf` liegt im Plugin und ist auf dem bearbeitenden Rechner zu
installieren. Fehlt die Schrift, ersetzt PowerPoint sie — das Layout bleibt
gültig, weil der Titel gegen die breitere von Track und Arial Bold gemessen
wird und die Zeilenhöhen absolut gesetzt sind.

**Track setzt alles in Versalien** und kennt kein `–`, `—`, `→` oder `§`.
Gedankenstriche werden automatisch ersetzt, bei allem anderen bricht der
Generator mit Angabe des Zeichens ab.

Die Logo-PNG liegen fertig in `assets/`. Sie werden **nicht** bei jedem Lauf neu
erzeugt — so bleibt der Produktivpfad frei von svglib, reportlab und pypdfium2,
und das eingebettete Bild ist auf jedem Rechner byteidentisch. Neu erzeugen nur
bei einer Logoänderung:

```
python werkzeuge/logo_erzeugen.py
```

## Voraussetzungen

- Python 3.11 oder neuer
- `python-pptx`, `fonttools` — `pip install python-pptx fonttools`
- Arial (`arial.ttf`, `arialbd.ttf` in `C:\Windows\Fonts`) — auf Windows immer da
- PowerPoint, nur für die Sichtprüfung
- `svglib`, `reportlab`, `pypdfium2` — nur für `logo_erzeugen.py`
