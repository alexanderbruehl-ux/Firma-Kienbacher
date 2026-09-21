---
name: regelkarten-vorschau
description: Baut aus einer oder mehreren fertigen Regelkarten-PPTX eine einzelne, eigenstaendige HTML-Vorschau zum Ansehen und Weitergeben - originalgetreu in Position, Farbe und Schrift, mit Reiter zum Umschalten zwischen mehreren Karten. Nutze diese Skill, wenn jemand eine Karte "ansehen" will ohne PowerPoint, eine Vorschau mehrerer Karten nebeneinander braucht, oder Karten an Kolleginnen und Kollegen weitergeben will, die keinen Claude-Zugang haben.
user-invocable: false
---

# Eine Vorschau bauen

Diese Skill ersetzt **nicht** die Sichtpruefung aus `regelkarten-erzeugen` (das
gerenderte Bild vor dem Melden einer Karte als fertig). Sie ist ein
zusaetzliches, schnelles Mittel, eine oder mehrere bereits erzeugte Karten
**anzusehen und weiterzugeben**, wenn kein PowerPoint zur Hand ist oder die
Karte an jemanden ohne Claude-Zugang gehen soll.

## Werkzeug

```
python werkzeuge/vorschau_erzeugen.py RK-012.pptx RK-013.pptx ... --out vorschau.html --titel "..."
```

Liest Position, Farbe, Schrift und Text **direkt aus den PPTX-Dateien** (nicht
aus der JSON-Definition) - die Vorschau zeigt also exakt das, was der
Generator tatsaechlich geschrieben hat, nicht die Absicht dahinter.

Track.ttf und das Logo werden aus `regelkarten-erzeugen/assets/` als
Data-URI eingebettet. Arial bleibt Systemschrift, genau wie auf der echten
Karte - die Datei bleibt dadurch klein und lauffaehig auf jedem Rechner mit
Windows-Standardschriften, ohne dass zusaetzliche Schriftdateien mitgeschickt
werden muessen.

## Zwei Wege, sie bereitzustellen

1. **Als Artifact veroeffentlichen** (Publish-Werkzeug dieser Umgebung) -
   praktisch fuer die schnelle Ansicht und Rueckmeldung im Gespraech. Ein
   Artifact ist **privat**, bis der Ersteller es ueber das Share-Menue der
   Seite freigibt - das kann Claude nicht selbst umstellen. Downloads, die
   die Seite selbst ausloest (auch Data-URI-Links), sind in der
   Artifact-Ansicht **blockiert** - dafuer mit `--ohne-download` bauen, sonst
   haengen dort tote Download-Buttons.
2. **Die HTML-Datei selbst herausgeben** (`SendUserFile` oder aequivalent,
   ohne `--ohne-download`) - die Datei ist vollstaendig eigenstaendig
   (Schrift, Logo und je Karte die PPTX als Download-Link eingebettet, keine
   externen Ressourcen) und laesst sich direkt per E-Mail, Chat oder ueber
   das Firmen-OneDrive weiterreichen. Jede und jeder oeffnet sie im Browser,
   ganz ohne Claude-Konto, und kann die PPTX herunterladen. Das ist der
   Standardweg fuer die Weitergabe an Kolleginnen und Kollegen.

**Immer beide Wege anbieten**, wenn eine Vorschau fuer mehr als eine Person
gedacht ist: das Artifact fuer die schnelle Ruecksprache, die Datei fuer die
Verteilung.

## Bearbeiten und Drucken

Kein Inline-Druck in der Vorschau. Serverseitiges PPTX-Rendering ist in
dieser Umgebung nicht verlaesslich moeglich (LibreOffice-Headless-Konvertierung
bricht ohne verwertbare Fehlermeldung ab, unabhaengig vom Inhalt), und ein
Druckversuch ueber `window.print()` war in einer eingebetteten Ansicht
blockiert. Stattdessen: **Download-Button je Karte**, Bearbeiten und Drucken
passiert in PowerPoint selbst - zuverlaessiger und ehrlicher als ein
Nachbau, der in Randfaellen abweichen koennte. Fuer Dateitypen ausserhalb
von Regelkarten-PPTX (oder wenn nur Download ohne PPTX-Nachbau noetig ist)
die allgemeine Skill `dateivorschau` (Repo-Wurzelverzeichnis
`.claude/skills/`) verwenden - selbes Prinzip, ohne die
Regelkarten-spezifische Shape-Rekonstruktion.

## Zusaetzlich bei jeder fertigen Karte

Neben der Vorschau immer auch die **Original-PPTX** (und, falls vorhanden,
den Markdown-Zwilling) als Datei herausgeben - die Vorschau ist ein Abbild,
keine bearbeitbare Fassung. Wer eine Karte pruefen oder aendern will, braucht
die PPTX.

## Wenn sich am Plugin-Design etwas aendert

Diese Skill liest `assets/Track.ttf` und `assets/logo_weiss.png` aus
`regelkarten-erzeugen` mit. Aendert sich dort das Logo oder die Schrift, muss
hier nichts angepasst werden - der Pfad ist relativ zum Plugin, nicht
kopiert.

## Voraussetzungen

- Python 3.11 oder neuer, `pip install python-pptx`
- Sonst nichts - kein PowerPoint, kein LibreOffice, kein Browser-Rendering
  auf der Erzeugerseite noetig.
