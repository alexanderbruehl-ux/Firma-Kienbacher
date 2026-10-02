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
| `Meisterwerke_Logo.pdf` | Vektor-PDF des Gesamtlogos (ohne Claim) |
| `Meisterwerke_Logo_mit_Claim.svg` / `.pdf`, `Logo_mit_Claim_hell.png` / `_dunkel.png` | Logo **mit Claim** „MAGNA OPERA OF INTERIOR & SOUND“ (Entwurf, siehe unten); PNG 6000 px |
| `logo_claim_aus_bild.py`, `curvefit.py` | Claim aus der Rasterdatei rekonstruieren (`pip install pillow numpy scipy scikit-image matplotlib`) |
| `original/meisterwerke_logo_mit_claim_RASTER.gif` | Rasterquelle mit dem ALTEN Claim „OPUS MAGNA …“ (1733 × 864 px) |
| `Logo_hell.png`, `Logo_dunkel.png` | Vorschau, 6000 px Breite |
| `Vergleich_Signet_alt_neu.png` | Prüfbild: Signet neu (gefüllt) über früherer Nachzeichnung (rot) und Original-DWG (grau gestrichelt) |
| `trace_logo.py` | **überholt** – frühere Vektorisierung (Potrace) aus der Bilddatei „LOGO MW.jpg“ |

Hinweise zur DWG: Die Datei enthält die Umrisse doppelt (gefüllte Flächen/HATCH und Splines). Die Splines werden von `ezdwg`
teils falsch gelesen (feine Striche) – verwendet werden nur die HATCH-Konturen (16 Pfade: 1 Signet, 15 Wortmarke inkl. Innenflächen).
Das Signet ist ein Polygon mit 16 Ecken. Für Fertigungsdaten die Original-DWG verwenden, nicht die abgeleiteten Dateien.

**Signet-Vergrößerung (02.10.2026, Wunsch):** Das obere M ist gegenüber der Original-DWG um den Faktor **1,3035** vergrößert
(`SIGNET_FAKTOR` in `logo_aus_dwg.py`; `1.0` = Original). Gleichmäßige Skalierung um Mitte und Unterkante des Signets, die Form bleibt wie
im Original. **Der Schriftzug ist unverändert** (Pfade identisch zur DWG), ebenso Abstand Signet–Schrift (36,3 Einheiten) und Mittelachse.
Grund: Die frühere Nachzeichnung hatte das Signet größer als das Original (14,1 % der Logobreite, 1,55-fache Wortmarkenhöhe; Original: 10,6 %, 1,21-fach).
Mit Faktor 1,3035 liegt das Signet bei 13,8 % bzw. 1,58-fach, also innerhalb von ca. 2 % der früheren Darstellung.
Gesamtmarke: Seitenverhältnis 3,794 : 1 (Original-DWG 4,213 : 1).

Position auf der Blende (Stand 30.09.2026): parallel zur Unterkante (3,7°), Logounterkante 8 mm über
der Blendenunterkante, Mittelachse (um 3,7° gekippt) verlängert durch den 100er-Mittelpunkt,
Breite 115 mm (Höhe ≈ 30,3 mm, Signet 15,9 × 12,9 mm), Schriftzug-Unterkante wie bisher; Logo-Mitte (291,2 | 42,1) mm.
Kleinster Abstand Logo → Rand des 100er-Ausschnitts: 4,6 mm (der Diamantschnitt-Konus von 2 mm Breite liegt davon noch abzuziehen).

## Claim „MAGNA OPERA OF INTERIOR & SOUND“ (Entwurf, 02.10.2026)

Der Claim liegt nur als Raster vor (GIF, Claim-Höhe 42 px, nur Tinte/transparent) und dort mit dem **alten, grammatisch falschen Text
„OPUS MAGNA …“** (*opus* ist Einzahl, *magna* Mehrzahl). Richtig ist die Mehrzahl **„MAGNA OPERA“** (ebenso richtig: „OPERA MAGNA“).
Alle Buchstaben des neuen Claims kommen im alten vor. `logo_claim_aus_bild.py`:
- Buchstaben einzeln rekonstruiert: mehrfach vorkommende Exemplare (O 4×, N 3×, A/U/S/I/R je 2×) auf Teilpixel genau übereinandergelegt und gemittelt,
  Kontur geglättet, Ecken aus den Schnittpunkten der Kanten, nahezu gerade Kanten als Geraden, Rundungen mit wenigen kubischen Béziers (`curvefit.py`).
- **Das M stammt direkt aus dem Vektor-Schriftzug** (auf Claim-Höhe skaliert, 43,8 px breit; das M im GIF ist 47 px breit und kräftiger).
- Neusatz mit dem Buchstabenabstand des GIF (Kontrolle am alten Text: mittlere Abweichung 1,6 px bei 42 px Buchstabenhöhe), mittig zum Schriftzug;
  Abstand zur Schrift und Höhe wie im GIF. Claim-Breite 87,4 % des Schriftzugs (GIF: 84,8 %, ein Zeichen mehr).
- Signet und Schriftzug sind unverändert; in `mw_trace.json` kommen nur `claim`, `bbox_claim`, `claim_text` hinzu.

**Grenzen:** Das ist eine Rekonstruktion aus einem 42-px-Raster, keine Originalzeichnung. Bei normaler Größe (auf der Blende ca. 3 mm Schrifthöhe) nicht
sichtbar, in starker Vergrößerung bleiben leichte Unregelmäßigkeiten (z. B. in U, N, D, &). Für Fertigungsdaten und Großformate die Original-Vektordatei
mit dem richtigen Claim beschaffen.

