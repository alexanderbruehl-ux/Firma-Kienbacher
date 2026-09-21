---
name: regelkarten-inhalt
description: Die verbindlichen inhaltlichen Regeln für Kienbacher-Regelkarten — was auf eine Karte darf und was nicht, Trennung von Standardablauf und Ausnahme, korrekte Rollenzuordnung, Umgang mit ERP-Modulen und Systemangaben, Pflichtabschnitte, verbotene Überschriften, Umgang mit fachlichen Lücken. Nutze diese Skill, bevor der Inhalt einer Regelkarte formuliert, geprüft oder geändert wird, und bei jeder Frage dazu, ob eine Angabe auf die Karte gehört.
user-invocable: false
---

# Was auf eine Regelkarte gehört

Die Karte beantwortet **eine** Frage aus dem Arbeitsalltag. Wer sie liest, muss
in wenigen Sekunden wissen:

- Wann brauche ich diese Karte?
- Was muss ich anschauen oder prüfen?
- Was mache ich als Nächstes?
- Wer macht was?
- Wann kann ich weiterarbeiten?

Alles, was diese fünf Fragen nicht beantwortet, kommt nicht drauf.

## Die Quelle der Wahrheit

1. **Was der Ersteller sagt und was in seinen Unterlagen steht.** Sonst nichts.
2. **Neuere Korrekturen schlagen ältere Fassungen.** Auch die eigene Karte von
   letzter Woche.
3. **Eine frühere Antwort von dir ist keine Quelle.** Was du in einem
   vorherigen Gespräch formuliert hast, ist nicht dadurch bestätigt, dass es
   schon einmal dastand.
4. **Eine Layoutvorlage liefert die Gestaltung, nicht den Inhalt.** Aus einer
   bestehenden Karte übernimmst du Schritte nur, wenn sie zum aktuellen Prozess
   gehören und bestätigt sind.

## Nichts erfinden

Modulnamen, Masken, Feldnamen, Tastenkombinationen, Buchungsarten,
Berechtigungen, Freigaben — **nie ergänzen, immer erfragen.** Was belegt ist,
steht in `references/systemkatalog.md`. Eine erfundene Maske kostet den Werker
an der Maschine echte Zeit und die Karte ihre Glaubwürdigkeit.

**Ein ERP-Modul entscheidet nicht.** Es zeigt Informationen oder verarbeitet
Buchungen. Über einen betrieblichen Ablauf entscheidet eine Rolle.

**Und Angaben werden nicht von einem Vorgang auf einen anderen übertragen,**
nur weil es ähnlich klingt. Für das Umpacketikett etwa sind BARI, BARU,
Kontrollarbeitsgang und AG 300 ausdrücklich **nicht** bestätigt, obwohl sie für
die normale Etikettenbuchung belegt sind.

## Standardablauf und Ausnahme trennen

Eine Ausnahme darf nie wie ein regulärer Weg aussehen. Wenn die
Produktionsplanung im Einzelfall telefonisch eine Weiterproduktion anweist, ist
das eine Ausnahme — und wird als solche benannt, nicht als Freigabeweg
dargestellt.

Umgekehrt: Eine betriebliche Unterbrechung, die wirklich nötig ist, wird
deutlich benannt. Kein Beschönigen.

## Rollen richtig zuordnen

Die fünf Aufgabenarten liegen oft bei **verschiedenen** Rollen:

**Melden · Prüfen · Entscheiden · Ausführen · Dokumentieren**

Wer sie zusammenwirft, schreibt eine Karte, nach der niemand arbeiten kann.
Der belegte Rollenkatalog und die Grenzen je Rolle stehen in
`references/rollenkatalog.md`.

**Zwei Grenzen gelten immer:** Mitarbeitende entscheiden nicht, korrigieren
keine Bestände und reparieren nicht. Und keine Rolle bekommt eine Aufgabe
zugewiesen, die nicht beschrieben wurde.

## Der Pflichtaufbau

| Abschnitt | Pflicht? | Inhalt |
|---|---|---|
| Kopf | ja | `KIENBACHER AKADEMIE / [BEREICH]`, konkrete Frage als Titel, optional eine Zeile Erläuterung |
| Anlass | nein | Ein Satz: Wann wird die Karte gebraucht? |
| Hauptablauf | ja | Nummerierte Schritte mit kurzen Tätigkeitswörtern |
| Ausnahme | nein | Nur wenn fachlich relevant. **Kein pauschaler STOPP-Kasten** |
| **Wer macht was?** | **ja** | Eigener zweispaltiger Bereich. Rollennamen in den Schritten ersetzen ihn nicht |
| Abschlusskriterium | ja | „WEITERARBEITEN WENN" bei Unterbrechung oder Entscheidung, „FERTIG WENN" bei abgeschlossener Tätigkeit. Ein bis zwei prüfbare Kriterien |
| Fußzeile | ja | Karten-ID, Revision, Datum, Status, Verfasser, Prüfer, Freigeber |

## Verbotene Überschriften

- **„SOFORT MÖGLICH" und „ALTERNATIV MÖGLICH"** — waren dem Haus zu unklar.
  Eine zeitliche Reihenfolge darf nicht als freie Wahl erscheinen.
- **Ein pauschaler STOPP-Kasten auf jeder Karte.** Wer überall stoppt, stoppt
  nirgends.

## Bei Entscheidungen

- Eine **eindeutige** Frage, mit ja oder nein zu beantworten.
- Beide Wege beschriftet („JA", „NEIN") und **beide enden bei einer klaren
  Handlung oder Übergabe**.
- Für eine reine Arbeitsfolge **keine künstliche Verzweigung** einbauen.

## Lücken bleiben Lücken

Was nicht geklärt ist, wird eine **offene Frage** — sie steht im
Markdown-Zwilling neben der Karte, nie auf der Karte selbst. Eine unklare Stelle
als fertige Arbeitsanweisung darzustellen ist der schlimmste Fehler, den diese
Karten machen können.

Frag **gebündelt** nach, nicht einzeln. Die fünf Fragen, die fast immer reichen,
stehen am Ende von `references/systemkatalog.md`.

## Personendaten

Sobald eine Karte Personen berührt, gilt: **keine Gesundheitsdaten auf der
Karte und keine im Logbuch.** Die bestehende Karte zum Personalausfall macht es
richtig — Krankmeldung geht über den Verteiler an die Lohnverrechnung, aber
„keine Diagnose im Logbuch". Weise von dir aus darauf hin, wenn eine Karte in
diese Richtung läuft.

## Screenshots

Nur echte, vorliegende Screenshots. Keine ERP-Maske nach Vermutung nachbauen.
Wird einer verwendet: den relevanten Ausschnitt lesbar zeigen, die benötigten
Felder nummerieren, und die Nummern müssen zur Arbeitsfolge passen. Vor einer
Weitergabe auf vertrauliche Daten im Bild achten.

Ein Screenshot-Platzhalter ist nur in einem Entwurf sinnvoll. Er ersetzt keine
fertige Bedienungsanleitung.

## Bei einer Änderung

- Neue Revision als **neue Datei**. Frühere Fassungen bleiben erhalten.
- **Alle betroffenen Stellen anfassen:** Ablauf, Rollenbereich,
  Abschlusskriterium, gegebenenfalls Screenshot. Eine Karte mit geändertem
  Ablauf und altem Rollenbereich ist schlimmer als gar keine.
- Vor der Ausgabe prüfen, ob eine alte Fehlannahme noch irgendwo steht.
