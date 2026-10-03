# Übergabe: Alu-Blende „Alassio Design“ (Frauscher 650 Alassio, Schwalbennest, Teak-Fach) – Letztstand 03.10.2026

Alle Maße in mm. Antworten/Doku deutsch. Dieses Paket enthält den kompletten Projektordner `testprojekt-alu-bauteil/`.

## 1. Was ist das Bauteil
Alu-Blende (Dicke 8,5, hochglanzpoliert) mit drei Lochfeldern (Ø118,2 TMT, Ø156,2 Sub, Ø46,2 Hochtöner), Meisterwerke-Logo (Frästiefe 0,5) mit Abstand zum 100er-Ausschnitt und Signet-M im Hochtöner-Feld.
Das **CadQuery-Skript ist die Quelle der Wahrheit**; Fusion bekommt das STEP.

## 2. Wo liegt was (in der Reihenfolge, in der man es braucht)
| Zweck | Datei |
|---|---|
| **Fusion: fertiges 3D-Modell** | `04_cad/blende/export/Blende_2A35M.step` (Volumen 410,1 cm³, Masse ca. 1107 g, 1443 Bohrungen) |
| Fusion-Skript (STEP laden, Material, Ansicht, Volumenprüfung; **ungetestet**) | `05_fusion/fusion_blende.py` |
| CAD-Quelle (Parameter oben im Skript) | `04_cad/blende/blende_2a35.py` → `python3 blende_2a35.py` erzeugt STEP/STL neu |
| Netz (Blender/Vorschau) | `04_cad/blende/export/Blende_2A35M.stl`, `Szene_*.stl` (Fach, Korpus, Rumpf, Einfassung) |
| Logo-DXF für Fusion (Logo 105 mm + 100er-Kreis) | `04_cad/blende/dxf/Logo_Abdeckung_100er.dxf` (+ `_Vorschau.png`) |
| Hochtöner-Lochliste (101 Bohrungen, Feldkoordinaten) | `03_konzepte/akustik/ht_neu_loecher.json` (`holes: [x,y,d]`, `dy` = M-Versatz) |
| Fertigungszeichnung A3 (Entwurf, noch **ohne Bemaßung**) | `06_zeichnung/Zeichnung_Blende_2A35M.pdf/.png`, Quelle `zeichnung_blende.py` |
| Renderings (Letztstand) | `05_render/Blende_2A35M_{gesamt,detail,hochtoener}_freigabe.png`, Quelle `render_blende.py` (Blender) |
| Aufmaß/Einbauschnittstelle | `04_cad/blende/aufmass/` (Konturen links/rechts als DXF/JSON, Prüfschablonen 1:1, STEP Blende links/rechts) |
| Frequenzgang-Plots | `03_konzepte/akustik/Frequenzplot_Hochtoener_neu.png` (neu: −0,4/−1,4/−2,7/−4,0 dB bei 5/10/15/20 kHz), `Frequenzplot_Sonnenblume.png` (bisher) |
| **Logos** | Ordner `LOGOS/` (Kopie des Letztstands) und `03_konzepte/logo/` (mit Quellen) |
| Fertigungsregeln | `docs/FERTIGUNGSRICHTLINIEN_ALU.md` |

## 3. Festgelegte Konstruktionsdaten (Stand freigegeben)
- **Hochtöner Ø46,2**: Restwand 1,5; Sechseckraster Ø2,5, Steg ≥ 0,8; M 28 mm breit, Achse senkrecht, 1,5 mm höher; 101 Bohrungen (Ø2,5 ×98, Ø2,0 ×1 in der Senke oben im M, Ø1,5 ×2 an den oberen Spitzen); je 4 Löcher parallel zu den M-Schenkeln; Außenrand „entspannt“; offener Querschnitt 39,9 %.
- **Sub Ø156,2 / TMT Ø118,2**: Haut **gestuft** von hinten mit 45°-Fräser: Mitte **2,2** / ab 0,42·R **2,85** / ab 0,72·R **3,5** mm; Flankenversatz = Stufenhöhe; Hohlkehle R2,5 zur Zylinderfläche. Bohrungen Ø2,0/2,5/3,0/3,5 (Sub 857, TMT 485). Frontabsenkung 0,6.
- **Logo**: Breite 105 mm, parallel zur Unterkante (3,7°), 8 mm über der Unterkante, Abstand zum 100er-Ausschnitt 7,2 mm (ohne 2-mm-Diamantschnitt-Konus). Signet-M 1,3035× gegenüber Original-DWG, Wortmarke unverändert.
- **Claim „MAGNA OPERA OF INTERIOR & SOUND“**: freigegeben, aber **nicht für die Fertigung** (nur Visitenkarten u. Ä.).
- Werkstoff EN AW-6082 (in Fusion ersatzweise „Aluminum 6061“, gleiche Dichte).
- Koordinaten: CAD-System der Einbauschnittstelle, Blendenvorderseite z = 0, +z ins Cockpit.

## 4. Lokal weiterarbeiten
```bash
pip install cadquery numpy-stl matplotlib ezdxf shapely scipy pillow scikit-image   # Python 3.10–3.12
cd testprojekt-alu-bauteil/04_cad/blende && python3 blende_2a35.py        # STEP/STL neu (dauert einige Minuten)
cd ../../06_zeichnung && python3 zeichnung_blende.py                      # Zeichnung neu
# Rendering: Blender (bpy) + render_blende.py in 05_render/
```
Fusion: Neues Design → *Einfügen → Dateien einfügen* `Blende_2A35M.step` (oder `fusion_blende.py` als Skript). Das STEP ist ein reiner Volumenkörper ohne Zeitleiste; Änderungen immer im CadQuery-Skript machen und STEP neu importieren. Das Logo-DXF als Skizze auf die Vorderseite legen.

## 5. Bekannte Lücken / offene Punkte
- `fusion_blende.py` ist nicht an Fusion getestet.
- Zeichnung hat keine Bemaßung (Kontur, Feldmitten, Magnete, Hochtöner-Raster) und eine vorläufige Sachnummer `TP-ALU-BLENDE-2A35M-L`.
- Renderings zeigen die gestufte Haut nicht (nur im STEP).
- Das Akustikmodell (Frequenzplots) ist schematisch (Massengesetz), keine Messung.
- Ältere Konzept-Bilder in `03_konzepte/` zeigen teils das alte Logo/alte Felder (nur Historie).
- Nur die linke Blende ist modelliert; die rechte wäre gespiegelt/aus `aufmass/…rechts` abzuleiten.
