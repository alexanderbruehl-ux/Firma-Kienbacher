---
name: regelkarten-design
description: Gestaltungsregeln für Kienbacher-Regelkarten — Raster im A4-Hochformat, Kienbacher-CI in Blau #0079A7 und Grau #7B7C7E, Typografie mit Track im Kopf und Arial im Text, Lesbarkeit und Kontrast, Aufbau von Ablaufschritten und Ja/Nein-Verzweigungen, Bereich "Wer macht was?", Fußzeile. Nutze diese Skill bei jeder Frage zu Aussehen, Layout, Farbe, Schriftgröße, Logo, Abstand, Lesbarkeit oder Druckbarkeit einer Regelkarte — und immer, bevor eine Karte erzeugt oder verändert wird.
user-invocable: false
---

# Gestaltung der Regelkarte

Die genauen Zahlen stehen in `references/raster.md`. **Lies die Datei, bevor du eine
Karte baust oder ein Layout beurteilst** — hier steht nur, warum die Werte so sind
und woran du eine schlechte Karte erkennst.

## Der Gestaltungsstand ist festgelegt

Am 17.09.2026 hat der Auftraggeber das Aussehen **abgenommen**. Ab hier gilt:

> **Jede neue Karte sieht aus wie die Referenzkarten.** Layout, Farben,
> Typografie, Blockformen und Reihenfolge werden nicht neu erfunden, nicht
> „verbessert" und nicht an den Inhalt angepasst.

Die abgenommene Fassung liegt in `referenz/`:

| Datei | Wofür |
|---|---|
| `RK-011_referenzkarte.png` | **das Zielbild.** Entscheidung mit Ja/Nein-Verzweigung, zweizeiliger Titel, 12 pt Fließtext |
| `RK-010_referenzkarte.png` | dieselbe Gestaltung bei voller Seite: drei Schritte, fünf Rollen, 10 pt nach der Kaskade |
| `RK-011_referenzkarte.json` | die zugehörige Definition, als Muster für den Aufbau |

**Sieh dir das Zielbild an, bevor du eine Karte als fertig meldest**, und
vergleiche. Weicht deine Karte in etwas anderem als dem Inhalt ab, ist das ein
Fehler — kein Spielraum.

Geändert wird die Gestaltung nur, wenn der Auftraggeber es **ausdrücklich
verlangt**. Dann gehören Bild, `raster.md` und `werkzeuge/ci.py` gemeinsam
nachgezogen, sonst laufen sie auseinander.

Was ausdrücklich **kein** Grund für eine Abweichung ist: Der Inhalt passt nicht
auf die Seite. Dann wird gekürzt oder der Prozess geteilt — nicht das Layout
angefasst.

## Wofür die Karte gemacht ist

Sie hängt an der Maschine oder liegt am Arbeitsplatz. Jemand liest sie **im Stehen,
unter Zeitdruck, oft mit schmutzigen Händen und in schlechtem Licht**, und meist
nicht zum ersten Mal. Daraus folgt alles Weitere:

- Der Titel muss aus zwei Metern Entfernung die Frage beantworten „ist das meine
  Karte?". Deshalb 20–24 pt und eine konkrete Frage, kein Schlagwort.
- Der nächste Handlungsschritt muss beim Überfliegen findbar sein. Deshalb
  nummerierte Schritte und kurze Zeilen, kein Fließtextblock.
- Eine Entscheidung muss man sehen, bevor man sie liest. Deshalb die Verzweigung
  als Grafik und nicht als Satz „falls nein, dann …".

## Die fünf Fehler, die eine Karte unbrauchbar machen

1. **Zu viel drauf.** Die häufigste Ursache. Wenn es eng wird, ist die richtige
   Antwort kürzen oder den Prozess auf zwei Karten teilen — nicht der Schriftgrad.
   Unter 10 pt geht nichts.
2. **Farbe trägt die Bedeutung allein.** Jeder Zweig, jede Ausnahme bekommt das
   Wort dazu: „JA", „NEIN", „AUSNAHME". Etwa jeder zwölfte Mann sieht Farben anders,
   und die Karte wird oft schwarz-weiß kopiert.
3. **Linien, die ins Leere laufen** oder durch Text hindurch. Jede Verbindungslinie
   beginnt an einer Box und endet an einer Box.
4. **Rollen nur im Fließtext.** Der Bereich „Wer macht was?" ist Pflicht und wird
   nicht dadurch ersetzt, dass in den Schritten Rollennamen vorkommen.
5. **Die Karte als Bild.** Jeder Text, jede Fläche, jede Linie ist ein eigenes
   Objekt. Nur echte Screenshots sind Bilder.

## Farbe

Ausschließlich Kienbacher-CI: Blau `#0079A7`, Grau `#7B7C7E` und deren Aufhellungen
und Abdunklungen. Grün und Gelb sind bewusst abgeschafft — die früheren Karten
hatten eine eigene Farbwelt, die mit dem Firmenauftritt nichts zu tun hatte.

Rot `#B22F22` ist **nur** für einen echten Sicherheitshinweis zulässig, also wenn
jemand zu Schaden kommen kann. Nicht für Dringlichkeit, nicht für „wichtig", nicht
für ein Abschlusskriterium.

**Blau ist Struktur, nicht Text.** Kopfband, Rahmen, Linien, Chips. Fließtext und
Abschnittstitel stehen in `#00435C`, weil Blau auf den hellen Flächen nur 4,29 : 1
erreicht und damit unter der Schwelle liegt. Alle nachgerechneten Werte stehen in
`references/raster.md`.

## Schrift

**Track** nur für Eyebrow und Titel im Kopfband — die Schrift hat keinen Fettschnitt
und ist auf vielen Rechnern nicht installiert. **Arial** für alles Übrige, Regular
und Bold, weil sie überall vorhanden ist und die Karte damit auf jedem Arbeitsplatz
gleich aussieht.

Fett ist reserviert für Rollennamen, Abschnittstitel, Schrittnummern und
Chip-Beschriftungen. Nicht zur Betonung mitten im Satz — wenn alles wichtig ist,
ist nichts wichtig.

## Logo

Die Kienbacher-Bildmarke steht als weiße Knockout-Variante oben rechts im Kopfband,
16 mm hoch, rechte Kante bündig mit dem Satzspiegel. Sie wird nie verzerrt, nie
eingefärbt und nie kleiner als 12 mm gesetzt. Der Schriftzug „KIENBACHER" kommt
nicht auf die Karte — die Eyebrow-Zeile „KIENBACHER AKADEMIE / [BEREICH]" leistet
das bereits, und beides nebeneinander wäre doppelt.

## Bevor du eine Karte als fertig meldest

Sieh dir das gerenderte Bild an — nicht die Definition, das **Bild**. Prüfe:

- Kein Text ist abgeschnitten, keine Zeile läuft aus ihrer Box.
- Keine zwei Flächen überlappen.
- Alle Umlaute und Sonderzeichen sind da.
- Jede Verzweigungslinie endet an einer Box.
- Der Titel steht vollständig im Kopfband, das Logo ist sauber freigestellt.
- Die Karte endet vor der Fußzeile, nicht darunter.
- **Sie sieht aus wie `referenz/RK-011_referenzkarte.png`** — gleiche Blockformen,
  gleiche Farben, gleiche Reihenfolge, gleiche Fußzeile.

Findest du einen dieser Punkte, meldest du die Karte **nicht** als fertig, sondern
nennst den Fehler und behebst ihn.
