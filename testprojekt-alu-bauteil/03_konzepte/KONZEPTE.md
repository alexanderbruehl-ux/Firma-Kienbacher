# Designkonzepte Blende Schwalbennest (Stand 30.09.2026)

Grundlage: Maße und Einbau laut `ANFORDERUNGEN.md` (maßlich eingefroren). Alle Entwürfe verwenden
die CAD-Kontur (links 65,6°), die Treiberausschnitte aus `parameter.json` und das Meisterwerke-Logo
(`logo/`). Dargestellt ist die linke Blende, die rechte ist spiegelbildlich.

![Konzepte](bilder/Konzepte_flach.jpg)

## Logo

`logo/Meisterwerke_Logo.svg` (Signet + Wortmarke) und `logo/Meisterwerke_Signet.svg` (nur „M“).
Nachgezeichnet vom Referenzbild „Meisterwerke Marina“ (Signet aus Messung der Schenkel konstruiert,
Wortmarke in Cinzel, SIL Open Font License). Erzeugt mit `logo/mwlogo.py`.
Position auf der Blende: **mittig unter dem 100er (KT 100 V)**, **parallel zur Unterkante gedreht
(3,7°)**, Breite 125 mm, Höhe ≈ 27.8 mm. Mitte (286.1 | 37.5) mm, Logounterkante 5 mm über der
Blendenunterkante. Abstand Signet-Oberkante zum 100er-Feld ≈ 8 mm.

## K1 – Leder (Designvariante 1)

- Träger 7–7,5 mm (Alu-Platte 5 mm oder PA12/ABS-Druck) + Leder 1,0–1,2 mm auf Schaumunterlage,
  gesamt 8,5 mm. Leder um die Kanten geschlagen und auf der Rückseite verklebt.
- Schwarze Lautsprechergitter (Lochblech oder Stoff) in den Ausschnitten, mit dunklem Zierring.
- Ziernaht umlaufend 4,5 mm innen. **Logo geprägt** (Blindprägung).
- **Edelstahl-Abschlussleiste** an der überstehenden rechten Kante, poliert, Optik wie die Einfassung
  des Schwalbennests.
- Lederfarben: dunkelblau, hellgrau, schwarz, sattelbraun → `bilder/K1_Lederfarben_flach.jpg`.

## K2 – Alu aus dem Vollen (Designvariante 2, wahrscheinlicher)

Gemeinsam für K2a–c:
- EN AW-6082 T6, 8,5 mm. Sichtseite glasperlgestrahlt + Eloxal (Farbe siehe unten), umlaufende
  **Glanzfacette** (Diamantschnitt) an der Außenkante.
- **Perforationszonen von hinten auf 2,0–2,5 mm Restwand taschenfräsen.** Löcher und Schlitze
  bohren/fräsen nur durch diese Restwand. So bleibt L/D ≈ 1, die Schalldurchlässigkeit ist gut und
  die Fräszeit gering. Außerhalb der Zonen behält die Blende die volle Dicke (Steifigkeit).
- Rückseite: 4 flache Taschen für Stahlscheiben oder Gegenmagnete gegenüber den Magnettaschen
  Ø 12 im Deckel bei (23/16), (103/193), (365/38), (423/195) mm.
- **LED-Option:** Nur das Signet wird durchgefräst (Signethöhe ≈ 13 mm, Strichstärke ≈ 1,0–1,2 mm, Fräser
  Ø 0,8 mm) und mit einem PMMA-Einsatz (opal) hinterlegt. Der LED-Streifen sitzt in einer Tasche auf
  der Rückseite. Die Wortmarke wird nach dem Eloxieren lasergraviert, weil ihre Haarstriche zu fein
  für einen Durchbruch sind. Stromzufuhr offen (z. B. Federkontakte neben den Magneten).
- Eloxalfarben: natur, titan/sekt, dunkelblau, schwarz → `bilder/K2_Eloxalfarben_flach.jpg`
  (am Beispiel K2b).

| Konzept | Muster | Charakter | Fertigung |
|---|---|---|---|
| **K2a „Ringe“** | konzentrische Lochkreise je Treiber, Loch-Ø wächst nach außen (Sub/TMT 1,0 → 2,4 mm), polierter Diamantschnitt-Ring um jedes Feld | klassisch, uhrwerkhaft, am nächsten an den Referenzen R02 | Bohren, viele Löcher (≈ 3.000–4.000); Ringe auf der Drehmaschine nicht möglich (Kontur), daher Glanzfräsen |
| **K2b „Diagonale“** | Langlöcher parallel zur 65,6°-Kante, als Sehnen in den Treiberkreisen; dazu eine Glanzschnitt-Leitlinie | nimmt die Diagonale des Boots auf, sportlich, eigenständig | Nutenfräsen Ø 2,2 / 1,6 mm, deutlich weniger Einzelelemente als Bohren |
| **K2c „Verlauf“** | flächiges Lochfeld im 65,6°-Raster; über den Treibern große Löcher, dazwischen fein, nach rechts zur „fliegenden“ Kante auslaufend | ruhig, flächig, modern; die Treiber sind nur zu ahnen | nur über den Treibern durchgehend, sonst Sacklöcher 1–2 mm tief als Dekor, damit das Gehäuse dicht bleibt |

## Offen

- Auswahl: K1 und eine K2-Variante (oder Kombination, z. B. K2b-Muster mit K2a-Ringen)
- Eloxal- bzw. Lederfarbe
- LED ja/nein und Stromzufuhr
- Spaltmaß (Vorschlag 2 mm)
