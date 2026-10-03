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
Breite **105 mm** (Stand 02.10.2026, vorher 115; Schrift 8 mm über der Unterkante).
Kleinster Abstand Logo → Rand des 100er-Ausschnitts: **7,2 mm** (der Diamantschnitt-Konus von 2 mm Breite liegt davon noch abzuziehen).

## Claim „MAGNA OPERA OF INTERIOR & SOUND“ (regelbasierter Entwurf, 02.10.2026)

Der Claim liegt nur als Raster vor (GIF, Claim-Höhe 42 px, nur Tinte/transparent) und dort mit dem **alten, grammatisch falschen Text
„OPUS MAGNA …“** (*opus* ist Einzahl, *magna* Mehrzahl). Richtig ist die Mehrzahl **„MAGNA OPERA“** (ebenso richtig: „OPERA MAGNA“).
Alle Buchstaben des neuen Claims kommen im alten vor. Die Buchstaben sind **nicht mehr aus dem Pixelrauschen nachgezeichnet**, sondern nach
**Regeln des Meisterwerke-Schriftzugs konstruiert** (`claim_regeln.py`, Einheiten: Kappenhöhe = 1000), jeder Buchstabe wurde einzeln gegen das
(gemittelte) Pixelbild geprüft. `logo_claim_aus_bild.py` setzt sie mit dem Buchstabenabstand des GIF zusammen.

**Gemeinsame Regeln** (vom I abgeleitet, gelten für alle Buchstaben):
- **Stamm/Strich-Enden laufen kubisch aus** (t³ über 390 Einheiten, +20,5 am Ende; oben mehr nach links, unten mehr nach rechts: Punktsymmetrie).
- **Flache Enden haben die Delle des I** (3 Einheiten tief; unten um 180° gedreht), auf die Endbreite normiert.
- Stamm 113,8; Haarlinie ca. 70 (im GIF: Querbalken A 49, rechter N-Stamm 61); Querstriche und Bögen aus Haarlinie und dicker Wand.
- Möglichst nur **gerade Kanten** und **wenige exakte Béziers** statt Kurvenanpassung (N, A: Kanten exakt; Auslauf-Kurven sind exakt kubisch).

**Buchstaben:** I, E, F, T (aus dem Schriftzug-E/I/T abgeleitet, E-Arme +10 %, T −12 %); R, P (Schriftzug-R: Steg höher, Bogen weiter, Bein aus zwei geraden
Kanten mit Fuß-Auslauf, Bogenwand ≥ 65); D (E-Stamm + Bogen); N (punktsymmetrisch, Diagonale 42,8°); A (zwei parallele Streifen 72/130, 23,2°, Balken);
U (I-Stamm + Haarlinien-Stamm + Bogen); O (zwei Superellipsen); S, G, & (Striche mit variabler Breite entlang einer geglätteten Mittellinie,
Skelett des gemittelten GIF-Buchstabens, per Flächenabgleich nachgeschliffen). **Das M stammt direkt aus dem Vektor-Schriftzug** (43,8 px breit; das M im GIF ist 47 px).

- Neusatz mit dem Buchstabenabstand des GIF (Kontrolle am alten Text: mittlere Abweichung 1,6 px bei 42 px Buchstabenhöhe), mittig zum Schriftzug;
  Abstand zur Schrift und Höhe wie im GIF. Claim-Breite ca. 88 % des Schriftzugs (GIF: 84,8 %, ein Zeichen mehr).
- Signet und Schriftzug sind unverändert; in `mw_trace.json` kommen nur `claim`, `bbox_claim`, `claim_text` hinzu.
- Rekonstruktion: `python logo_claim_aus_bild.py` (benötigt `pillow numpy scipy scikit-image matplotlib shapely`).

**Grenzen:** Das ist eine Rekonstruktion aus einem 42-px-Raster, keine Originalzeichnung. Die Pixelbilder lassen etwa ±0,5 px (± 12 Einheiten) Spielraum;
Details wie Spitzen, Serifen und Balkenstärke sind Interpretation (offen: Balken-A 49 vs. Haarlinie 70, Überhang runder Buchstaben, Spitzenform). Bei normaler
Größe (auf der Blende ca. 3 mm Schrifthöhe) nicht sichtbar. Für Fertigungsdaten und Großformate die Original-Vektordatei mit dem richtigen Claim beschaffen.
