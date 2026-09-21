# Regelkarten-Rudi einbinden

Dieses Archiv ist ein vollstaendiger Claude-Code-Marketplace mit einem Plugin:
`regelkarten` (Ansprache: "Rudi").

## 1. Entpacken

Den Ordner `regelkarten-kienbacher` an einen festen Platz legen, zum Beispiel
`C:\Claude\regelkarten-kienbacher`. Der Pfad darf sich spaeter nicht aendern -
er steht in den Einstellungen.

## 2. Einbinden

In einer interaktiven Claude-Code-Sitzung:

    /plugin marketplace add C:\Claude\regelkarten-kienbacher
    /plugin install regelkarten@regelkarten-kienbacher

Alternativ von Hand in `%USERPROFILE%\.claude\settings.json`:

    {
      "enabledPlugins": {
        "regelkarten@regelkarten-kienbacher": true
      },
      "extraKnownMarketplaces": {
        "regelkarten-kienbacher": {
          "source": {
            "source": "directory",
            "path": "C:\Claude\regelkarten-kienbacher"
          }
        }
      }
    }

## 3. Voraussetzungen fuer das Erzeugen der Karten

- Python 3.11 oder neuer
- `pip install python-pptx fonttools`
- Arial (auf Windows immer vorhanden)
- PowerPoint - nur fuer die Sichtpruefung der fertigen Karte

## 4. Arbeitsordner

Der Generator sucht selbst den Ordner, in dem `karten/` und `register/` liegen.
Wer neu anfaengt, legt beide Ordner im gewuenschten Projektverzeichnis an und
startet Claude Code von dort.

## 5. Schrift Track

`skills/regelkarten-erzeugen/assets/Track.ttf` liegt im Plugin, weil der
Generator die Textbreiten dagegen misst. Zum **Bearbeiten** der fertigen PPTX
muss Track auf dem jeweiligen Rechner installiert sein - das gehoert ueber die
IT ausgerollt und ist vorher lizenzrechtlich zu klaeren. Fehlt die Schrift,
ersetzt PowerPoint sie durch Arial; das Layout bleibt gueltig.

## 6. Loslegen

    /regelkarte

oder einfach "Rudi" ansprechen.
