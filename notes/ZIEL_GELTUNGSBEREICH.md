# Abschnitte 7.5.1 Ziel und 7.5.2 Geltungsbereich — Review (Zwischenstand)

Status: **Beide Abschnitte inhaltlich abgeschlossen.** Teil des großen,
bisher unveränderten Original-Rohtexts (siehe `PROJEKTSTATUS.md`,
Status-Check vom Review-Durchgang).

---

## 7.5.1 Ziel

**Alter Text (Version k, unverändert):**
> "Sicherstellen einer reibungslosen Produktion, um die Spritzgussteile
> in der gewünschten Qualität, Termin und innerhalb der geplanten
> Kosten herzustellen."

**Neuer Text:**
> Sicherstellen einer reibungslosen Produktion, um die Spritzgussteile
> in der gewünschten Qualität, zum vereinbarten Termin und innerhalb
> der geplanten Kosten herzustellen, unter Berücksichtigung einer
> klaren Rollenverteilung mit eindeutig zugeordneten Aufgaben,
> Kompetenzen und Verantwortlichkeiten sowie einer multidisziplinären
> Zusammenarbeit der beteiligten Funktionen.

**Ergänzung:** Themen Rollenklarheit, Aufgabenverteilung und
multidisziplinäre Zusammenarbeit explizit verankert — das begründet
rückwirkend den Zweck der gesamten AKV-Ausarbeitung in 7.5.3.

---

## 7.5.2 Geltungsbereich

**Alter Text (Version k, unverändert):**
> "Dieser umfasst die Auftragsplanung, Vorbereitung von Materialien u.
> Einbauteilen, Werkzeugen und der gesamten maschinellen Einrichtung
> inklusive der Wartung und Instandhaltung und Qualitätskontrollen."

**Neuer Text:**
> Dieser Geltungsbereich umfasst die Auftragsplanung, Vorbereitung von
> Material, Kaufteilen und Einlegeteilen, Werkzeugen und der gesamten
> maschinellen Einrichtung inklusive Wartung, Instandhaltung und
> Qualitätskontrollen – von der Einlastung freigegebener
> Produktionsaufträge bis zur Bereitstellung der fertigen Produkte zur
> Übergabe an Versand/Logistik.
>
> **Vorgänger-Prozess:** Auftragserfassung/Vertrieb
> (Kundenbestellungen, Lieferpläne/-abrufe) sowie – bei Neuteilen oder
> Werkzeugänderungen – der Vorserienprozess (Produktentstehung,
> Erstbemusterung).
> **Nachfolge-Prozess:** Transportabwicklung/Spedition (externer
> Weitertransport zum Kunden) sowie Fakturierung/Rechnungsstellung.

**Korrekturen gegenüber dem ersten Entwurf (von Alexander erkannt):**
1. **"Einbauteile" → "Kaufteile und Einlegeteile":** "Einbauteile" ist
   kein in diesem Dokument definierter/verwendeter Begriff. Die
   etablierten Materialkategorien sind Kaufteile (vereinheitlicht,
   siehe `PRODUKTIONSLOGISTIKER.md`) und Einlegeteile (ersetzt
   „Blecheinleger, Buchsen, Schrauben").
2. **Nachfolge-Prozess-Fehler:** "Versand/Logistik an den Kunden" kann
   nicht der Nachfolge-Prozess sein, da Versand laut
   `FUEHRUNG_HAUPTPROZESS.md` ausdrücklich **Teil dieses
   E2E-Auftragsabwicklungsprozesses** ist ("Teamleitung Lager …
   Output: Versand — vor- und nachgelagerter Schritt im
   E2E-Auftragsabwicklungsprozess"). Der tatsächliche Nachfolge-Prozess
   beginnt erst, wenn die Ware das Werk verlässt (Transportabwicklung/
   Spedition, Fakturierung).

**Herleitung Vorgänger-/Nachfolgeprozess (zwei Perspektiven):**
- *Generisch* (klassische Auftragsabwicklungskette): Vertrieb/
  Auftragserfassung → (bei Neuteilen: Produktentstehung/
  Vorserienprozess) → Auftragsabwicklung Produktion (dieses Dokument)
  → Transport/Spedition → Fakturierung.
- *Von innen heraus* (aus den bereits erarbeiteten Rollen): Input über
  Produktionsplanung und -steuerung (Kundenbedarfe/Lieferpläne/
  JIT-JIS-Abrufe → Betriebsaufträge) und Wareneingang/Lager (Kaufteile,
  Rohstoffe); bei Neuteilen/Werkzeugänderungen zusätzlich freigegebene
  Werkzeuge/Spezifikationen aus dem Vorserienprozess. Output über
  Versandeinheiten (Produktionslogistiker → Lager → Kommissionierung/
  Versand, noch innerhalb des Prozesses).
