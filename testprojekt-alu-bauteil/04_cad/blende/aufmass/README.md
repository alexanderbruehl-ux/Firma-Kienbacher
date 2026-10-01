# Aufmaß Schwalbennester – Außenkontur links/rechts anpassen

Die Öffnungen in den Schwalbennestern sind herstellerseitig nicht identisch (angezeichnet und zugeschnitten mit Schablone,
dadurch Winkel- und Maßfehler). Darum wird jede Blende einzeln an ihre Öffnung angepasst. Basis ist die eingefrorene
Soll-Kontur (CAD, Spalt 2,0 mm, Überstand 17,5 mm).

## Ablauf

1. **Prüfschablone drucken:** `zeichnungen/Pruefschablone_<seite>_1zu1.pdf` (540 × 290 mm, Plotter) oder
   `…_A4_Kacheln.pdf` (6 × A4 quer, mit Passkreuzen und 15 mm Überlappung). Immer mit 100 % bzw.
   „Tatsächliche Größe“ drucken und das 100-mm-Kontrollmaß nachmessen.
2. **Schablone auflegen:** auf den Korpusdeckel in der Öffnung, die Kreise auf die Treiberausschnitte ausrichten.
3. **Messen:** an M1–M6 den Spalt zwischen Schablonenkante und Innenkante der Edelstahleinfassung messen
   (Fühlerlehre bzw. Endmaße). Die Lage der Messstellen zeigt `zeichnungen/Aufmassskizze_<seite>.png`.
   - M1/M2: oben, von links nach rechts
   - M3/M4: unten, von links nach rechts
   - M5/M6: schräge Rahmenkante, von unten nach oben
   - Die Überstandskante liegt an der offenen Staufachseite und wird nicht gemessen.
4. **Werte eintragen** in `aufmass_<seite>.json`, in mm. `null` heißt Sollwert 2,0.
5. **Rechnen:**
   - `python3 blende_aufmass.py links|rechts|beide`: ca. 4 min pro Seite.
   - `--ohne-step` erzeugt nur Kontur und DXF.

## Korrektur

Jede vermessene Kante wird als Gerade durch ihre beiden korrigierten Messpunkte neu bestimmt. Der Punkt wird um
(gemessener Spalt − 2,0) nach außen verschoben, die neuen Ecken ergeben sich als Schnittpunkte der Kanten. Damit
sind Parallelverschiebung (Maßfehler) und Verdrehung (Winkelfehler) jeder Kante erfasst. Bohrbild, Logo, Magnete und
Nut bleiben an den Treibern ausgerichtet, nur die Außenkontur ändert sich.

## Ausgaben

| Datei | Inhalt |
|---|---|
| `zeichnungen/Aufmassskizze_<seite>.png` | Skizze mit Messstellen und Feldern für die Messwerte |
| `zeichnungen/Pruefschablone_<seite>_1zu1*.pdf` | 1:1-Schablone (ganz bzw. A4-Kacheln) |
| `zeichnungen/Kontur_<seite>.dxf` | Layer KONTUR (nach Aufmaß), KONTUR_SOLL, TREIBER, MAGNETE, MESSSTELLEN, Ansicht mm |
| `zeichnungen/Kontur_<seite>.png/.json` | Vorschau Soll vs. angepasst, Eckkoordinaten (Ansicht und global) |
| `step/Blende_<seite>.step.zip` | extrudierter 3D-Volumenkörper (STEP AP214, ca. 28 MB entpackt) |
| `zeichnungen/STEP_Kontrolle_Schnitte.png` | Kontrollschnitte durch beide STEP-Dateien |

- **Koordinaten:** STEP und `kontur_global` liegen im Koordinatensystem der Fusion-Lautsprechermodelle,
  Blendenvorderseite z = 145. Die Blende passt damit direkt in die Baugruppe.
- **Rechte Seite:** Kontur und Bohrbild sind gespiegelt, Logo und Hochtöner-M bleiben lesbar.
  Sie wird per Kabsch-Einpassung auf die Treiber und Magnete des rechten Korpus gesetzt (Restfehler 0,07 mm).
- **Stand:** Die STEP-Dateien sind die Soll-Konturen (noch kein Aufmaß eingetragen). Nach dem Messen
  `beide` erneut ausführen.

Das Logo ist vorläufig (Nachzeichnung) und wird durch die Original-Vektordatei ersetzt.
