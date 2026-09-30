# Designkonzepte Blende Schwalbennest

## Aktuelle Vorschau (Stand 30.09.2026) – immer zwei Varianten

![Vorschau](bilder/Vorschau_flach.jpg)

**Variante 1 – Leder sattelbraun:** Lautsprechergitter schwarz, Logo blind geprägt, Ziernaht, an der
überstehenden rechten Kante eine **polierte Edelstahl-Abschlussleiste, 9 mm breit** (so breit wie die
Einfassung des Schwalbennests im Rumpf, aus dem Foto gemessen: oben ≈ 9 mm, links ≈ 8 mm).

**Variante 2 – Aluminium hochglanzpoliert mit Lochmuster:** Logo eingefräst (ohne Farbe, keine LED),
schlanke gefräste **Kantennut** (1,2 mm breit, 4 mm innen) parallel zur rechten Kante als optische Nähe zur
Edelstahleinfassung, Diamantschnitt-Ring um jedes Lochfeld. Das Lochmuster soll ein **Blickfang** sein
statt eines technischen Rasters (vgl. Burmester). Drei Entwürfe:

| Muster | Idee | Wirkung |
|---|---|---|
| **2A „Sonnenblume“** | Phyllotaxis-Spirale (goldener Winkel 137,5°), Loch-Ø wächst von innen nach außen | organisch, spiralige Linien schimmern je nach Blickwinkel |
| **2B „Welle“** | konzentrische Lochkreise, Loch-Ø wellenförmig moduliert | Ringe scheinen zu „schwingen“, Sinnbild Schallwelle |
| **2C „Strahlenkranz“** | Zentrum als Sonnenblumenfeld, außen Kranz aus Langlöchern im Wechsel lang/kurz | dynamisch, Blick zieht zur Treibermitte |

Fertigung (für alle drei): Lochfelder von hinten auf 2,0–2,5 mm Restwand taschenfräsen, Verlaufsgrößen
in 4–6 Stufen (Standardbohrer), Langlöcher mit Schaftfräser Ø 1,5 mm. Hochglanz: Polieren bzw.
Diamantfräsen, danach Klarlack oder Glanzeloxal.

---

## Frühere Konzeptrunde

Grundlage: Maße und Einbau laut `ANFORDERUNGEN.md` (maßlich eingefroren). Alle Entwürfe verwenden
die CAD-Kontur (links 65,6°), die Treiberausschnitte aus `parameter.json` und das Meisterwerke-Logo
(`logo/`). Dargestellt ist die linke Blende, die rechte ist spiegelbildlich.

![Konzepte](bilder/Konzepte_flach.jpg)

## Logo (vorläufig)

`logo/` – vorläufige Nachzeichnung aus der Bilddatei (siehe `logo/README.md`), bis die Original-
Vektordatei vorliegt. Position: **parallel zur Unterkante (3,7°)**, Logounterkante 8 mm über der Blendenunterkante.
**Die Mittelachse des Logos (senkrecht zur Grundlinie, also um 3,7° gekippt) läuft verlängert durch den
100er-Mittelpunkt.** Mitte (291,3 | 40,9) mm, Breite 115 mm, Höhe ≈ 27,9 mm.

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
- ~~LED-Option~~ (entfällt, Logo wird eingefräst bzw. geprägt): Nur das Signet wird durchgefräst (Signethöhe ≈ 13 mm, Strichstärke ≈ 1,0–1,2 mm, Fräser
  Ø 0,8 mm) und mit einem PMMA-Einsatz (opal) hinterlegt. Der LED-Streifen sitzt in einer Tasche auf
  der Rückseite. Die Wortmarke wird nach dem Eloxieren lasergraviert, weil ihre Haarstriche zu fein
  für einen Durchbruch sind. Stromzufuhr offen (z. B. Federkontakte neben den Magneten).
- Eloxalfarben: natur, titan/sekt, dunkelblau, schwarz → `bilder/K2_Eloxalfarben_flach.jpg`
  (am Beispiel K2b).

| Konzept | Muster | Charakter | Fertigung |
|---|---|---|---|
| **K2a „Ringe“** | konzentrische Lochkreise je Treiber, Loch-Ø wächst nach außen (Sub/TMT 1,0 → 2,4 mm), polierter Diamantschnitt-Ring um jedes Feld | klassisch, uhrwerkhaft, am nächsten an den Referenzen R02 | Bohren, viele Löcher (≈ 3.000–4.000); Ringe auf der Drehmaschine nicht möglich (Kontur), daher Glanzfräsen |
| **K2b „Diagonale“** | Langlöcher parallel zur 65,6°-Kante, als Sehnen in den Treiberkreisen | nimmt die Diagonale des Boots auf, sportlich, eigenständig | Nutenfräsen Ø 2,2 / 1,6 mm, deutlich weniger Einzelelemente als Bohren |
| **K2c „Verlauf“** | flächiges Lochfeld im 65,6°-Raster; über den Treibern große Löcher, dazwischen fein, nach rechts zur „fliegenden“ Kante auslaufend | ruhig, flächig, modern; die Treiber sind nur zu ahnen | nur über den Treibern durchgehend, sonst Sacklöcher 1–2 mm tief als Dekor, damit das Gehäuse dicht bleibt |

## Offen

- Auswahl: K1 und eine K2-Variante (oder Kombination, z. B. K2b-Muster mit K2a-Ringen)
- Eloxal- bzw. Lederfarbe
- LED ja/nein und Stromzufuhr
- Spaltmaß (Vorschlag 2 mm)
