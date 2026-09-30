# Anforderungen Blende Schwalbennest (Stand 30.09.2026, von Alexander Brühl bestätigt)

## Einbau

![Schnitt](Einbau_Schnitt_schematisch.png)

- **Rumpfwand 10 mm**, Öffnung mit polierter Edelstahleinfassung. Dahinter liegt das Fach mit
  **140 mm Tiefe**.
- Der **LS-Korpus** (Deckel 20 mm + Gehäuse 119 mm = 139 mm) schlüpft in das Fach und ist genau
  auf die Innenmaße eingepasst. **Links rutscht er in einen Hinterschnitt** hinter die Rumpfwand
  (im CAD: linke Korpuskante senkrecht, 90°).
- Die **Blende (max. 8,5 mm)** wird mit **Magneten** am Deckel gehalten. Die Magnete halten
  **1,5 mm Abstand**, so dass die Blende genau in der 10-mm-Wand sitzt und **bündig mit dem Rumpf**
  abschließt.
- **Links ist die Blende gegenüber dem Korpus abgeschrägt** (CAD 65,6°), damit sie in die
  eingefasste Öffnung passt.
- **Rechts steht sie ca. 15–20 mm über den Korpus** (CAD: Rückseite ≈17 mm, als Fase ausgeführt).
  Das ergibt die schlanke, „fliegende“ Kante.
- **Spalt zwischen Blende und Einfassung:** links, oben und unten umlaufend gleich (Vorschlag 2 mm),
  rechts größer.
- Treiberausschnitte laut `parameter.json` → `einbauschnittstelle`. Die Blende gibt es links und
  rechts, spiegelbildlich.
- Tiefe: 8,5 + 1,5 + 20 + 119 = 149 mm ≤ 10 mm Wand + 140 mm Fach. Der zuvor vermutete
  Tiefenkonflikt entfällt.

## CAD-Referenz (Stand Fusion/STEP, bleibt Referenz)

Die Maße der heutigen Lederabdeckung und des Deckels bleiben **unverändert** in
`parameter.json` → `einbauschnittstelle`. Zusätzlich aus dem STEP ausgelesen (Ursprung = linke
untere Ecke der Blendenvorderseite, mm):

| Kontur | Ecken (unten links → unten rechts → oben rechts → oben links) |
|---|---|
| Blende Vorderseite | (0/0) · (369,1/23,9) · (438,7/209,4) · (93,8/207,0) |
| Blende Rückseite (mit Überstand/Fase rechts) | (−0,6/−0,1) · (388,4/25,0) · (457,8/210,1) · (93,5/207,5) |
| Deckel/Korpus-Front | (−17,8/2,4) · (373,8/27,7) · (440,6/205,9) · (−17,4/202,7) |

Die Fotomontage (Referenzfoto aus dem privaten Repo, nicht hier abgelegt) wurde **am Foto**
perspektivisch angepasst, nicht an der Blende. Die Blende ist dafür so eingepasst, dass links,
oben und unten ein gleicher Spalt von 2 mm entsteht. Rechts wurden 20 mm Luft hinter der Fase
angenommen. Die Öffnungsmaße sind damit noch nicht nachgemessen.

## Designvarianten

| | Variante 1 – Leder | Variante 2 – Alu gefräst (**wahrscheinlicher**) |
|---|---|---|
| Aufbau | belederte Blende auf Träger | aus dem Vollen gefräst, EN AW-6082/5083 |
| Schalldurchlass | Lautsprechergitter | gebohrte oder geschlitzte Perforation |
| Logo | geprägt | eingefräst, optional LED-hinterleuchtet |
| Farbe/Oberfläche | Leder dunkelblau, hellgrau, schwarz oder sattelbraun | offen (natur, titan, dunkelblau eloxiert; Glanzfacette) |
| Überstehende Kante | Abschlussleiste in Optik der Edelstahl-Einfassung des Schwalbennests | gefräste Kante, ggf. Glanzfacette |

## Offen

- Nachmessen: Öffnung innen an der Einfassung (Länge oben/unten, Höhe) und Spalt rechts
- Spaltmaß festlegen (Vorschlag 2 mm)
- Logo/Signet (Meisterwerke Marina, Kienbacher, neutral)
- Variante 2: Perforation gebohrt oder geschlitzt, LED ja/nein (Bauraum für LED-Streifen und
  Diffusor in 8,5 mm)
- Stückzahl
