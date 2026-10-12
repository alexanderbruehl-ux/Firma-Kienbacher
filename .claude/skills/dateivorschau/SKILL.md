---
name: dateivorschau
description: >-
  Projektuebergreifender Standard dieses Nutzers (Alexander Bruehl): bei jeder
  fuer Menschen relevanten Datei (PPTX/DOCX/XLSX/PDF/Bilder - Berichte,
  Vorlagen, Listen, Uebersichten), die in einem Projekt entsteht oder
  geliefert wird - nicht nur auf Nachfrage, nicht fuer Quellcode, Skripte
  oder Konfigurationsdateien. Baut eine eigenstaendige HTML-Vorschau: vollstaendiger
  scrollbarer Lese-Inhalt direkt aus der Datei (ganzes DOCX, alle PPTX-Folien,
  kein Rendering-Dienst noetig), zeigt alle relevanten Dateien des aktuellen
  Projekts zur Auswahl per Ordnerbaum (Ueberschrift "Dateien fuer Projekt: "
  plus Projektname), veroeffentlicht als Artifact, weil Claude Code/Cowork
  Office-Dateien nicht inline anzeigen. Immer nutzen bei
  .docx/.pptx/.xlsx/.pdf/Bild-Dateien, auch ungefragt - fehlende Vorschau war
  wiederholt ein Problem fuer diesen Nutzer.
---

# Eine allgemeine Datei-Vorschau bauen

Diese Skill nutzt **keinen externen Rendering-Dienst** (kein LibreOffice, kein
Konvertierungsserver). Grund: LibreOffice-Headless-Konvertierung ist in
vielen Sandbox-Umgebungen unzuverlaessig - `soffice --convert-to` kann ohne
verwertbare Fehlermeldung abbrechen, unabhaengig vom Inhalt. Und ein
eingebettetes `docProps/thumbnail.jpeg` in einer PPTX/DOCX ist haeufig nur
ein leerer Platzhalter, kein echtes Abbild - darauf ist kein Verlass.

Stattdessen liest das Werkzeug die Datei **strukturell selbst aus** und baut
daraus eine Vorschau:

## Werkzeug

```
python werkzeuge/vorschau_erzeugen.py datei1.pptx datei2.png ... --out vorschau.html --titel "..."
python werkzeuge/vorschau_erzeugen.py notes working source --out vorschau.html --titel "Dateien für Projekt: ..."
```

Argumente koennen einzelne Dateien **oder Ordner** sein. Ein Ordner wird
rekursiv nach relevanten Dateien durchsucht (`node_modules`, `.git` und
Aehnliches werden uebersprungen) - damit zeigt die Vorschau **das ganze
Projekt**, nicht nur die gerade frisch gelieferten Dateien.

- **Bilder** (`png`, `jpg`, `jpeg`, `gif`, `webp`, `svg`) werden direkt als
  `<img>` eingebettet - vollstaendige Ansicht, kein Ausschnitt.
- **PDF** wird ueber `<embed>` eingebettet - die meisten Browser rendern das
  nativ, inklusive eigenem Scrollen/Blaettern.
- **PPTX**: **alle Folien** werden aus den echten Shapes (Position,
  Fuellfarbe, Text, eingebettete Bilder) nachgebaut und untereinander
  scrollbar dargestellt - Werte direkt aus der Datei via `python-pptx`,
  keine Annahme uebers Layout. Skalierung ueber CSS Container Query Units
  (`cqw`), damit Schriftgroessen proportional zur Breite bleiben.
- **DOCX**: der **komplette Dokumentkoerper** (Ueberschriften, Absaetze,
  Tabellen) in Original-Reihenfolge via `python-docx`, scrollbar - keine
  Kuerzung auf einen Auszug, ausser bei sehr langen Dokumenten (Schutzlimit
  ~200.000 Zeichen, dann mit Hinweis).
- **Alles andere** (XLSX, ZIP, ...) sowie jede Datei, bei der das Parsen
  fehlschlaegt oder `python-pptx`/`python-docx` fehlt, bekommt eine Karte mit
  Dateityp und Groesse als Rueckfallebene - nie ein Fehler, nie eine leere
  Karte.

Diese Vorschau ist eine **vollstaendige Nur-Lese-Ansicht**, kein Editor:
man kann das ganze Dokument durchscrollen und lesen, aber nicht bearbeiten.
Komplexe Formatierung und Animationen fehlen trotzdem (kein echtes Rendering
der Originalsoftware). Wer die Vorschau auf dem jeweiligen Bildschirm zu
unhandlich findet oder bearbeiten/drucken will, laedt die Originaldatei ueber
den Button herunter.

## Ordnerbaum bei mehreren Dateien

Werden mehrere Dateien uebergeben, zeigt die Vorschau links einen
**Ordnerbaum** (Gruppierung ueber den jeweiligen Pfad relativ zum
Arbeitsverzeichnis) - Datei anklicken, rechts erscheint ihre vollstaendige
Ansicht samt Download-Button. Auf schmalen Bildschirmen (Handy) wird der Baum
durch eine Auswahlliste (Dropdown) ersetzt, gleiche Funktion. Bei genau einer
Datei entfaellt die Navigation und die Ansicht nimmt die volle Breite ein.

Jede Karte hat einen **Download-Button** (Data-URI, kein externer Link) -
funktioniert nur, wenn die HTML-Datei direkt geoeffnet wird (lokal oder per
Dateiversand), **nicht** in einer eingebetteten/sandboxed Ansicht wie einem
Artifact-Link: dort blockiert die Plattform von der Seite selbst
ausgeloeste Downloads. Fuer eine Artifact-Ansicht bleibt nur die
Ansicht selbst (Bilder/PDFs sichtbar), kein funktionierender Download-Button
fuer andere Dateitypen - das ehrlich so benennen, keinen toten Button zeigen.

## Was zaehlt als "relevante Datei" (und was nicht)

"Relevant" heisst hier: **fuer Menschen relevant** - etwas, das jemand lesen,
pruefen, ausdrucken oder weitergeben will. Das umfasst Word/Excel/PowerPoint/
PDF/Bilder: Berichte, Stellen-/Rollenbeschreibungen, Listen, Vorlagen,
Uebersichten, Auswertungen und Ähnliches.

**Ausdruecklich nicht gemeint sind Code-Dateien** - Quellcode (`.py`, `.js`,
`.ts`, `.go`, ...), Konfigurationsdateien (`.json`, `.yaml`, `.toml`, `.env`,
...), Skripte, Build-/Infrastruktur-Dateien. Auch wenn solche Dateien im
selben Projekt neu entstehen (z. B. das Werkzeug, das diese Vorschau selbst
erzeugt), loesen sie diese Skill nicht aus - sie sind technische Arbeitsmittel,
kein Lieferobjekt fuer den Nutzer. Diese Skill greift erst, sobald aus der
Arbeit ein fuer Menschen lesbares Ergebnis entsteht (z. B. das generierte
.docx), nicht fuer den Code, der es erzeugt hat.

## Standard-Ausgabeweg: als Artifact veroeffentlichen

**Das ist der Standardweg, nicht eine Option.** Claude Code und Claude Cowork
zeigen Office-Dateien (DOCX/PPTX/XLSX/PDF) nirgends inline an - weder im
Chat noch im Datei-/Code-Browser (der zeigt bei Binaerdateien nur
Rohbytes, das ist kein Fehler, sondern Absicht des Code-Browsers). Deshalb
gilt bei **jeder** Lieferung einer oder mehrerer solcher Dateien, in jedem
Projekt, auch ohne explizite Nachfrage:

1. `vorschau_erzeugen.py` **nicht nur auf die gerade erzeugten/gelieferten
   Dateien** anwenden, sondern auf die eigenen Ordner des aktuellen
   Projekts (z. B. `notes`, `working`, `source` - je nachdem, was dieses
   Repo/Projekt als seine Dateien definiert; `scripts`/Code-Ordner weglassen,
   das Werkzeug filtert Code ohnehin per Endung heraus). So sieht der Nutzer
   **alle** relevanten Projektdateien zur Auswahl, nicht nur die heute
   gelieferten. Ausgabe in eine Scratchpad-Datei (z. B. `vorschau.html`).
2. `--titel` immer im Format `"Dateien für Projekt: <Projektname>"` setzen,
   mit dem tatsaechlichen Namen des aktuellen Projekts (z. B. aus der
   CLAUDE.md oder dem Projektkontext) - nicht dem Repo-Namen und nicht dem
   Namen einer einzelnen Datei. Die Fenster-Ueberschrift uebernimmt diesen
   Titel direkt.
3. Die erzeugte HTML-Datei pruefen: sie darf (und wird im Normalfall) kein
   eigenes `<!DOCTYPE>`, `<html>`, `<head>` oder `<body>` enthalten - das
   Werkzeug erzeugt bereits ein Fragment, kompatibel mit dem
   Artifact-Skelett. Falls doch vorhanden, vor dem Publizieren entfernen.
4. Mit dem **Artifact**-Werkzeug veroeffentlichen (`action: "quickstart"`
   mit passendem `intent` vor der ersten Veroeffentlichung eines neuen
   Artifacts, danach `action: "publish"` mit `file_path` auf die
   Scratchpad-HTML). Das ist der Schritt, der die Vorschau tatsaechlich
   **inline sichtbar** macht - `SendUserFile` mit einer HTML-Datei oeffnet
   beim Nutzer nur einen Browser-Download-Dialog, keine eingebettete
   Ansicht. Spaetere Lieferungen in diesem Projekt aktualisieren dieselbe
   Artifact-URL (gleicher `file_path`/`url`), statt staendig neue Links zu
   erzeugen.
5. Die eigentlichen Originaldateien (DOCX/PPTX/...), die neu zur Lieferung
   gehoeren, zusaetzlich wie gewohnt per `SendUserFile` mitschicken, damit
   der Nutzer sie herunterladen, oeffnen und bearbeiten kann - das Artifact
   ersetzt das Original nicht, es macht nur den Inhalt auf einen Blick
   sichtbar.
6. Dem Nutzer kurz mitteilen, dass Download-Buttons innerhalb der
   Artifact-Ansicht inaktiv sind (siehe oben) und die Originaldateien dafuer
   extra mitgeschickt wurden.

## Dateinamen

Immer den vollstaendigen, aussagekraeftigen Dateinamen verwenden (siehe
`CLAUDE.md` im Repo-Wurzelverzeichnis) - der Download-Button nutzt ihn direkt
als Dateiname beim Speichern.

## Verhaeltnis zu `regelkarten-vorschau`

- **`dateivorschau`** (diese Skill): allgemein, jeder Dateityp, naeherungsweise
  Inhaltsvorschau plus Download.
- **`regelkarten-vorschau`** (im Regelkarten-Plugin): nur fuer
  Kienbacher-Regelkarten-PPTX, baut das Layout millimetergenau nach dem
  Kienbacher-CI nach (Track-Schrift, exakte Raster-Werte) - fuer die genaue
  Sichtpruefung einer Karte vor der Freigabe. Fuer alles ausserhalb der
  Regelkarten oder wenn nur ein grober Anhaltspunkt reicht, diese allgemeine
  Skill verwenden.

## Voraussetzungen

- Python 3.11 oder neuer
- `pip install python-pptx python-docx` fuer die Inhaltsvorschauen von PPTX
  und DOCX. Ohne diese Pakete funktioniert das Werkzeug weiterhin (Bilder,
  PDF, Download bleiben unveraendert) - PPTX/DOCX fallen dann auf die
  Dateityp-Karte zurueck statt abzubrechen.
- Sonst nichts - kein PowerPoint, kein LibreOffice, kein Browser-Rendering
  auf der Erzeugerseite noetig.
