# Meisterwerke-Logo – Original-Vektordaten

**Status (02.10.2026):** Das Logo stammt aus der **Original-Reinzeichnung** (`original/meisterwerke_logo_RZ_ohne_claim_pfad.dwg`,
AutoCAD R14, Signet + Wortmarke ohne Claim, Schrift in Pfaden). Es ersetzt die vorläufige Nachzeichnung aus der Bilddatei.

| Datei | Inhalt |
|---|---|
| `original/meisterwerke_logo_RZ_ohne_claim_pfad.dwg` | Original-Vektordatei (unverändert) |
| `logo_aus_dwg.py` | DWG → `mw_trace.json`, SVGs, Vorschau (`pip install ezdwg ezdxf matplotlib`) |
| `mw_trace.json` | Konturen von Signet und Wortmarke (Einheit: DWG-Zeichnungseinheiten, Gesamtbreite 453,46; y nach unten) |
| `Meisterwerke_Logo.svg` / `…_Signet.svg` / `…_Wortmarke.svg` | SVG-Ausgaben |
| `mwlogo.py` | Laden/Zeichnen (Position, Breite, Drehung) für die Konzept-Renderer und das CAD |
| `Logo_hell.png`, `Logo_dunkel.png` | Vorschau |
| `trace_logo.py` | **überholt** – frühere Vektorisierung (Potrace) aus der Bilddatei „LOGO MW.jpg“ |

Hinweise zur DWG: Die Datei enthält die Umrisse doppelt (gefüllte Flächen/HATCH und Splines). Die Splines werden von `ezdwg`
teils falsch gelesen (feine Striche) – verwendet werden nur die HATCH-Konturen (16 Pfade: 1 Signet, 15 Wortmarke inkl. Innenflächen).
Das Signet ist ein Polygon mit 16 Ecken. Für Fertigungsdaten die Original-DWG verwenden, nicht die abgeleiteten Dateien.

Proportionen laut Original (Gesamtmarke 4,213 : 1): Signet 10,6 % der Logobreite, 1,21-fache Höhe der Wortmarke.
Die frühere Nachzeichnung hatte das Signet zu groß (14,1 %, 1,55-fach).

Position auf der Blende (Stand 30.09.2026): parallel zur Unterkante (3,7°), Logounterkante 8 mm über
der Blendenunterkante, Mittelachse (um 3,7° gekippt) verlängert durch den 100er-Mittelpunkt,
Mitte (291,3 | 40,9) mm, Breite 115 mm (Höhe ≈ 27,3 mm, Signet 12,2 × 9,9 mm).
