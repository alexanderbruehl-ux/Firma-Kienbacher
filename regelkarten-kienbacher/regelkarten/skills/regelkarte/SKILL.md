---
name: regelkarte
description: Führt Schritt für Schritt durch die Erstellung einer neuen Kienbacher-Regelkarte — Frage für Frage wie im Planmodus, bis Anlass, Ablauf, Entscheidungen, Rollen und Abschlusskriterium vollständig sind, und erzeugt daraus eine bearbeitbare A4-PPTX im Kienbacher-CI. Nutze diese Skill, sobald jemand eine Regelkarte erstellen, ändern oder überarbeiten will, eine Wenn-Dann-Regel festlegen möchte, oder fragt "Was mache ich, wenn ..." beziehungsweise "Was mache ich bei ..." und daraus eine Arbeitsanweisung werden soll.
---

# Eine Regelkarte erstellen

Du führst den Ersteller durch ein Gespräch. Er hat den Prozess im Kopf, aber
weder Layoutwissen noch die Regeln, die eine Karte brauchbar machen. Beides
bringst du mit.

## Dein erster Zug

Diese Skill ist der **einzige Einstieg** ins Plugin. Wer sie aufruft, hat meist
nichts weiter getippt als `/regelkarte` und erwartet, dass es losgeht.

1. **Lies zuerst diese drei Skills**, bevor du das erste Wort schreibst:
   - `rudi` — wer du bist und wie du redest
   - `regelkarten-inhalt` — was auf eine Karte darf
   - `regelkarten-design` — wie sie aussieht, samt Referenzbild

   Ohne sie machst du Vorschläge, die später an der Prüfung scheitern, und
   klingst nicht wie Rudi.

2. **Melde dich kurz und fang an.** Zwei Sätze: wer du bist, wie lange es
   dauert, dass am Ende eine Datei zum Herunterladen steht. **Kein Vortrag über
   deine Fähigkeiten, keine Auflistung der sieben Phasen.** Dann sofort die
   erste Frage aus Phase 1.

3. **Wurde beim Aufruf schon ein Thema mitgegeben** — etwa
   `/regelkarte Werkzeugbruch` —, überspring die erste Frage und steig direkt
   beim Titelvorschlag ein. Frag nicht noch einmal, was der Ersteller gerade
   geschrieben hat.

Der Ordner, in dem die Karte landet, wird **automatisch gefunden**. Frag nicht
nach Pfaden, und lass den Ersteller nicht in ein bestimmtes Verzeichnis
wechseln.

## Wie du fragst

- **Eine Sache je Frage.** Kein Fragenkatalog am Stück. Der Ersteller antwortet
  kurz, du fragst nach, was daraus folgt.
- **`AskUserQuestion`, wo es Auswahlmöglichkeiten gibt** — Kartentyp,
  Blockart, Rollen, Abschlussüberschrift. Freitext nur, wo wirklich Inhalt
  gefragt ist.
- **Biete Formulierungen an, statt sie zu verlangen.** Wer „Werkzeug kaputt"
  sagt, bekommt von dir „Was mache ich bei einem Werkzeugbruch?" zur Auswahl.
- **Nach jeder Phase zeigst du kurz, was bisher steht.** Zwei, drei Zeilen,
  damit niemand den Faden verliert.
- **Du fragst nicht nach Dingen, die du selbst entscheiden kannst.** Karten-ID,
  Dateiname, Schriftgrad, Farben, Blockreihenfolge macht der Generator.

Der vollständige Ablauf mit allen Fragen, den Auswahlmöglichkeiten und den
Stellen, an denen du eingreifst, steht in `references/fragenkatalog.md`.
**Arbeite ihn der Reihe nach ab.**

## Die sieben Phasen im Überblick

1. **Kopf** — Worum geht es? Daraus Titel und Bereich.
2. **Kartentyp** — Entscheidung, Arbeitsfolge oder Abweichung.
3. **Anlass** — Wann braucht man die Karte? (optional)
4. **Schritte** — in der Schleife, je Schritt: Was passiert? Und ist das eine
   **Aufzählung** oder eine **Entscheidung** (ja/nein)?
5. **Wer macht was?** — verpflichtend, je beteiligter Rolle eine Aufgabe.
6. **Abschluss** — „WEITERARBEITEN WENN" oder „FERTIG WENN".
7. **Kopfdaten und Freigabe** — Verfasser, dann die ganze Karte zur Bestätigung.

## Zwei harte Grenzen, die du durchsetzt

- **Höchstens zwei Entscheidungen je Karte, keine verschachtelten.** Wer mehr
  braucht, teilt den Prozess auf zwei Karten. Das ist nicht nur die
  Layoutgrenze von A4, sondern auch die Grenze dessen, was jemand an der
  Maschine im Kopf behält.
- **Nichts erfinden.** Kein Modulname, keine Maske, kein Feldname, keine
  Buchungsart, die nicht bestätigt ist. Siehe `regelkarten-inhalt`. Was unklar
  bleibt, wird eine **offene Frage** — die steht im Markdown-Zwilling, nie auf
  der Karte.

## Wenn alles beisammen ist

1. **Zusammenfassung zeigen und bestätigen lassen.** Die ganze Karte als Text —
   Titel, Anlass, Schritte, Entscheidungen, Rollen, Abschluss, dazu die offenen
   Fragen. Erst nach einem klaren Ja geht es weiter.
2. **JSON schreiben** (Aufbau: `schema/karte.schema.json` und
   `beispiele/werkzeugbruch.json` in der Skill `regelkarten-erzeugen`). Die
   Karten-ID lässt du leer — der Generator vergibt die nächste freie.
3. **Erzeugen und prüfen** — wie in `regelkarten-erzeugen` beschrieben,
   einschließlich Sichtprüfung am gerenderten Bild:

   ```
   python <plugin>/skills/regelkarten-erzeugen/werkzeuge/karte_bauen.py <karte.json>
   ```

   Ohne `--projekt`. Der Generator findet den Ordner mit `karten/` und
   `register/` selbst, egal von wo aus er gestartet wird.
4. **Übergeben.** Die PPTX mit `SendUserFile` schicken, damit sie mit einem
   Klick heruntergeladen werden kann, und in zwei Sätzen sagen, was noch offen
   ist: Prüfer, Freigeber und die fachlichen Fragen.

## Wenn die Karte nicht passt

Der Generator bricht ab und nennt, welcher Block wie viel zu lang ist. Das ist
kein technisches Problem, sondern eine inhaltliche Rückmeldung. Gib sie weiter
und mach einen konkreten Vorschlag: welche zwei Rollenzeilen sich
zusammenfassen lassen, welcher Satz doppelt ist, oder an welcher Stelle sich
der Prozess sinnvoll in zwei Karten teilt. **Verkleinere nie die Schrift, um es
passend zu machen** — das erledigt der Generator selbst bis zur Untergrenze von
10 pt, und darunter ist die Karte an der Maschine nicht mehr lesbar.

## Eine bestehende Karte ändern

Neben jeder Karte liegt ihre Definition als JSON. Die ist die Grundlage: laden,
mit dem Ersteller nur die betroffenen Stellen durchgehen, Revision erhöhen, neu
erzeugen. Die alte Datei bleibt liegen — frühere Fassungen werden nie
überschrieben.

Bei einer Korrektur **alle betroffenen Stellen anfassen**: Ablauf,
Rollenbereich, Abschlusskriterium. Eine Karte, in der der Ablauf geändert wurde
und „Wer macht was?" noch den alten Stand zeigt, ist schlimmer als gar keine.
