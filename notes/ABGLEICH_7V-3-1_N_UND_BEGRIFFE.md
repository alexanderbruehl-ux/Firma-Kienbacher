# Abgleich mit 7V-3-1 Vers. N und Begriffe (Stand 12.11.2026)

Entstanden bei der Checkliste „Übernahme in die Serie“
(`working/Checkliste_Uebernahme_in_die_Serie_Produktion.xlsx`, Generator
`scripts/checkliste_serie.py`). Grundlage: 7V-5-1-Entwurf (PDF, Stand
23.10.2026) und 7V-3-1 „Ablauf einer Produktentwicklung“ Vers. N
(10.11.2026).

## Von Alexander bestätigte Begriffe und Zuständigkeiten (12.11.2026)

- **Verpackungsvorschrift**, nicht „Verpackungsanweisung“
- **ERP-System (FOSS)**, nicht BMD (BMD ist das HR-System, BMD PI)
- **Produktionsfreigabemuster** bzw. **Rückstellmuster** (letzte
  Produktion), nicht „Grenzmuster“
- **Prüfpläne gibt es in der Produktion nicht.** Die Prüfungen stehen in der
  artikelbezogenen Arbeitsanweisung.
- **Werkzeugabnahme:** gemeinsam Prozesstechnik und Werkzeugbau
- **Maschinenzeit (Rüstzeit + Zykluszeit):** gemeinsam Prozesstechnik und
  Produktionsplanung

## Stellen im 7V-5-1-Entwurf, die davon abweichen

- „Grenzmusterkataloge“: Abgrenzung zur QS im Produktionsleiter-Teil und
  Rolle QS (7.5.3.19)
- „im Prüfplan definierte Merkmale/Maße“: Teamleitung Spritzguss (7.5.3.2)
- „liegen entsprechende Arbeitsanweisungen und Prüfpläne vor“: Verfahrensteil

## Offene Unstimmigkeiten zwischen 7V-5-1 (Entwurf) und 7V-3-1 Vers. N

1. **Prozessentwicklung in der Vorserie:** 7V-3-1 N weist der Produktion die
   „Entwicklung des Herstellungsprozesses“ zu. Die Rolle Prozesstechnik in
   der 7V-5-1 sagt „Fokus Serie, Vorserie in eigener Anweisung“. Vorschlag:
   Produktion = technische Bemusterung und Parameter, PT = formale
   Unterlagen (Erstmusterprüfbericht, FMEA, Lenkungsplan). Beide Anweisungen
   gleich formulieren.
2. **Objektstammdaten im FOSS für Betriebsmittel doppelt vergeben:**
   Teamleitung Instandhaltung (7.5.3.15) und Digitale Prozessentwicklung &
   Lean Management (7.5.3.12).
3. **Ausweichmaschine:** 7V-5-1 (7.5.4.3, in Bearbeitung) setzt voraus, dass
   in der Vorserie immer eine Ausweichmaschine mitbemustert wird. 7V-3-1 N
   verlangt das nicht.
4. Im PDF-Entwurf (23.10.) fehlen die Abschnitte „Aufzeichnungen“ und
   „Mitgeltende Unterlagen“, die in den Notizen als abgeschlossen markiert sind.
5. 7V-3-1 N verwendet „Verpackungsanweisung“, „Prüfpläne“ (7.3.4.4,
   7.3.4.8) und „Prüfplanung“ (Aufgabe QM). Für die Produktion müsste es
   „artikelbezogene Arbeitsanweisung“ heißen.

## Checkliste „Übernahme in die Serie“

- Werkzeug für Produktionsleiter-Themenblock 11 („Kontrolle des
  Bemusterungsprozesses aus Produktionssicht“) und Grundlage für die
  Mitzeichnung des Prozessreviews (7F-34-1, 7V-3-1 Abschnitt 7.3.4.10).
- Vorschlag zur Verankerung: in Themenblock 11 und bei den Aufzeichnungen
  nennen (ohne Dokumentnummer). Status derzeit: interne Arbeitshilfe, kein
  gelenktes Formblatt.
- Zuständigkeiten sind außer Werkzeugabnahme und Maschinenzeit nur
  Vorschläge und müssen noch gegen alle Rollen geprüft werden (Grundsatz in
  `PROJEKTSTATUS.md`).
- Neu erzeugen: `python3 scripts/checkliste_serie.py working/Checkliste_Uebernahme_in_die_Serie_Produktion.xlsx`,
  danach mit `recalc.py` der xlsx-Skill neu berechnen.
