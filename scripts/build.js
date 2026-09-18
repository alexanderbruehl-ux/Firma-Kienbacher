const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell,
  WidthType, BorderStyle, AlignmentType, ShadingType, LevelFormat, PageBreak
} = require("docx");

const FONT = "Calibri";

function h(text, level) {
  return new Paragraph({
    heading: level,
    spacing: { before: 240, after: 120 },
    children: [new TextRun({ text, bold: true, font: FONT })],
  });
}

function p(text, opts = {}) {
  return new Paragraph({
    spacing: { after: 120 },
    children: [new TextRun({ text, font: FONT, ...opts })],
  });
}

function bullet(text, level = 0) {
  return new Paragraph({
    numbering: { reference: "bullets", level },
    spacing: { after: 60 },
    children: [new TextRun({ text, font: FONT })],
  });
}

function roleHeading(text) {
  return new Paragraph({
    spacing: { before: 200, after: 100 },
    children: [new TextRun({ text, bold: true, font: FONT, size: 22 })],
  });
}

// Sub-heading for a single Themenblock within a role
function blockHeading(text) {
  return new Paragraph({
    spacing: { before: 220, after: 80 },
    children: [new TextRun({ text, bold: true, underline: {}, font: FONT, size: 20 })],
  });
}

// "Aufgabe:" / "Kompetenz:" / "Verantwortung:" label followed by inline text
function akv(label, text) {
  return new Paragraph({
    spacing: { after: 80 },
    children: [
      new TextRun({ text: label + " ", bold: true, font: FONT, size: 20 }),
      new TextRun({ text, font: FONT, size: 20 }),
    ],
  });
}

// Same, but the label stands alone above a following bullet list
function akvLabel(label) {
  return new Paragraph({
    spacing: { before: 40, after: 40 },
    children: [new TextRun({ text: label, bold: true, font: FONT, size: 20 })],
  });
}

function note(text) {
  return new Paragraph({
    spacing: { after: 100 },
    children: [new TextRun({ text, italics: true, font: FONT, size: 18 })],
  });
}

function footerNote() {
  return new Paragraph({
    spacing: { before: 400 },
    border: { top: { style: BorderStyle.SINGLE, size: 4, color: "CC0000" } },
    children: [
      new TextRun({
        text: "ENTWURF – Zwischenstand in Bearbeitung, wird gemeinsam mit den Rollenverantwortlichen abgestimmt.",
        italics: true, color: "CC0000", font: FONT, size: 18,
      }),
    ],
  });
}

const doc = new Document({
  numbering: {
    config: [
      {
        reference: "bullets",
        levels: [
          { level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } } },
          { level: 1, format: LevelFormat.BULLET, text: "◦", alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 1080, hanging: 360 } } } },
        ],
      },
    ],
  },
  sections: [
    {
      properties: { page: { size: { width: 11906, height: 16838 } } }, // A4
      children: [
        new Paragraph({
          children: [new TextRun({ text: "QM - Verfahrensanweisung", bold: true, font: FONT, size: 28 })],
        }),
        new Paragraph({
          spacing: { after: 200 },
          children: [new TextRun({ text: "Kap. 7.5 Produktrealisierung", font: FONT, size: 22 })],
        }),
        footerNote(),
        new Paragraph({ spacing: { before: 300, after: 200 },
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: "Auftragsabwicklung in der Produktion", bold: true, underline: {}, font: FONT, size: 26 })] }),

        h("7.5.1 Ziel", HeadingLevel.HEADING_2),
        p("Sicherstellen einer reibungslosen Produktion, um die Spritzgussteile in der gewünschten Qualität, Termin und innerhalb der geplanten Kosten herzustellen."),

        h("7.5.2 Geltungsbereich", HeadingLevel.HEADING_2),
        p("Dieser umfasst die Auftragsplanung, Vorbereitung von Materialien u. Einbauteilen, Werkzeugen und der gesamten maschinellen Einrichtung inklusive der Wartung und Instandhaltung und Qualitätskontrollen."),

        h("7.5.3 Verantwortung und Befugnisse", HeadingLevel.HEADING_2),
        note("Struktur je Rolle: AKV-Prinzip (Aufgaben / Kompetenzen / Verantwortung), gegliedert nach Themenblöcken. Details und Diskussionsstand siehe notes/PRODUKTIONSLEITER.md bzw. notes/SCHICHTFUEHRER.md."),

        // ============ 7.5.3.1 PRODUKTIONSLEITER ============
        roleHeading("7.5.3.1 Produktionsleiter"),

        blockHeading("1. Kapazitäts-/Planungsabstimmung"),
        akvLabel("Aufgaben:"),
        bullet("Teilnahme an der Kapazitäts- und Planungsabstimmung Produktion/Logistik (aktuell: wöchentliches Meeting „KPLI“)"),
        bullet("Kontrolle/Prüfung der von der Rolle „Produktionsplanung“ erstellten Pläne"),
        bullet("Mitwirkung bei der Umsetzung kurzfristiger, ungeplanter Kapazitätsmaßnahmen (z. B. Einsatz alternativer Anlagen, zusätzliche Schichten)"),
        bullet("Weiterentwicklung der Planungsmethodik und der eingesetzten Systeme"),
        akvLabel("Kompetenzen:"),
        bullet("Freigabe-/Entscheidungsbefugnis über die Produktionsplanung"),
        bullet("Entscheidungsbefugnis bei ungeplanten Kapazitätskonflikten"),

        blockHeading("2. IKK – Interdisziplinäre Koordinationsrunde Kernprozesse"),
        p("Teilnehmer (Abteilungsleiter): Produktion, Logistik, Produkt-/Projekttechnik, Business Development (Schwerpunkt Digitalisierung), Qualitätsmanagement. Fokus: Kernprozess der Leistungserbringung inkl. vorgelagertem Vorserienprozess. Charakter: taktisch."),
        akvLabel("Aufgabe:"),
        bullet("Leitung der IKK mit den genannten Bereichen"),
        bullet("Top-Down: Vorbereitung auf anstehende externe Themen (z. B. Audits, neue Kundenprojekte/Werkzeuge, TISAX-Einführung)", 1),
        bullet("Bottom-Up: Ableitung verallgemeinerter, systemischer Maßnahmen aus aktuellen operativen Problemen (Reklamationen, Werkzeug-/Ablaufschwierigkeiten, Ausschuss)", 1),
        akv("Kompetenz:", "Entscheidungsbefugnis über die aus der Runde abgeleiteten Maßnahmen."),
        akv("Führung:", "Leitung eines interdisziplinären Teams über Abteilungsgrenzen hinweg."),

        blockHeading("3. Wirtschaftlichkeit"),
        akv("Verantwortung:", "Wirtschaftlicher Einsatz von Personal und Ressourcen."),
        akv("Aufgabe:", "Sicherstellung des wirtschaftlichen Einsatzes von Personal und Ressourcen (laufende Steuerung/Überwachung im operativen Betrieb)."),

        blockHeading("4. Personalverantwortung"),
        p("Personalverantwortung für die Mitarbeiter der Produktion inkl. Werkzeugbau und Instandhaltung."),
        akvLabel("Verantwortung:"),
        bullet("Personalverantwortung für die Mitarbeiter der Produktion inkl. Werkzeugbau und Instandhaltung"),
        bullet("Einhaltung aller relevanten Gesetze, insbesondere Arbeitszeitgesetz und ArbeitnehmerInnenschutzgesetz (ASchG) – Themenfeld Sicherheit"),
        bullet("Disziplinarische Verantwortung bei WerkerInnen und Sachbearbeitern als Eskalationsstufe (Erstverantwortung liegt bei den jeweiligen Teamleitern)"),
        akvLabel("Aufgaben:"),
        bullet("Personalanforderung"),
        bullet("Führung von Mitarbeitergesprächen"),
        bullet("Bildungsbedarfsermittlung"),
        bullet("Aus- und Weiterbildung sowie Unterweisung der unterstellten Mitarbeiter: Details siehe Themenblock 14"),
        bullet("Mitwirkung an der Einführung geeigneter (flexibler) Arbeitszeitmodelle (gemeinsam mit HR)"),
        bullet("Sicherstellung der Urlaubsplanung"),
        akvLabel("Kompetenzen:"),
        bullet("Entscheidung über Einstellung/Kündigung"),
        bullet("Disziplinarische Maßnahmen bei WerkerInnen/Sachbearbeitern (als Eskalationsinstanz)"),

        blockHeading("5. Korrekturmaßnahmen / QS-Zusammenarbeit"),
        p("Das direkte Gegenüber der Produktionsleitung bei Korrekturmaßnahmen auf Gesamtebene ist die Rolle QS (Qualitätssicherung Produktion). QMB bleibt Korrespondenzfunktion auf Schicht-/Team-Ebene. Ablauf: QS stellt Bedarf fest → Produktionsleitung entscheidet Maßnahme → QS prüft und gibt frei."),
        akv("Aufgabe:", "Entscheidung über Art und Umsetzung von Korrekturmaßnahmen bei durch QS festgestelltem Handlungsbedarf (gesamtheitliche Ebene)."),
        akv("Kompetenz:", "Entscheidungsbefugnis über die konkrete Maßnahmenwahl bei Korrekturmaßnahmen."),

        blockHeading("6. Wartung und Instandhaltung"),
        p("Zwei getrennte Teams mit eigener Teamleitung, beide berichten im Regelbetrieb direkt an den Produktionsleiter: Teamleitung Instandhaltung (Maschinen, Anlagen, Infrastruktur inkl. Betriebsmittel, Fertigungshilfsmittel, Roboter, automatisierte Anlagen) und Teamleitung Werkzeugbau (Werkzeugbau sowie Werkzeugwartung, -reparatur und -instandhaltung)."),
        akv("Aufgabe:", "Überwachung der Wartung und Instandhaltung von Maschinen, Anlagen und Infrastruktur (Teamleitung Instandhaltung) sowie von Werkzeugen (Teamleitung Werkzeugbau). Bei technischen Eskalationsfällen: Priorisierung der erforderlichen Maßnahmen."),
        akv("Kompetenz:", "Entscheidungsbefugnis über die Umsetzung der bestgeeigneten Variante bei Eskalationsthemen (keine Terminierung/Ressourcenzuteilung im Regelbetrieb)."),

        blockHeading("7. Produktionsaufzeichnungen"),
        akvLabel("Verantwortung: Organisatorische Sicherstellung, dass Produktionsaufzeichnungen den Anforderungen aus ISO 9001 (§7.5.2/7.5.3) und IATF 16949 (§7.5.3.2.1) entsprechen:"),
        bullet("Vorhanden/vollständig – erforderliche Aufzeichnungen werden tatsächlich erstellt und geführt"),
        bullet("Eindeutig/korrekt identifizierbar – Kennzeichnung (Titel, Datum, Ersteller, Referenznummer)"),
        bullet("Versioniert – Änderungen sind nachvollziehbar"),
        bullet("Aufbewahrung – gemäß Record-Retention-Policy (IATF 16949 §7.5.3.2.1)"),
        bullet("Zugänglich/lesbar/geschützt – auffindbar und geschützt vor Verlust/unbefugtem Zugriff"),
        akv("Aufgabe:", "Regelmäßige/stichprobenhafte Kontrolle der produktionsrelevanten Aufzeichnungen (z. B. Prüfbegleitkarte, Schichtlogbuch [Schichtführer], Maschinen-/Prozessdaten, Wartungsprotokolle) auf diese Kriterien; Veranlassung von Korrekturen bei Abweichungen."),
        note("Abgrenzung: Vorserienbezogene Dokumente (z. B. Erstmusterprüfberichte, FMEAs) sind nicht Teil dieser Aufgabe – sie sind in der Produkt-/Projekttechnik verortet."),

        blockHeading("8. Reklamationen / QMB-Zusammenarbeit"),
        p("QMB ist eine normativ geforderte Funktion (IATF 16949 §5.3.1/§5.3.2) und vertritt die Organisation nach außen in Qualitätsangelegenheiten – nicht nur gegenüber Kunden, sondern auch gegenüber Lieferanten und bei der Überwachung von Partnern im Produktionsnetzwerk (Lohnfertigung). QS deckt demgegenüber die internen Qualitätsbelange ab: Sperren, Beurteilung, Grenzmusterkataloge, Erststückfreigaben sowie interne Maßnahmen zur Verbesserung und Vermeidung von Reklamationen."),
        akv("Aufgabe:", "Unterstützung von QMB bei der Bearbeitung von Reklamationen (Kunden, Lieferanten, Netzwerkpartner/Lohnfertiger) durch Bereitstellung produktionsseitiger Informationen (Ursachenanalyse, Sofort-/Korrekturmaßnahmen) für die externe Kommunikation. Die inhaltliche Entscheidung über und Umsetzung von Korrekturmaßnahmen auf Produktionsseite erfolgt gemäß Themenblock 5."),

        blockHeading("9. Lehrlingsausbildung"),
        akv("Verantwortung (keine operative Aufgabe):", "Verantwortlich für die Lehrlingsausbildung im Bereich Produktion. Operativ wird die Ausbildung durch zwei separate Lehrlingsausbildner wahrgenommen: Kunststofftechniker – Ausbildner: Techniker im Bereich Automatisierung/Instandhaltung; Werkzeugbautechniker – Ausbildner: Teamleitung Werkzeugbau."),

        blockHeading("10. Sperren von fehlerhaften Produkten"),
        akv("Regelfall (Aufgabe):", "Umsetzung der Sperrentscheidung von QS/PQB – der Produktionsleiter folgt hier zu 100 % der fachlichen Beurteilung durch QS/PQB."),
        akvLabel("Unklare/strittige Fälle (Kompetenz, gemeinsame Entscheidung mit QS/PQB): Abwägung zwischen Reklamationsrisiko und Sperrkosten:"),
        bullet("Vertagung der endgültigen Entscheidung (z. B. Rücksprache mit Kunde/GF am Folgetag), Produktion läuft in der Zwischenzeit weiter"),
        bullet("Trennung zwischen Produktions- und Lieferfreigabe: Teile werden weiterproduziert (z. B. Engpassanlage), aber zunächst nur für die Auslieferung gesperrt"),

        blockHeading("11. Bemusterungs-Eskalation (multidisziplinäre Abstimmung)"),
        p("Bemusterung (Werkzeug, Automatisierung, Material, Spritzgussparameter) obliegt der Rolle Prozesstechnik und Bemusterung. Die Kundenfreigabe nach Vorstellung serienfallender Teile entspricht dem normativ geforderten Produktfreigabeprozess (IATF 16949 §8.3.4.4). Danach ist Prozess/Referenznummer/Werkzeug zur Vorserie frei (z. B. für Run@Rate) – das Herstellungsrisiko einer etwaigen Vorproduktion liegt bei der Produktion (vergleichbar der „Interim Approval“ im PPAP-Prozess)."),
        akv("Aufgabe:", "Kontrolle des Bemusterungsprozesses aus Produktionssicht."),
        akvLabel("Kompetenz: Eskalationsinstanz bei mehreren Varianten oder Risikofragen – multidisziplinäre Abstimmung (IATF 16949 §8.3.2.1) zwischen:"),
        bullet("Produktionsleitung"),
        bullet("Abteilungsleitung Produkt-/Projekttechnik"),
        bullet("ggf. QMB"),
        bullet("in seltenen Fällen Leitung SCM (z. B. Auslieferbehälter, Verpackungsvorschriften)"),
        note("Der formale Projektabschluss (Prozessreview/Workflow aller Abteilungsleiter, dokumentiert in DocuWare) ist ein separater, bereits etablierter Schritt."),

        blockHeading("12. Werkzeugoptimierungen in Absprache mit PT (Prozesstechnik und Bemusterung)"),
        p("Fall 1 – vor Serienstart: läuft im Rahmen des Vorserienprozesses (siehe Themenblock 11)."),
        akvLabel("Fall 2 – nach Serienstart, aus Produktionssicht (Qualitäts-/Kostengründe, technische Werkzeugänderung und/oder erneute Kundenfreigabe erforderlich) – Aufgabe:"),
        bullet("Entgegennahme des Optimierungsbedarfs, herangetragen von Prozesstechnik und Bemusterung, Werkzeugbau oder (seltener) Schichtführern"),
        bullet("Grobe Nutzen-/Kostenbewertung als Gesamtkosten- und Qualitätsverantwortlicher der Produktion"),
        akv("Kompetenz:", "Entscheidung, ob das Thema bei der Produkt-/Projekttechnik eingesteuert wird."),

        blockHeading("13. Optimieren der technischen Produktprozessentwicklung"),
        akv("Aufgabe (Top-Down):", "Vorgabe von Optimierungszielen/-schwerpunkten (z. B. Zykluszeiten, Verfahrens-/Prozessparameter, Automatisierungsgrad o. Ä.) an Prozesstechnik und Bemusterung, Automatisierung bzw. Digitale Prozessentwicklung & Lean Management, je nach Thema."),
        akv("Kompetenz (Bottom-Up):", "Bewertung, Priorisierung und Freigabe von Optimierungsvorschlägen, die von diesen drei Disziplinen herangetragen werden."),

        blockHeading("14. Aus- und Weiterbildung / Unterweisung"),
        p("Klarstellung: Schichtführer sind eine Teamleitungsfunktion, keine eigene Hierarchieebene."),
        akvLabel("Aufgabe (direkt unterstellte Mitarbeiter = TeamleiterInnen):"),
        bullet("Konkrete Schulungsbedarfsermittlung"),
        bullet("Sicherstellung der Aus- und Weiterbildung sowie Unterweisung"),
        bullet("Kontrolle der Umsetzung im Sinne einer Wirksamkeitsprüfung"),
        akv("Verantwortung (alle unterstellten Mitarbeiter, auch die der TeamleiterInnen, z. B. Einsteller):", "Grundsätzliche Verantwortung für Aus- und Weiterbildung sowie Unterweisung – Schwerpunkt auf Sicherstellung, dass die Durchführung durch die TeamleiterInnen oder andere Fachabteilungen (z. B. HR, QS, SVP, SFK) erfolgt."),

        blockHeading("Vertretung"),
        akvLabel("Struktur: dreiteilige, fest zugeordnete Vertretung nach Fachbereichen:"),
        bullet("Organisation/Personal → Produktionskoordination"),
        bullet("Technik → Prozesstechnik und Bemusterung"),
        bullet("Qualität → QS Produktion"),
        akv("Kompetenz:", "Festlegung dieser Vertretungsregelung sowie Übertragung der jeweiligen Teilbefugnisse an die drei Vertretungsfunktionen."),
        akvLabel("Umfang der übertragenen Befugnisse:"),
        bullet("Regelfall (kurzfristige Abwesenheit): Vertretung übt die Aufgaben/Kompetenzen des Fachbereichs aus, jedoch nicht die weitreichendsten Entscheidungsbefugnisse (z. B. Neueinstellungen)"),
        bullet("Bei längerer Abwesenheit (Richtwert 4–6 Wochen): erweiterte Befugnisse – auch weitreichende Entscheidungen gehen auf die Vertretung über"),

        // ============ 7.5.3.2 SCHICHTFÜHRER ============
        roleHeading("7.5.3.2 Teamleitung Spritzguss-Produktion (Schichtführer)"),
        note("Gehört zur Gruppe „Führungsrollen im Hauptprozess“ (End2End-Auftragsabwicklung, gemeinsam mit Teamleitung Lager, Montage, Endfertigung). Schichtführer und andere TeamleiterInnen unterscheiden sich grundsätzlich nicht; der relevanteste Unterschied ist die Schichtarbeit."),

        blockHeading("1. Maschinenüberwachung und Parametrierung"),
        akvLabel("Aufgabe:"),
        bullet("Überwachung der laufenden Produktionsmaschinen während der Schicht – inkl. der (teilweise automatisierten) Materialzuführung – auf Einhaltung der vorgegebenen Prozessparameter (Einstelldatenblatt)"),
        bullet("Auswahl der richtigen Einstelldaten und Übertragen der gültigen Parametersätze auf die Maschine (Umbau/Einstellung)"),
        bullet("Feinjustierung der Parameter innerhalb definierter Grenzen, auf Basis der laufenden Teilequalität, bis die geforderte Bauteilqualität erreicht ist. Grundlage: Rückstellmuster der letzten Produktion, im Prüfplan definierte Merkmale/Maße inkl. Toleranzen, bei besonders komplexen Fällen Erstmuster/Produktionsfreigabemuster aus dem Serienstart. PQB liefert dazu die Qualitätsrückmeldung zu den Teilen und kann fallweise auf Erfahrungsbasis beraten – die Entscheidung über Parameteranpassungen liegt jedoch nicht bei PQB"),
        akvLabel("Kompetenz:"),
        bullet("Eigenständige fachliche Entscheidung über Parameteranpassungen – beruht auf erlerntem Wissen und Erfahrung, da keine generelle/pauschale Lösung möglich ist (Vielzahl an Parametern und Wechselwirkungen, z. B. Materialchargen)"),
        bullet("Bei technischen Störungen: Eskalation an Teamleitung Instandhaltung (Maschine, automatisierte Materialförderung) bzw. Teamleitung Werkzeugbau (Werkzeugprobleme) bzw. Automatisierung"),
        note("Hinweis: Die „Produktionsfreigabe“ ist derselbe Schritt wie die Erststückfreigabe – siehe Themenblock 7."),

        blockHeading("2. Schichtergebnis Qualität/Quantität"),
        akv("Verantwortung:", "Sicherstellung der geplanten Produktionsmenge und der geforderten Bauteilqualität während der Schicht. Bei Abweichungen von der Produktionsplanung (z. B. durch Störungen): Rückmeldung an Produktionsplanung/Produktionsleitung."),

        blockHeading("3. Fehlerbewertung, Sperren, Transport gesperrter Ware"),
        akv("Aufgabe:", "Bewertung gemeldeter Fehler (Fehlermeldungen der Werker) gemeinsam mit PQB auf Schicht-/Team-Ebene; Entscheidung über Sperrung fehlerhafter Produkte. Anweisung an Lager bzw. Produktionslogistiker zum Transport gesperrter Ware ins gesperrte Lager."),

        blockHeading("4. Personalverantwortung Schicht"),
        akv("Verantwortung:", "Personalverantwortung für die unterstellten Werker der Schicht, inkl. Sicherheit, Ordnung und Sauberkeit am Arbeitsplatz. Erstverantwortung für disziplinarische Maßnahmen bei den unterstellten Werkern (Produktionsleiter als Eskalationsstufe)."),
        akv("Aufgabe:", "Personalführung der Schicht (Einteilung, Feedback, Konfliktmanagement)."),

        blockHeading("5. Produktions- und Qualitätsaufzeichnungen"),
        akv("Aufgabe:", "Durchführung/Erstellung der vereinbarten Produktions- und Qualitätsaufzeichnungen der Schicht (z. B. Schichtlogbuch, Prüfbegleitkarte)."),

        blockHeading("6. Restmaterialentsorgung"),
        akv("Aufgabe:", "Ausgespritztes Material sortenrein in Restmüllgebinde bzw. vorgeschriebene Container entsorgen."),

        blockHeading("7. Freigabeprüfungen"),
        akv("Aufgabe:", "Erststück-/Letztstückfreigabe sowie erneute Freigabe nach geplanten/ungeplanten Produktionsunterbrechungen >30 min, jeweils gemeinsam mit PQB lt. Prüfbegleitkarte. Dies ist derselbe Schritt wie die Produktionsfreigabe nach der Parametrierung (Themenblock 1) – kein separater, vorgelagerter Freigabeschritt."),

        blockHeading("8. Einfache Werkzeug-Wartungstätigkeiten"),
        akv("Aufgabe:", "Durchführung einfacher Werkzeug-Wartungstätigkeiten am eingebauten Werkzeug (z. B. Reinigung, Schmierung beim Rüstvorgang). Tiefergehende Wartung, Reparatur und Instandhaltung obliegt der Teamleitung Werkzeugbau."),

        blockHeading("9. Schichtübergabe"),
        akv("Aufgabe:", "Durchführung der Schichtübergabe an den nachfolgenden Schichtführer: Weitergabe des aktuellen Produktions- und Qualitätsstatus je Maschine, offener Vorkommnisse und laufender Maßnahmen, dokumentiert im Schichtlogbuch."),

        // ============ übrige Rollen: noch unverändert Version k (Rohgerüst) ============
        new Paragraph({ children: [new PageBreak()] }),
        note("Die folgenden Rollen sind noch nicht im Detail überarbeitet – Inhalt entspricht noch Version k (unverändertes Rohgerüst) und dient nur als Platzhalter."),

        roleHeading("7.5.3.3 Aufgaben des Maschinenpersonals (Werker)"),
        bullet("Eigenverantwortliches Beurteilen der produzierten Teile lt. AAW"),
        bullet("Fehlermeldung bei niO Teilen an SF/PQB"),
        bullet("Beachten von zus. Q-Hinweisen z.B.: temp. AAW"),
        bullet("Teile entgraten oder montieren (lt. Anweisung)"),
        bullet("Teile verpacken, etikettieren lt. Verpackungsvorschrift"),
        bullet("Mitwirkung Erststück / Letztstückfreigabe"),

        roleHeading("7.5.3.4 Aufgaben Montage"),
        bullet("Durchführen der Fertigungsarbeiten an Produkten der Produktionsmaschinen lt. Produktions- bzw. Auftragsplanung"),
        bullet("Qualitätskontrolle der bearbeiteten Produkte lt. Arbeitsanweisung"),
        bullet("Organisation der Lagerbereiche, Lagerstand u. Kennzeichnung"),
        bullet("Verpackung der Produkte von Montageautomaten"),
        bullet("Meldung an PQB / WE-Kontrolle bei festgestellten NIO Teilen / Lieferungen von Unterlieferanten"),
        bullet("Sperren von fehlerhaften Produkten"),
        bullet("Erststück / Letztstückfreigabe"),

        roleHeading("7.5.3.5 Aufgaben Boxenbauer"),
        bullet("Buchungen und Abtransport der Gebinde / Teile"),
        bullet("Unterstützende Mitarbeit im Produktionsbereich"),
        bullet("Qualitätsfreigabe der Leergebinde u. Verpackungsmaterial unter Berücksichtigung der Qualitätsvorschriften"),
        bullet("Übergabe der Restgebinde an das Lager (Artikelrest)"),
        bullet("Material Rückbuchungen durchführen"),

        roleHeading("7.5.3.6 Aufgaben Produktionslogistiker"),
        bullet("Verwaltung, Sicherstellung der Versorgung mit Zukaufteilen, Kartonagen und internen Leergebinden"),
        bullet("Durchführen von Reinigungsarbeiten wie Blecheinleger, Buchsen, Schrauben, Gebinde, …"),
        bullet("Zu- und Abtransport von HF und FT-Teile (Gebinde) aus der Montage"),
        bullet("Übergabe der Versandeinheiten an das Lager auf definierten Platz"),
        bullet("Bereitstellung von Leergebinde u. Verpackungsmaterial in der Montage"),
        bullet("Buchungen prüfen und durchführen von Korrekturen"),
        bullet("Korrektur und Rückmeldung von falschen Gewichtsangaben"),
        bullet("Kommunikation mit Lagerverantwortlichen bei Abweichungen durchführen"),
        bullet("Abschließen von Produktionsaufträgen im System"),
        bullet("Abwiegen und Entsorgen / Zuführen von Ausschüssen (Recyclingmaterial), Papier, Kartonagen in allen Bereichen"),

        roleHeading("7.5.3.7 Aufgaben Produktionsplanung"),
        bullet("Produktionsfeinplanung"),
        bullet("Zusammenarbeit mit und Unterstützung der Arbeitsvorbereitung (Mithilfe der Personaleinsatzplanung/Einsteuerung der Reparaturen und Wartungen von den Werkzeugen)"),
        bullet("Aktive Mitarbeit bei der Optimierung von Prozessen und Maßnahmen zur Qualitäts- oder Wirtschaftlichkeitsverbesserung"),
        bullet("Mitarbeit bei logistischen und produktionswirtschaftlichen Projekten"),
        bullet("Projektmanagement im Produktionsbereich"),
        bullet("Administrative Tätigkeiten im Produktionsbereich (z.B.: Vorbereitung der Produktionsaufträge, Erstellung unterschiedlicher Listen/Tabellen, usw.)"),
        bullet("Umsetzung der Vorgaben (Kundenbedarfe) laut Kapazitätsübersicht-Liste"),
        bullet("Erstellung der Produktionsaufträge im ERP-System (FOSS)"),
        bullet("Einplanung der Produktionsaufträge im MES-System (authentig)"),
        bullet("Dokumentation im DocuWare anlegen"),
        bullet("Berichtswesen"),

        roleHeading("7.5.3.8 Aufgaben Digitale Prozessentwicklung & Lean Management (ex Arbeitsvorbereitung)"),
        bullet("Stammdatenpflege"),
        bullet("Arbeitsaufträge rechtzeitig unter Berücksichtigung der Projektpläne erstellen"),
        bullet("Prozessdaten- und Werkzeugoptimierung"),
        bullet("Informationspflicht an die vorgesetzte Stelle bei drohenden Kapazitätsengpässen oder anderen Einflüssen, welche die Bedarfserfüllung gefährden"),
        bullet("Machbarkeitsprüfungen bzgl. rechtzeitiger Bereitstellung von Werkzeugen und Vorrichtungen"),
        bullet("Mitarbeit bei logistischen und produktionswirtschaftlichen Projekten"),
        bullet("Vergabe u. Verwaltung von Lagerplätzen für WZG, Vorrichtungen, Mess-/Hilfsmittel"),

        roleHeading("7.5.3.9 Aufgaben Qualitätsprüfer/in (PQB)"),
        bullet("Durchführung von fertigungsbegleitenden Qualitätsprüfungen"),
        bullet("Dokumentieren der Prüf- und Messergebnisse in Q Studio"),
        bullet("Erfassen von festgestellten Fehlern"),
        bullet("Mitarbeit bei der Reklamationsbearbeitung"),
        bullet("Durchführung von Qualitätsschulungen"),
        bullet("Sperren von fehlerhaften Teilen"),
        bullet("Maßnahmenverfolgung bei Prozessänderungen"),
        bullet("Erststück / Letztstückfreigabe"),
        bullet("Erneute Freigabe nach Produktionsunterbrechung"),

        roleHeading("7.5.3.10 Aufgaben Teamleitung Lager (Materialvorbereitung)"),
        bullet("Be- und Entladen von LKWs"),
        bullet("Organisation der Lagerbereiche, Lagerstand u. Kennzeichnung"),
        bullet("Buchungen in FOSS ausführen"),
        bullet("Sperren fehlerhafter Ware"),
        bullet("Vortrocknung u. Bereitstellung der Rohstoffe"),
        bullet("Verwaltung u. Vorbereitung der Einlegeteile"),
        bullet("Einlagerung produzierter Ware"),
        bullet("Transport gesperrter Ware ins Gesperrt-Lager"),
        bullet("Kommissionierung und Versand"),
        bullet("Bestellanforderungen an Einkauf"),
        bullet("Bedarfsmeldung bei Abfallentsorgung"),

        roleHeading("7.5.3.11 Alle Mitarbeiter"),
        bullet("Informationen auf der Anschlagtafel beachten"),
        bullet("Qualitative und quantitative Arbeitserbringung"),
        bullet("Durchgängiges Umweltbewusstsein"),
        bullet("Sorgsamer Umgang mit Ressourcen"),
        bullet("Aktive Mitarbeit bei Verbesserungsmaßnahmen"),
        bullet("Ordnung und Sauberkeit am Arbeitsplatz"),

        h("7.5.4 Verfahren", HeadingLevel.HEADING_2),
        p("Zur Sicherheit der Produktionsabläufe wurden entsprechende Prüf- und Arbeitsanweisungen erstellt. In den Produktionsaufträgen und Produktdatenblättern sind alle Informationen zur Herstellung der Produkte enthalten. Der Ablauf ist im Flow Chart (siehe separate Grafik / Anhang) dargestellt."),

        h("7.5.4.1.1 Grobplanung", HeadingLevel.HEADING_3),
        p("Kundenbestellungen werden vom VKI geprüft und ins FOSS übergeben. Entsprechend Lagerstand und Bedarfen werden die Produktionsaufträge eingelastet. Im Modul KPLI werden die aktuellen Bedarfe ermittelt."),

        h("7.5.4.2 Feinplanung", HeadingLevel.HEADING_3),
        p("Diese erfolgt aufgrund der freigegebenen FOSS-Aufträge übersichtlich in TIG und auf der Planungstafel mit Produktionsinfo der Aufträge durch die Produktionsplanung. Die Planungstafel steht der Arbeitsvorbereitung der einzelnen Fachabteilungen zur Verfügung, wobei in den bereits aufliegenden Aufträgen alle vorzubereitenden Details angeführt sind. Gleichzeitig erfolgt täglich bzw. nach Bedarf ein kurzes Informationsgespräch an der Planungstafel mit den dazu benötigten Personen (AV, QM, Lager, Logistik). Die Planung wird täglich aktualisiert, um eine gewisse Flexibilität beizubehalten. Der Schichtplan am Bildschirm zeigt die aktuelle Werkerzuteilung an den Arbeitsplätzen; die Mitarbeiterqualifikationsmatrix wird dazu einbezogen, die entsprechende Produktschulung wird vor der Zuteilung des Werkers durch die Stelle Produktionsleitung überprüft."),

        h("7.5.4.3 Zeitlich begrenzte Änderungen in der Produktionsprozesslenkung", HeadingLevel.HEADING_3),
        p("Änderungen werden generell als interne Projekte geführt und entsprechend den Erfordernissen an die AV mitgeteilt. In den wöchentlichen Produktionsbesprechungen werden die Themen besprochen. Im Modul ARPL besteht die Möglichkeit, zeitlich begrenzte Änderungen mit Ablauftermin im Arbeitsplan einzutragen; diese Zusatzanweisungen sind an den Auftragspapieren ersichtlich, bis die Änderung terminlich abgelaufen ist. Temporäre Produktänderungen werden gemäß den Anforderungen von PT und QM/RPP auf Konformität geprüft; es erfolgt eine Rückmeldung an die Produkttechnik über den Status des betreffenden PA's mittels Eintragung im Schichtlogbuch SF/PQB. Ein Prüfmittelwechsel erfolgt generell nicht, da nur 1 Satz angefertigt wurde. Alle in der Produktion vorhandenen Messmittel haben einen gültigen Prüfstatus. Ein Wechsel des Werkzeuges von der Standardspritzgussmaschine auf die geeignete Ersatzmaschine ist grundsätzlich erlaubt, da in der Prozessentwicklungsphase Vorserie immer eine Ausweichmaschine mit bemustert wird. Derselbe Vorgang gilt für den Fall, wenn der Standardladungsträger nicht verfügbar ist, mit alternativen Gebinden."),

        h("7.5.4.4 Abwicklung der Produktionsaufträge", HeadingLevel.HEADING_3),
        p("Für die allgemeine Vorbereitung der Formen ist der Schichtführer zuständig. Der Einbau der Formen erfolgt durch den Schichtführer oder mit Aushilfe geschulter Mitarbeiter bei Bedarf. Produktionslogistik / Wareneingang ist für die rechtzeitige Vorbereitung der entsprechenden Einlegeteile zuständig, Boxenbauer für die Gebindebereitstellung und interne Transporte von der Produktion ins Lager. Der Lagerarbeiter ist für die rechtzeitige Vorbereitung der Materialien zuständig. Der Schichtführer hat nun die Aufgabe, die Produktion abzuwickeln (7A-51-3), entsprechende Qualitätskontrollen mittels Prüfbegleitkarte durchzuführen und Vorkommnisse zu beheben."),

        h("7.5.4.5 Begleitende Produktionsarbeiten", HeadingLevel.HEADING_3),
        p("Störungen werden, wenn möglich, sogleich behoben. Vom QMB / PL wird dann geprüft, ob Korrekturmaßnahmen notwendig sind, um Wiederholungsfehler zu vermeiden. Laufende Qualitätskontrollen werden vom PQB nach geregelter Häufigkeit lt. Arbeits- und Prüfanweisung durchgeführt und protokolliert. Interne Reklamationen werden über den Reklamationsbericht dokumentiert; der interne Reklamationskoordinator führt die Maßnahmenverfolgung nach dem 8D-Verfahren durch. Eine geregelte Wartung u. Instandhaltung (siehe Wartungslisten) dient als vorbeugende Maßnahme zur Produktionssicherheit (6A-32-1). Der Teamleader ist für die Auslieferqualität, für die Auswertung der Produktionsvorkommnisse verantwortlich u. hat bei Bedarf Maßnahmen einzuleiten."),

        h("7.5.4.6 Material", HeadingLevel.HEADING_3),
        p("Alle Anlieferungen werden im WEP ident geprüft. Die Produktionsplanung erfolgt rechtzeitig. Um eine geforderte Vortrocknung von Originalmaterial rechtzeitig einzuleiten, werden die Trocknungsdetails am Arbeitsplan angedruckt (ARPL). Der Aushang erfolgt zuvor an der Plantafel. Restmaterial wird in sauberen, verschlossenen, beschrifteten Behältern / Säcken an das Lager retourniert, gebucht und aufbewahrt."),
      ],
    },
  ],
});

Packer.toBuffer(doc).then((buffer) => {
  require("fs").writeFileSync(__dirname + "/../working/7V-5-1_Auftragsabwicklung_Produktion_ENTWURF.docx", buffer);
  console.log("done");
});
