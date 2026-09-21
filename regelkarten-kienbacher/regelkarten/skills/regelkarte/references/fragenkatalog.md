# Fragenkatalog

Der Ablauf in der Reihenfolge, in der er abzuarbeiten ist. Die Fragen sind
Vorlagen, keine Formeln — sprich wie ein Kollege, nicht wie ein Formular.

---

## Phase 1 — Kopf

### 1.1 Worum geht es?

> „Was ist das Problem oder die Situation, für die es eine Regel braucht?"

Freitext. Alles Weitere hängt daran.

### 1.2 Titel vorschlagen

Aus der Antwort baust du **zwei Formulierungen** und lässt wählen
(`AskUserQuestion`):

| Form | Wann | Beispiel |
|---|---|---|
| „Was mache ich **bei** …?" | Zustand oder Ereignis | Was mache ich bei einem Werkzeugbruch? |
| „Was mache ich, **wenn** …?" | Bedingung, die eintreten kann | Was mache ich, wenn Material fehlt? |

Dazu als dritte Möglichkeit die eigene Formulierung des Erstellers.

**Der Titel ist eine Frage, kein Schlagwort.** Nicht „Werkzeugbruch", sondern
„Was mache ich bei einem Werkzeugbruch?". Er muss aus zwei Metern Entfernung
beantworten, ob das die richtige Karte ist.

**Und er muss kurz sein.** Über etwa 45 Zeichen wird es im Kopfband eng — der
Generator meldet das, aber besser ist, es kommt gar nicht so weit.

### 1.3 Bereich

> „Für welchen Bereich? Das steht als kleine Zeile über dem Titel."

Auswahl: PRODUKTION · MONTAGE · WERKZEUGBAU · LOGISTIK · QUALITÄT.
Daraus wird `KIENBACHER AKADEMIE / [BEREICH]`.

### 1.4 Untertitel

> „Soll unter dem Titel noch eine kurze Zeile stehen, die den Ablauf auf den
> Punkt bringt? Zum Beispiel: Maschine stoppen, melden, Werkzeug beurteilen
> lassen."

Optional. Drei bis fünf Wörter, meist die Kernschritte als Aufzählung.

---

## Phase 2 — Kartentyp

> „Was soll die Karte leisten?"

| Auswahl | Bedeutung | Folge für den Aufbau |
|---|---|---|
| **Entscheidung** | Es gibt eine Prüfung mit zwei Wegen | mindestens eine Ja/Nein-Verzweigung, Abschluss „WEITERARBEITEN WENN" |
| **Arbeitsfolge** | Eine Tätigkeit wird Schritt für Schritt ausgeführt | nur nummerierte Schritte, Abschluss „FERTIG WENN" |
| **Abweichung** | Etwas ist schiefgegangen: melden, prüfen, weiter | Schritte plus meist eine Verzweigung, Abschluss „WEITERARBEITEN WENN" |

**Bei einer reinen Arbeitsfolge baust du keine künstliche Ja/Nein-Frage ein.**
Eine zeitliche Reihenfolge ist keine Wahlmöglichkeit.

---

## Phase 3 — Anlass

> „Woran merkt jemand, dass er diese Karte braucht?"

Ein Satz, wird zum Block „WENN". Optional — wenn der Titel den Anlass schon
vollständig erklärt, lass ihn weg, statt ihn zu wiederholen.

Gut ist eine **Beobachtung**, nicht eine Bewertung: „Bruch sichtbar oder hörbar,
Teile unvollständig" statt „Werkzeug ist defekt".

---

## Phase 4 — Schritte (Schleife)

Je Schritt zwei Fragen, dann die Frage nach dem nächsten.

### 4.1 Was passiert?

> „Was passiert als Erstes?" — beim nächsten Durchlauf: „Und dann?"

### 4.2 Aufzählung oder Entscheidung?

`AskUserQuestion` mit genau diesen beiden Möglichkeiten:

| Auswahl | Wann | Was daraus wird |
|---|---|---|
| **Aufzählung** | Es wird etwas getan, ohne Weggabelung | nummerierter Kasten |
| **Entscheidung (Ja/Nein)** | Es wird geprüft, und es geht unterschiedlich weiter | Frage mit zwei beschrifteten Zweigen |

Wenn der Ersteller unsicher ist, hilft diese Probe: **Stünde an dieser Stelle
in einem Ablaufplan eine Raute?** Wird etwas geprüft und geht es danach
unterschiedlich weiter — Entscheidung. Wird einfach etwas getan — Aufzählung.

### 4.3a Bei Aufzählung

> „Wer macht das?" — Auswahl aus dem Rollenkatalog
> (`regelkarten-inhalt/references/rollenkatalog.md`), plus freie Eingabe.

Dann formulierst du **Titel und Text** und legst sie zur Bestätigung vor:

- **Titel:** kurz, in Versalien, mit einem Tätigkeitswort —
  „MASCHINE STOPPEN UND TEILE SICHERN"
- **Text:** ein bis zwei Sätze, konkret. Was wird angesehen, was eingegeben,
  wo steht es.

### 4.3b Bei Entscheidung

Drei Fragen hintereinander:

1. > „Was genau wird geprüft? Formulier es als Frage, die man mit ja oder nein
   > beantworten kann."

   Muss eindeutig sein. „Ist Material vorhanden?" geht. „Wie ist die Lage?"
   nicht.

2. > „Was passiert bei JA?"
3. > „Was passiert bei NEIN?"

Beide Wege müssen **bei einer klaren Handlung oder Übergabe enden**. Ein Weg,
der ins Leere läuft, ist kein Weg.

Daraus baust du je Zweig einen kurzen Titel in Versalien und einen Text von ein
bis zwei Sätzen.

### 4.4 Noch ein Schritt?

> „Gibt es noch einen Schritt, oder sind wir mit dem Ablauf durch?"

**Zählmarken, die du im Auge behältst:**

- Bei der **dritten Entscheidung** brichst du ab und schlägst vor, den Prozess
  auf zwei Karten zu teilen.
- Ab etwa **sechs Blöcken** weist du darauf hin, dass es auf A4 eng wird — noch
  bevor der Generator es meldet.

---

## Phase 5 — Wer macht was?

**Verpflichtend auf jeder Karte.** Rollennamen in den Schritten ersetzen ihn
nicht.

### 5.1 Beteiligte Rollen

Du zeigst die Rollen, die in den Schritten vorgekommen sind, als Mehrfachauswahl
und fragst:

> „Wer ist außerdem beteiligt?"

Vorschläge aus dem Rollenkatalog. **Keine Rolle aufnehmen, nur damit die
Tabelle voller aussieht.**

### 5.2 Je Rolle die Aufgabe

> „Was macht [Rolle] in diesem Ablauf konkret?"

Ein Satz, mit Tätigkeitswörtern. Du schlägst aus den Schritten eine
Formulierung vor und lässt bestätigen.

**Prüfe dabei die fünf Aufgabenarten** (melden, prüfen, entscheiden, ausführen,
dokumentieren): Liegt eine davon bei niemandem, frag nach. Besonders
„dokumentieren" wird gern vergessen — Schichtlogbuch, Instandhaltungsliste,
Werkzeugbauliste.

**Und prüfe die Grenzen:** Mitarbeitende entscheiden nicht, korrigieren keine
Bestände und reparieren nicht. Steht so etwas in einem Vorschlag, frag nach,
wer es wirklich tut.

---

## Phase 6 — Abschlusskriterium

Überschrift schlägst du nach Kartentyp vor:

- **„WEITERARBEITEN WENN"** bei Unterbrechung oder Entscheidung
- **„FERTIG WENN"** bei einer abgeschlossenen Tätigkeit

> „Woran erkennt man, dass es weitergehen kann?"

Ein bis zwei **überprüfbare** Kriterien. Nicht den ganzen Ablauf wiederholen.

Gut: „Werkzeugbau hat das Werkzeug freigegeben."
Schlecht: „Alles ist erledigt."

---

## Phase 7 — Kopfdaten und Freigabe

### 7.1 Verfasser

> „Wer schreibt die Karte? Der Name kommt in die Fußzeile."

Steht der Name schon aus dem Gespräch fest, schlag ihn vor und lass bestätigen.
**Prüfer und Freigeber bleiben leer** — die werden später von Hand eingetragen.

### 7.2 Offene Fragen sammeln

Alles, was im Gespräch unklar geblieben ist, listest du auf:

> „Diese Punkte konnten wir nicht klären — sie kommen nicht auf die Karte,
> sondern in die Begleitdatei. Passt das so, oder kannst du etwas davon jetzt
> beantworten?"

### 7.3 Die ganze Karte zeigen

Vollständig als Text, in der Reihenfolge der Karte. Dann:

> „Passt das so? Dann erzeuge ich die Karte."

Erst nach einem klaren Ja wird gebaut.

---

## Formulierungen, die du korrigierst

| Statt | Besser | Warum |
|---|---|---|
| „BARI gibt frei" | „Der Schichtführer prüft in BARI und entscheidet" | Ein Modul entscheidet nicht |
| „SOFORT MÖGLICH" | die Sache benennen | war dem Haus zu unklar |
| „Bei Problemen melden" | wem, womit, woran erkennbar | zu unbestimmt zum Handeln |
| „Der Mitarbeiter korrigiert den Bestand" | wer das wirklich darf | Mitarbeitende korrigieren keine Bestände |
| „gegebenenfalls" | die Bedingung ausschreiben | sonst entscheidet jeder anders |
| ein STOPP-Kasten auf jeder Karte | die tatsächliche Unterbrechung benennen | pauschale Warnungen werden überlesen |
