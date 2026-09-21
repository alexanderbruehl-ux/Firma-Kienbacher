---
name: dateivorschau
description: Baut aus beliebigen Dateien (PPTX, DOCX, XLSX, PDF, Bilder, ...) eine eigenstaendige HTML-Uebersicht mit Download-Button je Datei - unabhaengig vom Regelkarten-Projekt. Bilder und PDFs werden inline angezeigt, alles andere bekommt eine Karte mit Dateityp, Groesse und Download zum Oeffnen im Originalprogramm. Nutze diese Skill, wenn jemand mehrere Dateien "ansehen" oder an andere weitergeben will, ohne dass ein Rendering des Originalformats noetig ist.
user-invocable: false
---

# Eine allgemeine Datei-Vorschau bauen

Anders als die projektspezifische `regelkarten-vorschau` (die PPTX-Shapes
Punkt fuer Punkt nachbaut) macht diese Skill **keinen Rendering-Versuch** des
Originalformats. Grund: LibreOffice-Headless-Konvertierung ist in dieser
Umgebung unzuverlaessig - `soffice --convert-to` bricht bei jeder PPTX ohne
verwertbare Fehlermeldung ab (getestet auch mit einer trivialen
Ein-Zeilen-Datei), unabhaengig vom Inhalt. Ein Nachbau wie bei den
Regelkarten lohnt sich nur, wenn ein Layout wirklich pixelgenau geprueft
werden muss - fuer alles andere ist "Original zum Download anbieten"
robuster und ehrlicher als ein Nachbau, der abweichen koennte.

## Werkzeug

```
python werkzeuge/vorschau_erzeugen.py datei1.pptx datei2.png ... --out vorschau.html --titel "..."
```

- **Bilder** (`png`, `jpg`, `jpeg`, `gif`, `webp`, `svg`) werden direkt als
  `<img>` eingebettet - vollstaendige Vorschau im Browser.
- **PDF** wird ueber `<embed>` eingebettet - die meisten Browser rendern das
  nativ.
- **Alles andere** (PPTX, DOCX, XLSX, ZIP, ...) bekommt eine Karte mit
  Dateityp und Groesse, keine Inhaltsvorschau. Bearbeiten, Drucken und
  genaues Ansehen passiert im jeweiligen Programm (PowerPoint, Word, Excel,
  ...), nicht im Browser.

Jede Karte hat einen **Download-Button** (Data-URI, kein externer Link) -
funktioniert nur, wenn die HTML-Datei direkt geoeffnet wird (lokal oder per
Dateiversand), **nicht** in einer eingebetteten/sandboxed Ansicht wie einem
Artifact-Link: dort blockiert die Plattform von der Seite selbst
ausgeloeste Downloads. Fuer eine Artifact-Ansicht bleibt nur die
Ansicht selbst (Bilder/PDFs sichtbar), kein funktionierender Download-Button
fuer andere Dateitypen - das ehrlich so benennen, keinen toten Button zeigen.

## Dateinamen

Immer den vollstaendigen, aussagekraeftigen Dateinamen verwenden (siehe
`CLAUDE.md` im Repo-Wurzelverzeichnis) - der Download-Button nutzt ihn direkt
als Dateiname beim Speichern.

## Verhaeltnis zu `regelkarten-vorschau`

- **`dateivorschau`** (diese Skill): allgemein, jeder Dateityp, kein
  Rendering-Versuch, nur Anzeige (wo trivial) plus Download.
- **`regelkarten-vorschau`** (im Regelkarten-Plugin): nur fuer
  Kienbacher-Regelkarten-PPTX, baut das Layout aus den PPTX-Shapes 1:1 nach
  (Position, Farbe, Schrift) - fuer die genaue Sichtpruefung einer Karte vor
  der Freigabe. Fuer alles ausserhalb der Regelkarten diese allgemeine Skill
  verwenden.
