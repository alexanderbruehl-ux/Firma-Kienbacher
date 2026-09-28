# Projektstatus – Revision 7V-5-1 (Stand: siehe Datum letzter Commit)

## Kontext

Alexander ist Produktionsleiter bei einem automotive-zertifizierten
(IATF 16949) Kunststoff-Spritzguss-Unternehmen (Kienbacher). Er überarbeitet
gemeinsam mit Claude die QM-Verfahrensanweisung „Auftragsabwicklung in der
Produktion" (Dok. 7V-5-1, Version k → l), um sie an den aktuellen
Organisationszustand anzupassen und die IATF-16949-Konformität sicherzustellen.

## Methodik / Vorgehen

- **Organisierendes Prinzip: AKV** (Aufgaben / Kompetenzen / Verantwortung)
  - **Verantwortung** = wofür wird die Person am Ergebnis gemessen (Rechenschaft)
  - **Aufgaben** = was ist regelmäßig zu tun (Tätigkeiten)
  - **Kompetenzen/Befugnisse** = was darf eigenständig entschieden/angeordnet werden
  - Ein Punkt kann in mehreren Spalten stehen (z. B. wenn dieselbe Person entscheidet
    UND operativ mitwirkt – siehe Beispiel „ungeplante Kapazitätsmaßnahmen").
- **Zusätzliche Themenfelder** (nicht als eigene Matrix-Spalte, sondern als inhaltliche
  Ergänzung *innerhalb* der drei AKV-Spalten – **Option B**, siehe Entscheidung):
  - **Führung**: klassische Personalführung (Zielvereinbarung, Feedback, Entwicklung,
    Konfliktmanagement, Vorbildfunktion) – gilt für alle Führungsrollen
  - **Außensicht**: nur bei der Rolle **Produktionsleiter** – Repräsentation,
    Schnittstelle nach außen/oben. Bei nachgelagerten Rollen (z. B. Schichtführer) NICHT relevant.
  - **Sicherheit**: Arbeitssicherheit, gesetzliche Pflichten (z. B. ASchG)
  - **Umwelt**: Umweltbewusstsein, Ressourcenschonung
- **Vorgehensweise in der Diskussion**: sehr langsam, Punkt für Punkt aus der
  bestehenden Liste (Version k), nichts überspringen, Rückfragen stellen statt
  raten, unternehmensspezifische Begriffe klären bevor sie ins Dokument kommen.
- Alexander ergänzt nach dem gemeinsamen Grobentwurf noch weitere
  unternehmensspezifische Details selbst.

## Bearbeitungsstand

| Rolle (Dok. 7.5.3.x) | Status |
|---|---|
| 1 Produktionsleiter | ✅ Inhaltlich fertig abgestimmt (Themenblöcke 1–14 + Vertretung), siehe `PRODUKTIONSLEITER.md` — noch nicht in `working/*.docx` eingearbeitet |
| 2 Schichtführer → **Teamleitung Spritzguss-Produktion (Schichtführer)** (Umbenennung zur eindeutigen Klarstellung, analog zu den anderen Teamleitungsfunktionen) | ✅ Inhaltlich fertig abgestimmt (Themenblöcke 1–8), siehe `SCHICHTFUEHRER.md` — noch nicht in `working/*.docx` eingearbeitet |
| 3 Maschinenpersonal (Werker) | ⬜ Noch nicht begonnen |
| 4 Fertigung Montage → **Teamleitung Montage** | ✅ Inhaltlich fertig abgestimmt (Themenblöcke 1–4), siehe `MONTAGE.md` |
| 5 Boxenbauer | ⬜ Noch nicht begonnen |
| 6 Produktionslogistiker | ⬜ Noch nicht begonnen |
| 7 Produktionsplanung | ⬜ Noch nicht begonnen |
| 8 Arbeitsvorbereitung → **Digitale Prozessentwicklung & Lean Management** (Umbenennung + inhaltliche Neuausrichtung bereits beschlossen) | ⬜ Noch nicht begonnen |
| 9 Qualitätsprüfer/in (PQB) | ⬜ Noch nicht begonnen (Verhältnis zu neuer Rolle „QS" ist bereits geklärt, siehe OFFENE_ROLLEN.md) |
| 10 Lager (Materialvorbereitung) → **Teamleitung Lager** | ✅ Inhaltlich fertig abgestimmt (Themenblöcke 1–7), siehe `LAGER.md` |
| 11 Alle Mitarbeiter | ⬜ Noch nicht begonnen |
| **NEU: Produktionskoordination (Organisation/Personal)** | ⬜ Rolle identifiziert, noch nicht ausgearbeitet |
| **NEU: Prozesstechnik und Bemusterung** | ⬜ Rolle identifiziert, noch nicht ausgearbeitet |
| **NEU: QS (Qualitätssicherung Produktion)** | ⬜ Rolle identifiziert, noch nicht ausgearbeitet |
| **NEU: Endfertigung** (Bereich, geführt durch Teamleitung Endfertigung = Produktionskoordination) | ✅ Inhaltlich fertig abgestimmt (Themenblöcke 1–2), siehe `ENDFERTIGUNG.md` — Produktionskoordination als eigene Rolle noch separat auszuarbeiten |
| **NEU: Automatisierung** | ⬜ Rolle identifiziert, noch nicht ausgearbeitet |
| **NEU: Teamleitung Instandhaltung** | 🔶 Normrahmen abgestimmt (IATF 16949 §8.5.1.5), siehe `INSTANDHALTUNG.md` — betriebsspezifische Details von Alexander noch zu ergänzen |
| **NEU: Teamleitung Werkzeugbau** | 🔶 Normrahmen abgestimmt (IATF 16949 §8.5.1.6), siehe `WERKZEUGBAU.md` — betriebsspezifische Details von Alexander noch zu ergänzen |

Details zu den neuen/umbenannten Rollen: siehe `OFFENE_ROLLEN.md`.

### Gruppierung der Führungsrollen (Teamleiter)

Um Doppelungen zu vermeiden, werden die Teamleitungsfunktionen nicht einzeln
und unabhängig voneinander ausgearbeitet, sondern in zwei Gruppen mit
jeweils gemeinsamer AKV-Basis (Turtle-Diagramm-Logik: Hauptprozess = Input-
Bereitstellung/Transformation/Output-Versand; Unterstützungsprozess =
Ressourcen-Bereitstellung „Mit was"):

- **Hauptprozess** (`FUEHRUNG_HAUPTPROZESS.md`): Teamleitung Lager,
  Teamleitung Spritzguss-Produktion (Schichtführer), Teamleitung Montage,
  Teamleitung Endfertigung
- **Unterstützungsprozesse** (`FUEHRUNG_UNTERSTUETZUNGSPROZESSE.md`):
  Teamleitung Instandhaltung, Teamleitung Werkzeugbau

Reihenfolge: gemeinsame AKV-Basis Hauptprozess ✅ erarbeitet (abgeleitet aus
Schichtführer), danach Montage/Endfertigung/Lager, danach die Gruppe
Unterstützungsprozesse.

## Nächster konkreter Schritt

Rolle **Produktionsleiter** ist inhaltlich vollständig abgestimmt
(Themenblöcke 1–14 + Abschnitt „Vertretung", siehe PRODUKTIONSLEITER.md).

**Teamleitung Spritzguss-Produktion (Schichtführer)** ist inhaltlich
vollständig abgestimmt: allgemeine AKV-Punkte in `FUEHRUNG_HAUPTPROZESS.md`
(Themenblöcke A–H) verallgemeinert, `SCHICHTFUEHRER.md` enthält nur noch
die Spritzguss-spezifischen Ausprägungen (Themenblöcke 1, 6, 8) sowie die
schichtspezifische Besonderheit Schichtübergabe (Themenblock 9).

Beide Rollen noch nicht in `working/*.docx` eingearbeitet.

**Teamleitung Montage** ist inhaltlich vollständig abgestimmt (Themenblöcke
1–4, siehe `MONTAGE.md`); Themenblock C in `FUEHRUNG_HAUPTPROZESS.md`
wurde um die Rückmeldung fehlerhafter Kaufteile ergänzt.

**Teamleitung Endfertigung** ist inhaltlich vollständig abgestimmt
(Themenblöcke 1–2, siehe `ENDFERTIGUNG.md`).

**Teamleitung Lager** ist inhaltlich vollständig abgestimmt (Themenblöcke
1–7, siehe `LAGER.md`) — damit ist die Gruppe **Führungsrollen im
Hauptprozess** vollständig abgearbeitet.

Als Nächstes: Gruppe **Unterstützungsprozesse** (Teamleitung
Instandhaltung, Teamleitung Werkzeugbau, siehe
`FUEHRUNG_UNTERSTUETZUNGSPROZESSE.md`), danach die separate Rolle
**Produktionskoordination** (Personalunion mit Teamleitung Endfertigung,
aber inhaltlich eigenständig — Vertretung des Produktionsleiters Bereich
Organisation/Personal).

## Bereits geklärte, generelle Struktur-Entscheidungen

- **QMB/QS-Korrespondenzstruktur** (zweistufig):
  - Schicht-/Team-Ebene: Schichtführer/Teamleiter ↔ **QMB**
  - Gesamtheitliche Ebene: Produktionsleitung ↔ **QS (Qualitätssicherung Produktion)**
  - Ablauf bei Korrekturmaßnahmen: QS stellt Bedarf fest → Produktionsleitung
    entscheidet über konkrete Maßnahme → QS prüft Wirksamkeit und gibt frei
    (z. B. Entsperren von Teilen/Prozessen). Damit ist ein Vier-Augen-Prinzip
    zwischen Produktions- und Qualitätsseite auf beiden Ebenen etabliert.
- **Dreiteilige Vertretungsstruktur des Produktionsleiters** (siehe OFFENE_ROLLEN.md
  für Details der einzelnen Vertretungsfunktionen):
  1. Organisation/Personal → Produktionskoordination
  2. Technik → Prozesstechnik und Bemusterung
  3. Qualität → QS Produktion (bewusst AUSSERHALB der Produktionsabteilung
     angesiedelt — 4-Augen-Prinzip)
