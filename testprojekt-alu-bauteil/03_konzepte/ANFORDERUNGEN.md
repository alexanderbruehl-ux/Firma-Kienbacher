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
- **Rechts steht sie ca. 15–20 mm über den Korpus**, gerade Kante über die volle Dicke (keine Fase).
  Rechts daneben bleibt das **Staufach offen**. Von der Seite gesehen entsteht so eine schlanke,
  „fliegende“ Kante.
- **Spalt zwischen Blende und Einfassung:** oben, unten und links gleich (Vorschlag 2 mm). Rechts
  schließt das offene Staufach an.
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
| Blende Rückseite (Bestand, rechts breiter als Vorderseite) | (−0,6/−0,1) · (388,4/25,0) · (457,8/210,1) · (93,5/207,5) |
| Deckel/Korpus-Front | (−17,8/2,4) · (373,8/27,7) · (440,6/205,9) · (−17,4/202,7) |

**Fotomontage** (Referenzfoto aus dem privaten Repo, hier nicht abgelegt): Der Maßstab stammt aus
dem CAD (Blendenhöhe ≈ Öffnungshöhe). Nur die Blendenkontur oben, unten und links wurde optisch an
die Einfassung angepasst (2 mm Spalt). Die rechte Kante ist die Deckelkante + 17,5 mm. Der Winkel der
linken Kante passt so (bestätigt). Korpus und Ausschnitte sind gegenüber der ersten Montage um
**≈ 11,4 mm nach rechts** versetzt. Dadurch bleibt zwischen Sub-Ausschnitt Ø 156 und linker
Blendenkante wieder der CAD-Steg von 8,1 mm. Zurückgerechnete Kontur im CAD-System
(≈, nur aus dem Foto): (19,6/−0,9) · (386,1/10,7) · (461,5/211,9) · (80,9/210,0).
Vor der Konstruktion die Öffnung real nachmessen.

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
