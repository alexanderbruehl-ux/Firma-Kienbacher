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
| 1 Produktionsleiter | 🔶 In Bearbeitung — siehe `PRODUKTIONSLEITER.md` |
| 2 Schichtführer | ⬜ Noch nicht begonnen |
| 3 Maschinenpersonal (Werker) | ⬜ Noch nicht begonnen |
| 4 Fertigung Montage → **Montage** (Umbenennung bereits beschlossen) | ⬜ Noch nicht begonnen |
| 5 Boxenbauer | ⬜ Noch nicht begonnen |
| 6 Produktionslogistiker | ⬜ Noch nicht begonnen |
| 7 Produktionsplanung | ⬜ Noch nicht begonnen |
| 8 Arbeitsvorbereitung → **Digitale Prozessentwicklung & Lean Management** (Umbenennung + inhaltliche Neuausrichtung bereits beschlossen) | ⬜ Noch nicht begonnen |
| 9 Qualitätsprüfer/in (PQB) | ⬜ Noch nicht begonnen (Verhältnis zu neuer Rolle „QS" ist bereits geklärt, siehe OFFENE_ROLLEN.md) |
| 10 Lager (Materialvorbereitung) | ⬜ Noch nicht begonnen (Führung: Teamleitung Lager) |
| 11 Alle Mitarbeiter | ⬜ Noch nicht begonnen |
| **NEU: Produktionskoordination (Organisation/Personal)** | ⬜ Rolle identifiziert, noch nicht ausgearbeitet |
| **NEU: Prozesstechnik und Bemusterung** | ⬜ Rolle identifiziert, noch nicht ausgearbeitet |
| **NEU: QS (Qualitätssicherung Produktion)** | ⬜ Rolle identifiziert, noch nicht ausgearbeitet |
| **NEU: Endfertigung** (Bereich, geführt durch Teamleitung Endfertigung = Produktionskoordination) | ⬜ Rolle identifiziert, noch nicht ausgearbeitet |

Details zu den neuen/umbenannten Rollen: siehe `OFFENE_ROLLEN.md`.

## Nächster konkreter Schritt

Weiter in der Punkteliste **Produktionsleiter**, nächster noch offener Punkt aus
dem Originaldokument (Version k):

> **„Organisation / Überwachung der Wartung und Instandhaltung"**

(Danach folgen aus der Originalliste noch: Prüfung der Produktionsaufzeichnungen,
Verantwortlich für die Lehrlingsausbildung, Sperren von fehlerhaften Produkten,
Bemusterungs-Nachbesprechung mit Technik, Werkzeugoptimierungen in Absprache mit PT,
Optimieren der technischen Produktprozessentwicklung, Schulungsplanung der
Schichtführer u. Einsteller.)

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
