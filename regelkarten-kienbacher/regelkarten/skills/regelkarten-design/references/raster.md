# Raster, Farben und Typografie der Regelkarte

Verbindliche Werte. Der Generator liest sie nicht aus dieser Datei, sondern hat sie
in `werkzeuge/layout.py` als Konstanten — diese Datei ist die lesbare Fassung
derselben Werte und die Begründung dahinter. Wird eine Zahl hier geändert, muss sie
auch dort geändert werden.

## 1. Seite

| Größe | Wert |
|---|---|
| Format | A4 hoch, 210 × 297 mm |
| in EMU | 7 560 000 × 10 692 000 (1 mm = 36 000 EMU) |
| Hintergrund | `#FFFFFF`, ausdrücklich gesetzt |
| Folien | genau eine |

Passt der Inhalt nicht auf eine Seite, wird **gekürzt oder der Prozess geteilt** —
nie auf eine zweite Seite ausgewichen und nie verkleinert unter die Mindestgrößen
in Abschnitt 4.

## 2. Raster (alle Werte in mm ab Blattkante oben links)

| Element | x | Breite | Bemerkung |
|---|---|---|---|
| Satzspiegel | 10,0 | 190,0 | linker und rechter Rand je 10,0 |
| Kopfband | 0,0 | 210,0 | randabfallend, Höhe 32,0 |
| Spalte links | 10,0 | 91,5 | Mitte bei 55,75 |
| Spalte rechts | 108,5 | 91,5 | Mitte bei 154,25 |
| Spalt zwischen den Spalten | — | 7,0 | |
| Rollenspalte „Wer macht was?" | 14,5 | 54,0 | |
| Aufgabenspalte „Wer macht was?" | 70,0 | 125,5 | |

Vertikal:

| Element | y | Höhe |
|---|---|---|
| Kopfband | 0,0 | 32,0 |
| Eyebrow-Zeile | 6,5 | 4,0 |
| Titel | 13,0 | 13,0 (Reserve für Ersatzschrift) |
| Logo (Bildmarke, weiß) | 8,0 | 16,0, rechte Kante bei 196,0 |
| Inhaltsbereich | 40,0 | bis 272,0 → **232,0 mm nutzbar** |
| Fußzeile | 280,0 | 12,0 |

**Innenabstand in jeder Farbfläche:** 4,5 mm links und rechts, 3,5 mm oben und unten.
**Abstand zwischen zwei Blöcken:** 5,0 mm. Zwischen zwei Abschnitten: 8,0 mm.
**Eckradius** aller `roundRect`: 3,0 mm absolut (der Adjust-Wert wird je Box aus
Höhe und Breite zurückgerechnet, damit der Radius optisch konstant bleibt).

## 3. Farben

Nur Kienbacher-CI: Blau `#0079A7` und Grau `#7B7C7E` sowie Aufhellungen und
Abdunklungen davon. **Kein Grün, kein Gelb.**

| Name | Wert | Verwendung |
|---|---|---|
| `ci_blau` | `#0079A7` | Kopfband, Rahmen, Verbindungslinien, JA-Chip |
| `ci_grau` | `#7B7C7E` | Rahmen und Kantenmarkierung der Ausnahme — **nie für Text** |
| `text` | `#00435C` | aller Text auf hellem Grund |
| `text_invers` | `#FFFFFF` | Text auf Blau und auf dem grauen Chip |
| `flaeche_blau_1` | `#E6F2F6` | normaler Ablaufschritt |
| `flaeche_blau_2` | `#D9EBF2` | JA-Zweig, hervorgehobener Schritt |
| `flaeche_grau_1` | `#F2F2F2` | neutrales Panel, „Wer macht was?" |
| `flaeche_grau_2` | `#EBEBEC` | zweite Graustufe |
| `chip_grau` | `#5C5D5E` | Chip für NEIN und AUSNAHME, weiße Schrift |
| `fuss` | `#5C5D5F` | Fußzeilentext |
| `warnung` | `#B22F22` | **nur** echter Sicherheitshinweis (Verletzungsgefahr) |

### Nachgerechnete Kontraste (WCAG 2.1)

| Paar | Verhältnis | |
|---|---|---|
| `#FFFFFF` auf `#0079A7` | 4,89 : 1 | bestanden (Normaltext ≥ 4,5) |
| `#FFFFFF` auf `#5C5D5E` | 6,60 : 1 | bestanden |
| `#00435C` auf `#FFFFFF` | 10,73 : 1 | bestanden |
| `#00435C` auf `#E6F2F6` | 9,40 : 1 | bestanden |
| `#00435C` auf `#D9EBF2` | 8,74 : 1 | bestanden |
| `#00435C` auf `#F2F2F2` | 9,58 : 1 | bestanden |
| `#5C5D5F` auf `#FFFFFF` | 6,59 : 1 | bestanden |

**Zwei Werte, die ausdrücklich verworfen wurden:**
`#7B7C7E` als Textfarbe auf Weiß erreicht nur 4,18 : 1 und fällt für die 8-pt-Fußzeile
durch — deshalb `#5C5D5F`. Und `#0079A7` als Textfarbe auf `#E6F2F6` erreicht nur
4,29 : 1 — deshalb sind auch Abschnittstitel in `#00435C`, und Blau bleibt der
Struktur vorbehalten (Flächen, Rahmen, Linien, Chips).

## 4. Typografie

| Ebene | Schrift | Größe | Schnitt | Farbe |
|---|---|---|---|---|
| Eyebrow | Track | 9 pt | Regular, gesperrt | `#FFFFFF` |
| Titel | Track | 20–24 pt | Regular | `#FFFFFF` |
| Abschnittstitel | Arial | 12–14 pt | Bold | `#00435C` |
| Schrittnummer | Arial | 12–14 pt | Bold | `#0079A7` |
| Fließtext | Arial | 11–12 pt | Regular | `#00435C` |
| Rollenname | Arial | 10–11 pt | Bold | `#00435C` |
| Chip-Text (JA/NEIN) | Arial | 14 pt | Bold | `#FFFFFF` |
| Fußzeile | Arial | 8–9 pt | Regular | `#5C5D5F` |

**Untergrenze: 10 pt.** Reicht der Platz nicht, wird der Fließtext von 12 auf 11 und
von 11 auf 10 pt reduziert — darunter nie. Dann wird gekürzt.

**Track nur im Kopfband.** Die Schrift hat keinen Fettschnitt, alles Fette ist Arial.
Track ist auf vielen Rechnern nicht installiert; die Titelbox hat deshalb 13 mm Höhe
bei 24 pt Schrift, damit eine Ersatzschrift nicht anstößt.

**Zeilenabstand** 1,15-fach. **Zeilenlänge** höchstens rund 90 Zeichen — bei 190 mm
Satzbreite und 11 pt Arial sind das etwa 105 Zeichen, deshalb ist durchgehender Text
über die volle Breite nur für kurze Absätze zulässig.

## 5. Ablauf und Entscheidungen

**Normaler Schritt:** Fläche `flaeche_blau_1`, Rahmen `ci_blau` 1,0 pt, Nummer als
eigenes Textfeld links oben in `ci_blau` bold.

**Entscheidung.** Die Frage steht frei über der Verzweigung, linksbündig im
Satzspiegel, Arial 14 pt bold. Darunter vier gerade Linien in `ci_blau`, 1,5 pt:

1. Stamm senkrecht von der Frage abwärts bei x = 105,0
2. Querbalken waagrecht von x = 55,75 bis x = 154,25
3. linker Ast senkrecht bei x = 55,75 bis zur Oberkante der linken Box
4. rechter Ast senkrecht bei x = 154,25 bis zur Oberkante der rechten Box

Jede Linie endet an einer Box. Keine Linie läuft durch Text.

**JA-Zweig, links:** Fläche `flaeche_blau_2`, Rahmen `ci_blau` 1,5 pt, Chip oben links
in `ci_blau` mit weißem „JA".

**NEIN-Zweig / Ausnahme, rechts:** Fläche `#FFFFFF`, Rahmen `ci_grau` 2,0 pt, Chip
oben links in `chip_grau` mit weißem „NEIN" beziehungsweise „AUSNAHME", zusätzlich
eine 3,0 mm breite senkrechte Markierung in `ci_grau` an der linken Boxkante.

Der Unterschied muss **ohne Farbe** erkennbar bleiben: gefüllt gegen weiß, dünner
gegen dicker Rahmen, ohne gegen mit Kantenmarkierung — und in jedem Fall das
ausgeschriebene Wort. Das trägt auch bei Farbfehlsichtigkeit und im
Schwarz-Weiß-Ausdruck.

## 6. Pflichtbereich „Wer macht was?"

Panel über die volle Satzbreite, Fläche `flaeche_grau_1`, Rahmen `ci_blau` 1,0 pt.
Titel „WER MACHT WAS?" Arial 13 pt bold. Je Zeile: Rollenname in der linken Spalte
bold, Aufgabe in der rechten Spalte regular. Zwischen den Zeilen eine 0,5-pt-Linie
in `ci_grau` bei mehr als drei Rollen.

## 7. Abschluss und Fußzeile

Abschlussband über die volle Satzbreite, Fläche `flaeche_blau_1`, ohne Rahmen.
Überschrift „WEITERARBEITEN WENN" oder „FERTIG WENN" Arial 11 pt bold, Kriterium
daneben oder darunter, 10 pt.

Fußzeile dreiteilig, Arial 8 pt, `#5C5D5F`:

- links: `RK-0xx / Revision x.x / TT.MM.JJJJ`
- Mitte: `Verfasser: … / Prüfer: … / Freigeber: …` — leer bleibende Felder als
  Unterstrich-Platzhalter
- rechts: `A4 Hochformat`

Darüber eine 0,5-pt-Trennlinie in `ci_grau` über die Satzbreite bei y = 278,0.
