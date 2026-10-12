---
name: dateivorschau
description: Baut aus beliebigen Dateien (PPTX, DOCX, XLSX, PDF, Bilder, ...) eine eigenstaendige HTML-Uebersicht mit Download-Button je Datei - unabhaengig vom Regelkarten-Projekt. Bilder und PDFs werden inline angezeigt, PPTX/DOCX bekommen eine aus dem tatsaechlichen Inhalt nachgebaute Vorschau (erste Folie bzw. Textauszug), alles andere eine Karte mit Dateityp, Groesse und Download zum Oeffnen im Originalprogramm. Nutze diese Skill, wenn jemand mehrere Dateien "ansehen" oder an andere weitergeben will, ohne dass ein Rendering-Dienst noetig ist.
user-invocable: false
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
```

- **Bilder** (`png`, `jpg`, `jpeg`, `gif`, `webp`, `svg`) werden direkt als
  `<img>` eingebettet - vollstaendige Vorschau im Browser.
- **PDF** wird ueber `<embed>` eingebettet - die meisten Browser rendern das
  nativ.
- **PPTX**: die erste Folie wird aus den echten Shapes (Position, Fuellfarbe,
  Text, eingebettete Bilder) als kleine Facsimile-Vorschau nachgebaut -
  Werte direkt aus der Datei via `python-pptx`, keine Annahme uebers Layout.
  Skalierung ueber CSS Container Query Units (`cqw`), damit Schriftgroessen
  proportional zur Kartenbreite bleiben.
- **DOCX**: ein Textauszug (Ueberschriften/Absaetze, ca. 700 Zeichen) aus dem
  Dokumentkoerper via `python-docx`.
- **Alles andere** (XLSX, ZIP, ...) sowie jede Datei, bei der das Parsen
  fehlschlaegt oder `python-pptx`/`python-docx` fehlt, bekommt eine Karte mit
  Dateityp und Groesse als Rueckfallebene - nie ein Fehler, nie eine leere
  Karte.

Diese Vorschauen sind **Anhaltspunkte, kein Ersatz** fuer das Original:
mehrseitige PPTX zeigen nur die erste Folie, DOCX nur einen Auszug, Animationen
und komplexe Formatierung fehlen. Bearbeiten, Drucken und die vollstaendige
Ansicht passieren im jeweiligen Programm.

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
