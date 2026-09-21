# regelkarten

Wenn-Dann-Regelkarten für die Kienbacher Akademie, angesprochen mit **„Rudi"**.

Rudi führt Frage für Frage durch die Erstellung einer Regelkarte — Anlass,
Ablauf, Entscheidungen, Rollen, Abschlusskriterium — und erzeugt daraus eine
bearbeitbare A4-PPTX im Kienbacher-CI, dazu den Inhalt als Markdown und einen
Eintrag im Kartenregister.

## Ansprache

„Rudi" allein genügt. Ebenso greift er ohne den Namen, sobald es um eine
Regelkarte geht: „Was mache ich, wenn …", „Wenn-Dann-Regel", „Arbeitsanweisung
für die Produktion", „Wer macht was", Kartenregister, Revision, Freigabe.

Als Slash-Befehl: `/regelkarten:regelkarte`

## Was drin ist

| Teil | Rolle |
|---|---|
| `skills/rudi` | Rudis Arbeitsanweisung: Arbeitsweise, die vier Dinge ohne Verhandlung, Berichtsform, Grenzen |
| `skills/regelkarte` | der geführte Ablauf in sieben Phasen, plus `references/fragenkatalog.md` mit allen Fragen |
| `skills/regelkarten-inhalt` | was auf eine Karte darf: Quellen, Rollen, Pflichtabschnitte, verbotene Überschriften — plus belegter `rollenkatalog.md` und `systemkatalog.md` |
| `skills/regelkarten-design` | Raster, Kienbacher-CI, Typografie, Lesbarkeit — plus `references/raster.md` mit allen Werten und nachgerechneten Kontrasten |
| `skills/regelkarten-erzeugen` | der Generator: JSON-Schema, Werkzeuge, Sichtprüfung, Register |
| `skills/regelkarten-vorschau` | eigenständige HTML-Vorschau aus fertigen PPTX — zum Ansehen ohne PowerPoint und zum Weitergeben an Kolleginnen und Kollegen ohne Claude-Zugang |
| `agents/Regelkarten-Rudi.md` | derselbe Rudi als abgesetzter Agent auf **Opus**, für Arbeitspakete mit fertiger Vorlage |

**Warum der Ablauf eine Skill ist und kein Agent:** Ein abgesetzter Agent kann
mitten im Lauf nicht zurückfragen. Das Frage-Antwort-Gespräch läuft deshalb im
Hauptgespräch. Der Agent ist für den Fall gedacht, dass der Ablauf schon
vollständig beschrieben vorliegt.

## Vier Dinge, an denen Rudi nicht verhandelt

1. **Nichts erfinden** — kein Modulname, keine Maske, keine Buchungsart ohne
   Bestätigung. Offenes wird eine offene Frage in der Begleitdatei, nie eine
   Arbeitsanweisung auf der Karte.
2. **„Wer macht was?" ist Pflicht** — Rollennamen in den Schritten ersetzen den
   Bereich nicht.
3. **Eine Seite A4** — passt es nicht, wird gekürzt oder der Prozess geteilt.
   Der Generator senkt den Fließtext bis 10 pt und bricht dann ab.
4. **Kein flaches Bild** — jeder Text, jede Fläche, jede Linie ist ein eigenes
   Objekt in der PPTX.

## Gestaltung

**Der Gestaltungsstand ist seit 17.09.2026 abgenommen und festgelegt.** Jede neue
Karte sieht aus wie `skills/regelkarten-design/referenz/RK-011_referenzkarte.png`.
Layout, Farben und Blockformen werden nicht an den Inhalt angepasst - passt etwas
nicht auf die Seite, wird gekürzt oder der Prozess geteilt.

Ausschließlich Kienbacher-CI: Blau `#0079A7`, Grau `#7B7C7E` und Töne daraus.
Kein Grün, kein Gelb. Rot nur für einen echten Sicherheitshinweis.

Ja- und Nein-Zweig werden über **fünf voneinander unabhängige Merkmale**
unterschieden — Position, Füllung, Rahmenstärke, Chip und das ausgeschriebene
Wort. Farbe trägt die Bedeutung nie allein; die Karte funktioniert bei
Farbfehlsichtigkeit und im Schwarz-Weiß-Ausdruck.

Schrift: **Track** im Kopfband (setzt in Versalien, kein Fettschnitt),
**Arial** für alles Übrige. Alle Textfarben sind gegen WCAG nachgerechnet und
werden bei jedem Lauf erneut geprüft.

## Einbinden

```
/plugin marketplace add "D:\Oswald Kienbacher GmbH\OK OneDrive - Production\Tillian\Claude\Regelkarten"
/plugin install regelkarten@regelkarten-kienbacher
```

Voraussetzungen: Python 3.11+, `pip install python-pptx fonttools`.
PowerPoint wird nur für die Sichtprüfung gebraucht.

Die Schrift `Track.ttf` liegt unter `skills/regelkarten-erzeugen/assets/` und
sollte auf jedem Rechner installiert sein, der Karten bearbeitet — sonst
ersetzt PowerPoint sie im Kopfband. Das Layout bleibt in beiden Fällen gültig.

## Nach jeder Änderung am Plugin

```
claude plugin validate ./regelkarten
```

**Nicht optional.** Ein Doppelpunkt mit Leerzeichen in einer `description` reicht,
damit YAML das Frontmatter für eine verschachtelte Zuordnung hält - die Skill lädt
dann still mit **leeren Metadaten** und springt nie an. Genau das war in `rudi`
passiert und ist nur aufgefallen, weil der Validator lief.

Danach in Claude Code `/reload-plugins`, dann ist die Änderung ohne Neustart aktiv.

## Aufruf

Nur `/regelkarte` erscheint im Slash-Menü (Groß- und Kleinschreibung egal, also
auch `/Regelkarte`). Die vier übrigen Skills sind Hintergrundwissen: `user-invocable:
false` nimmt sie aus dem Menü, das Modell lädt sie weiterhin selbst über ihre
Beschreibung. „Rudi" im Fließtext greift unverändert.

## Stand

Karten-IDs RK-007 bis RK-009 sind durch die Versuchskarten belegt, RK-001 bis
RK-006 sind ungeklärt und deshalb gesperrt. Die nächste freie ID vergibt der
Generator selbst.

## Version

0.1.0
