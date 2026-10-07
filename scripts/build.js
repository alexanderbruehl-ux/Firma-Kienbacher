const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell,
  WidthType, AlignmentType, ShadingType, LevelFormat, PageBreak
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
        new Paragraph({ spacing: { before: 300, after: 200 },
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: "Auftragsabwicklung in der Produktion", bold: true, underline: {}, font: FONT, size: 26 })] }),

        h("7.5.1 Ziel", HeadingLevel.HEADING_2),
        p("Sicherstellen einer reibungslosen Produktion, um die Spritzgussteile in der gewünschten Qualität, zum vereinbarten Termin und innerhalb der geplanten Kosten herzustellen, unter Berücksichtigung einer klaren Rollenverteilung mit eindeutig zugeordneten Aufgaben, Kompetenzen und Verantwortlichkeiten sowie einer multidisziplinären Zusammenarbeit der beteiligten Funktionen."),

        h("7.5.2 Geltungsbereich", HeadingLevel.HEADING_2),
        p("Dieser Geltungsbereich umfasst die Auftragsplanung, Vorbereitung von Material, Kaufteilen und Einlegeteilen, Werkzeugen und der gesamten maschinellen Einrichtung inklusive Wartung, Instandhaltung und Qualitätskontrollen – von der Einlastung freigegebener Produktionsaufträge bis zur Bereitstellung der fertigen Produkte zur Übergabe an Versand/Logistik."),
        akv("Vorgänger-Prozess:", "Auftragserfassung/Vertrieb (Kundenbestellungen, Lieferpläne/-abrufe) sowie – bei Neuteilen oder Werkzeugänderungen – der Vorserienprozess (Produktentstehung, Erstbemusterung)."),
        akv("Nachfolge-Prozess:", "Transportabwicklung/Spedition (externer Weitertransport zum Kunden) sowie Fakturierung/Rechnungsstellung."),

        h("7.5.3 Verantwortung und Befugnisse", HeadingLevel.HEADING_2),

        // ============ 7.5.3.1 PRODUKTIONSLEITER ============
        roleHeading("7.5.3.1 Produktionsleiter"),

        blockHeading("1. Kapazitäts-/Planungsabstimmung"),
        akvLabel("Aufgaben:"),
        bullet("Teilnahme an der Kapazitäts- und Planungsabstimmung Produktion/Logistik (aktuell: wöchentliches Meeting „KPLI“)"),
        bullet("Kontrolle/Prüfung der von der Rolle „Produktionsplanung und -steuerung“ erstellten Pläne"),
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
        p("Das direkte Gegenüber der Produktionsleitung bei Korrekturmaßnahmen auf Gesamtebene ist die Rolle QS (Qualitätssicherung Produktion). Auf Schicht-/Team-Ebene liegt die entsprechende Bewertung bei Teamleitung und PQB. Ablauf: QS stellt Bedarf fest → Produktionsleitung entscheidet Maßnahme → QS prüft und gibt frei."),
        akv("Aufgabe:", "Entscheidung über Art und Umsetzung von Korrekturmaßnahmen bei durch QS festgestelltem Handlungsbedarf (gesamtheitliche Ebene)."),
        akv("Kompetenz:", "Entscheidungsbefugnis über die konkrete Maßnahmenwahl bei Korrekturmaßnahmen."),

        blockHeading("6. Wartung und Instandhaltung"),
        p("Zwei getrennte Teams mit eigener Teamleitung, beide berichten im Regelbetrieb direkt an den Produktionsleiter: Teamleitung Instandhaltung (Maschinen, Anlagen, Infrastruktur inkl. Betriebsmittel, Fertigungshilfsmittel, Roboter, automatisierte Anlagen) und Teamleitung Werkzeugbau (Werkzeugbau sowie Werkzeugwartung, -reparatur und -instandhaltung)."),
        akv("Aufgabe:", "Überwachung der Wartung und Instandhaltung von Maschinen, Anlagen und Infrastruktur (Teamleitung Instandhaltung) sowie von Werkzeugen (Teamleitung Werkzeugbau). Bei technischen Eskalationsfällen: Priorisierung der erforderlichen Maßnahmen."),
        akv("Kompetenz:", "Entscheidungsbefugnis über die Umsetzung der bestgeeigneten Variante bei Eskalationsthemen (keine Terminierung/Ressourcenzuteilung im Regelbetrieb)."),

        blockHeading("7. Produktionsaufzeichnungen"),
        akvLabel("Verantwortung: Organisatorische Sicherstellung, dass Produktionsaufzeichnungen den Anforderungen aus ISO 9001 (§7.5.2/7.5.3) entsprechen:"),
        bullet("Vorhanden/vollständig – erforderliche Aufzeichnungen werden tatsächlich erstellt und geführt"),
        bullet("Eindeutig/korrekt identifizierbar – Kennzeichnung (Titel, Datum, Ersteller, Referenznummer)"),
        bullet("Versioniert – Änderungen sind nachvollziehbar"),
        bullet("Aufbewahrung – gemäß Record-Retention-Policy"),
        bullet("Zugänglich/lesbar/geschützt – auffindbar und geschützt vor Verlust/unbefugtem Zugriff"),
        akv("Aufgabe:", "Regelmäßige/stichprobenhafte Kontrolle der produktionsrelevanten Aufzeichnungen (z. B. Prüfbegleitkarte, Schichtlogbuch [Schichtführer], Maschinen-/Prozessdaten, Wartungsprotokolle) auf diese Kriterien; Veranlassung von Korrekturen bei Abweichungen."),
        note("Abgrenzung: Vorserienbezogene Dokumente (z. B. Erstmusterprüfberichte, FMEAs) sind nicht Teil dieser Aufgabe – sie sind in der Produkt-/Projekttechnik verortet."),

        blockHeading("8. Reklamationen / QMB-Zusammenarbeit"),
        p("QMB ist eine normativ geforderte Funktion und vertritt die Organisation nach außen in Qualitätsangelegenheiten – nicht nur gegenüber Kunden, sondern auch gegenüber Lieferanten und bei der Überwachung von Partnern im Produktionsnetzwerk (Lohnfertigung). QS deckt demgegenüber die internen Qualitätsbelange ab: Sperren, Beurteilung, Grenzmusterkataloge, Erststückfreigaben sowie interne Maßnahmen zur Verbesserung und Vermeidung von Reklamationen."),
        akv("Aufgabe:", "Unterstützung von QMB bei der Bearbeitung von Reklamationen (Kunden, Lieferanten, Netzwerkpartner/Lohnfertiger) durch Bereitstellung produktionsseitiger Informationen (Ursachenanalyse, Sofort-/Korrekturmaßnahmen) für die externe Kommunikation. Die inhaltliche Entscheidung über und Umsetzung von Korrekturmaßnahmen auf Produktionsseite erfolgt gemäß Themenblock 5."),

        blockHeading("9. Lehrlingsausbildung"),
        akv("Verantwortung (keine operative Aufgabe):", "Verantwortlich für die Lehrlingsausbildung im Bereich Produktion. Operativ wird die Ausbildung durch zwei separate Lehrlingsausbildner wahrgenommen: Kunststofftechniker – Ausbildner: Techniker im Bereich Automatisierung/Instandhaltung; Werkzeugbautechniker – Ausbildner: Teamleitung Werkzeugbau."),

        blockHeading("10. Sperren von fehlerhaften Produkten"),
        akv("Regelfall (Aufgabe):", "Umsetzung der Sperrentscheidung von QS/PQB – der Produktionsleiter folgt hier zu 100 % der fachlichen Beurteilung durch QS/PQB."),
        akvLabel("Unklare/strittige Fälle (Kompetenz, gemeinsame Entscheidung mit QS/PQB): Abwägung zwischen Reklamationsrisiko und Sperrkosten:"),
        bullet("Vertagung der endgültigen Entscheidung (z. B. Rücksprache mit Kunde/GF am Folgetag), Produktion läuft in der Zwischenzeit weiter"),
        bullet("Trennung zwischen Produktions- und Lieferfreigabe: Teile werden weiterproduziert (z. B. Engpassanlage), aber zunächst nur für die Auslieferung gesperrt"),

        blockHeading("11. Bemusterungs-Eskalation (multidisziplinäre Abstimmung)"),
        p("Bemusterung (Werkzeug, Automatisierung, Material, Spritzgussparameter) obliegt der Rolle Prozesstechnik und Bemusterung. Die Kundenfreigabe nach Vorstellung serienfallender Teile entspricht dem normativ geforderten Produktfreigabeprozess. Danach ist Prozess/Referenznummer/Werkzeug zur Vorserie frei (z. B. für Run@Rate) – mangels ausreichender Kundenbedarfe wird jedoch oft schon vorproduziert, bevor Run@Rate abgeschlossen ist; das Herstellungsrisiko dieser Vorproduktion liegt bei der Produktion (vergleichbar der „Interim Approval“ im PPAP-Prozess)."),
        akv("Aufgabe:", "Kontrolle des Bemusterungsprozesses aus Produktionssicht."),
        akvLabel("Kompetenz: Eskalationsinstanz bei mehreren Varianten oder Risikofragen – multidisziplinäre Abstimmung zwischen:"),
        bullet("Produktionsleitung"),
        bullet("Abteilungsleitung Produkt-/Projekttechnik"),
        bullet("ggf. QMB"),
        bullet("in seltenen Fällen Leitung SCM (z. B. Auslieferbehälter, Verpackungsvorschriften)"),
        note("Der formale Projektabschluss (Prozessreview/Workflow aller Abteilungsleiter, dokumentiert in DocuWare) ist ein separater, bereits etablierter Schritt."),

        blockHeading("12. Werkzeugoptimierungen in Absprache mit PT (Produkt-/Projekttechnik)"),
        p("Fall 1 – vor Serienstart: läuft im Rahmen des Vorserienprozesses (siehe Themenblock 11)."),
        akvLabel("Fall 2 – nach Serienstart, aus Produktionssicht (Qualitäts-/Kostengründe, technische Werkzeugänderung und/oder erneute Kundenfreigabe erforderlich) – Aufgabe:"),
        bullet("Entgegennahme des Optimierungsbedarfs, herangetragen von Prozesstechnik und Bemusterung, Werkzeugbau oder (seltener) direkt von Schichtführern"),
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
        akv("Verantwortung (alle unterstellten Mitarbeiter, auch die der TeamleiterInnen, z. B. Einsteller/Rüster):", "Grundsätzliche Verantwortung für Aus- und Weiterbildung sowie Unterweisung – Schwerpunkt auf Sicherstellung, dass die Durchführung durch die TeamleiterInnen oder andere Fachabteilungen (z. B. HR, QS, SVP, SFK) erfolgt."),

        blockHeading("Vertretung"),
        akvLabel("Struktur: dreiteilige, fest zugeordnete Vertretung nach Fachbereichen:"),
        bullet("Organisation/Personal → Produktionskoordination"),
        bullet("Technik → Prozesstechnik und Bemusterung"),
        bullet("Qualität → QS Produktion"),
        akv("Kompetenz:", "Festlegung dieser Vertretungsregelung sowie Übertragung der jeweiligen Teilbefugnisse an die drei Vertretungsfunktionen."),
        akvLabel("Umfang der übertragenen Befugnisse:"),
        bullet("Regelfall (kurzfristige Abwesenheit): Vertretung übt die Aufgaben/Kompetenzen des Fachbereichs aus, jedoch nicht die weitreichendsten Entscheidungsbefugnisse (z. B. Neueinstellungen)"),
        bullet("Bei längerer Abwesenheit (Richtwert 4–6 Wochen): erweiterte Befugnisse – auch weitreichende Entscheidungen gehen auf die Vertretung über"),

        // ============ TEAMLEITUNGSFUNKTIONEN (GRUPPENÜBERSCHRIFT) ============
        roleHeading("Teamleitungsfunktionen (Führungsrollen im Hauptprozess und in Unterstützungsprozessen)"),
        note("Umfasst: Teamleitung Spritzguss-Produktion (Schichtführer), Montage, Endfertigung, Lager, Instandhaltung, Werkzeugbau."),

        // ============ GEMEINSAME BASIS: FÜHRUNGSROLLEN IM HAUPTPROZESS ============
        h("Gemeinsame AKV-Basis: Führungsrollen im Hauptprozess", HeadingLevel.HEADING_2),
        note("Gilt für Teamleitung Spritzguss-Produktion (Schichtführer), Teamleitung Montage, Teamleitung Endfertigung, Teamleitung Lager (End2End-Auftragsabwicklung, Turtle-Diagramm-Logik: Input-Bereitstellung/Transformation/Output-Versand). Allgemeine Punkte werden hier einmal dokumentiert; die einzelnen Rollen unten enthalten nur noch ihre spezifischen Ergänzungen."),

        blockHeading("A. Prozessmittelüberwachung und Parametrierung"),
        akvLabel("Aufgabe:"),
        bullet("Überwachung der im jeweiligen Prozessschritt eingesetzten Maschinen, Anlagen, Werkzeuge und Vorrichtungen auf ordnungsgemäßen Zustand und korrekte Einstellung/Parametrierung – z. B. Spritzgussmaschinen (Teamleitung Spritzguss-Produktion), Montageautomaten/Vorrichtungen (Teamleitung Montage), Bearbeitungs-/Klebeanlagen (Teamleitung Endfertigung), Kommissionier-/Wiege-/Fördertechnik (Teamleitung Lager)"),
        bullet("Feinjustierung innerhalb definierter Grenzen auf Basis der Ergebnisqualität, soweit für den Bereich zutreffend"),
        akvLabel("Kompetenz:"),
        bullet("Eigenständige fachliche Entscheidung im Rahmen der bereichseigenen Prozessmittel"),
        bullet("Bei technischen Störungen: Eskalation an die zuständige Fachrolle (Teamleitung Instandhaltung für Maschinen/Anlagen, Teamleitung Werkzeugbau für Werkzeuge, Automatisierung für automatisierte Systeme) – konkret durch Eintrag in die jeweilige Aufgabenliste von Instandhaltung bzw. Werkzeugbau"),

        blockHeading("B. Ergebnisverantwortung Qualität/Quantität"),
        akv("Verantwortung:", "Sicherstellung der geplanten Produktionsmenge und der geforderten Qualität im jeweiligen Verantwortungsbereich. Bei Abweichungen von der Produktionsplanung (z. B. durch Störungen): Rückmeldung an Produktionsplanung/Produktionsleitung."),

        blockHeading("C. Fehlerbewertung, Sperren, Transport gesperrter Ware"),
        akv("Aufgabe:", "Bewertung gemeldeter Fehler gemeinsam mit PQB auf Schicht-/Team-Ebene; Entscheidung über Sperrung fehlerhafter Produkte. Anweisung an Lager bzw. Produktionslogistiker zum Transport gesperrter Ware ins gesperrte Lager. Zusätzlich: Rückmeldung fehlerhafter Kaufteile an PQB/Wareneingangskontrolle – da die Wareneingangsprüfung überwiegend stichprobenartig erfolgt, werden Fehler bei Kaufteilen häufig erst bei der Weiterverarbeitung festgestellt (bei Teamleitung Montage aufgrund des hohen Kaufteilanteils verstärkt relevant)."),

        blockHeading("D. Personalverantwortung"),
        akv("Verantwortung:", "Personalverantwortung für die unterstellten Mitarbeiter des Bereichs, inkl. Sicherheit, Ordnung und Sauberkeit am Arbeitsplatz. Erstverantwortung für disziplinarische Maßnahmen (Produktionsleiter als Eskalationsstufe). Ausnahme Teamleitung Lager: disziplinarische Eskalationsstufe ist dort der Abteilungsleiter SCM/Logistik, nicht der Produktionsleiter (siehe 7.5.3.7)."),
        akv("Aufgabe:", "Personalführung des Bereichs (Einteilung, Feedback, Konfliktmanagement)."),

        blockHeading("E. Produktions- und Qualitätsaufzeichnungen"),
        akv("Aufgabe:", "Durchführung/Erstellung der vereinbarten Produktions- und Qualitätsaufzeichnungen des Bereichs (z. B. Prüfbegleitkarte)."),

        blockHeading("F. Reststoff-/Abfallentsorgung"),
        akv("Aufgabe:", "Sortenreine Entsorgung der im jeweiligen Prozessschritt anfallenden Reststoffe/Abfälle in die vorgeschriebenen Behälter/Container – z. B. ausgespritztes Material (Teamleitung Spritzguss-Produktion), Verpackungsreste/Stanzabfälle (Teamleitung Montage), Schleifstaub/Klebstoffreste (Teamleitung Endfertigung)."),

        blockHeading("G. Einfache Wartungstätigkeiten"),
        akv("Aufgabe:", "Durchführung einfacher Wartungstätigkeiten an den bereichseigenen Betriebs-/Hilfsmitteln (z. B. Reinigung, Schmierung). Tiefergehende Wartung/Reparatur/Instandhaltung obliegt Teamleitung Instandhaltung bzw. Teamleitung Werkzeugbau."),

        blockHeading("H. Freigabeprüfungen"),
        akv("Aufgabe:", "Erststück-/Letztstückfreigabe sowie erneute Freigabe nach geplanten/ungeplanten Produktionsunterbrechungen >30 min, jeweils gemeinsam mit PQB lt. Prüfbegleitkarte."),

        blockHeading("I. Poka-Yoke-Verifizierung („Dummy-Prüfung“)"),
        p("Gilt für Bereiche mit integrierten (In-Line-)Prüfanlagen."),
        akv("Aufgabe:", "Regelmäßige Durchführung der vorgeschriebenen Funktionsprüfung dieser Prüfanlagen mittels Referenz-/Prüfteilen (Gut-/Schlechtteile), um sicherzustellen, dass fehlerhafte Teile zuverlässig erkannt werden. Prüffrequenz gemäß Lenkungsplan (Control Plan)."),

        blockHeading("J. Kundenreklamationen – Sofortmaßnahmen"),
        akvLabel("Aufgabe:"),
        bullet("Umsetzung von Sofortmaßnahmen bei Kundenreklamationen: 100%-Kontrolle der betroffenen Teile/Bestände, Sensibilisierung und Unterweisung der Mitarbeiter, Mithilfe bei der Eingrenzung des Fehlerzeitraums bzw. des ersten Auftretens"),
        bullet("Sicherstellung der Einhaltung geänderter Arbeitsanweisungen, die im Zuge der Reklamation angepasst wurden (Unterweisung durch Teamleitung oder QS)"),
        akv("Kompetenz:", "Gemeinsame Definition (mit QS) von Vermeidungs- und Abstellmaßnahmen sowie Sicherstellung von deren Einhaltung."),

        // ============ 7.5.3.2 SCHICHTFÜHRER ============
        roleHeading("7.5.3.2 Teamleitung Spritzguss-Produktion (Schichtführer)"),
        note("Führungsrolle im Hauptprozess (siehe oben). Schichtführer und andere TeamleiterInnen unterscheiden sich grundsätzlich nicht; der relevanteste Unterschied ist die Schichtarbeit. Nachfolgend nur die Spritzguss-spezifischen Ausprägungen sowie die schichtspezifische Besonderheit Schichtübergabe."),

        blockHeading("1. Maschinenüberwachung und Parametrierung – Spritzguss-spezifisch"),
        akvLabel("Aufgabe:"),
        bullet("Überwachung der laufenden Produktionsmaschinen während der Schicht – inkl. der (teilweise automatisierten) Materialzuführung – auf Einhaltung der vorgegebenen Prozessparameter (Einstelldatenblatt)"),
        bullet("Auswahl der richtigen Einstelldaten und Übertragen der gültigen Parametersätze auf die Maschine (Umbau/Einstellung)"),
        bullet("Feinjustierung der Parameter innerhalb definierter Grenzen, auf Basis der laufenden Teilequalität, bis die geforderte Bauteilqualität erreicht ist. Grundlage: Rückstellmuster der letzten Produktion, im Prüfplan definierte Merkmale/Maße inkl. Toleranzen, bei besonders komplexen Fällen Erstmuster/Produktionsfreigabemuster aus dem Serienstart. PQB liefert dazu die Qualitätsrückmeldung zu den Teilen und kann fallweise auf Erfahrungsbasis beraten – die Entscheidung über Parameteranpassungen liegt jedoch nicht bei PQB"),
        akvLabel("Kompetenz:"),
        bullet("Eigenständige fachliche Entscheidung über Parameteranpassungen – beruht auf erlerntem Wissen und Erfahrung von Schichtführer/Einsteller, da keine generelle/pauschale Lösung möglich ist (Vielzahl an Parametern und Wechselwirkungen, z. B. Materialchargen)"),
        bullet("Bei technischen Störungen: Eskalation an Teamleitung Instandhaltung (Maschine, automatisierte Materialförderung) bzw. Teamleitung Werkzeugbau (Werkzeugprobleme) bzw. Automatisierung"),
        note("Hinweis: Die „Produktionsfreigabe“ ist derselbe Schritt wie die Erststückfreigabe (siehe Themenblock H oben)."),

        blockHeading("6. Restmaterialentsorgung – Spritzguss-spezifisch"),
        akv("Aufgabe:", "Ausgespritztes Material sortenrein in Restmüllgebinde bzw. vorgeschriebene Container entsorgen."),

        blockHeading("8. Einfache Werkzeug-Wartungstätigkeiten – Spritzguss-spezifisch"),
        akv("Aufgabe:", "Durchführung einfacher Werkzeug-Wartungstätigkeiten am eingebauten Werkzeug (z. B. Reinigung, Schmierung beim Rüstvorgang). Tiefergehende Wartung, Reparatur und Instandhaltung obliegt der Teamleitung Werkzeugbau."),

        blockHeading("9. Schichtübergabe"),
        akv("Aufgabe:", "Durchführung der Schichtübergabe an den nachfolgenden Schichtführer: Weitergabe des aktuellen Produktions- und Qualitätsstatus je Maschine, offener Vorkommnisse und laufender Maßnahmen, dokumentiert im Schichtlogbuch (einziges Dokumentationsmittel für die Schichtübergabe)."),

        // ============ 7.5.3.3 EINSTELLER/RÜSTER ============
        roleHeading("7.5.3.3 Einsteller/Rüster"),
        note("Fachpersonal innerhalb der Produktion (Spritzguss), unterstellt der Teamleitung Spritzguss-Produktion. Keine Teamleitungsfunktion und kein Werker (Maschinenpersonal) – eigenständige Fachrolle. „Rüster“ und „Einsteller“ unterscheiden sich kaum (im Wesentlichen nur in der Parametrierungskompetenz) und werden daher im Dokument quasi-synonym als „Einsteller/Rüster“ geführt."),

        blockHeading("1. Werkzeugeinbau und Grundeinstellung"),
        akvLabel("Aufgabe:"),
        bullet("Mechanischer Einbau/Wechsel der Spritzgusswerkzeuge (Rüstvorgang)"),
        bullet("Einsteller zusätzlich: Vornahme von Grundeinstellungen und eigenständige Anpassung einzelner Parameter"),
        akvLabel("Kompetenz:"),
        bullet("Einsteller: eigenständige Anpassung einzelner Parameter im Rahmen der Grundeinstellung"),
        bullet("Keine eigenständige Freigabekompetenz: Der finale Schritt und die Produktionsfreigabe obliegen der Teamleitung Spritzguss-Produktion in Zusammenarbeit mit dem PQB"),

        blockHeading("2. Transport und Vor-/Nachbereitung von Werkzeugen und Betriebsmitteln"),
        akvLabel("Aufgabe:"),
        bullet("An- und Abtransport der Spritzgusswerkzeuge (aufgrund der Größe meist mit Spezialequipment wie Stapler, Krananlage, Transportplattformen – dafür jeweils zusätzliche Ausbildung/Berechtigung erforderlich)"),
        bullet("Vor- und Nachbereitung aller Betriebsmittel: Reinigung, bedarfsweise Zwischenreinigung, Anschluss von Temperiergeräten, Umbau von Handlingköpfen"),

        // ============ 7.5.3.4 MONTAGE ============
        roleHeading("7.5.3.4 Teamleitung Montage"),
        note("Führungsrolle im Hauptprozess (siehe oben). Besonderheit gegenüber Teamleitung Spritzguss-Produktion: Die Teamleitung Montage arbeitet operativ mit (kein reines Führungs-/Überwachungsprofil)."),

        blockHeading("1. Ausführung der Montagetätigkeiten"),
        akv("Aufgabe:", "Durchführung der Montagetätigkeiten – sowohl an manuellen Montagetischen als auch an Montageautomaten (integrierter Bestandteil der Montage, ebenfalls durch Montagepersonal betreut) – gemäß Produktions- bzw. Auftragsplanung. Bei Montageautomaten zusätzlich: Betrieb, Überprüfung des störungsfreien Betriebs, kleinere Wartungsarbeiten und Störungsmeldung an Instandhaltung."),
        note("Abgrenzung zu Teamleitung Spritzguss-Produktion: Dort überwacht/parametriert die Teamleitung die Maschinen, die Werker führen die Handarbeiten aus. Bei Montage arbeitet die Teamleitung selbst aktiv operativ mit."),

        blockHeading("2. Qualitätskontrolle"),
        akv("Aufgabe:", "Qualitätskontrolle der montierten Produkte gemäß Arbeitsanweisung."),

        blockHeading("3. Materialbereitstellung am Arbeitsplatz"),
        p("Die Montage verfügt über zwei bereichsnahe Lagerbereiche – ein Lager für Halbfertigfabrikate und ein vergleichsweise großes Kaufteilelager. Einlagerung, Organisation, Lagerstand und Kennzeichnung dieser Lagerbereiche erfolgen durch die Produktionslogistik, nicht durch die Montage."),
        akv("Aufgabe:", "Entnahme der benötigten Materialien (Kaufteile, Halbfertigfabrikate) aus den bereichsnahen Regalen/Blocklagern zu den Montagetischen, für den aktuellen und die nachfolgenden Aufträge – durch Montage-Mitarbeiter und die Teamleitung Montage selbst."),

        blockHeading("4. Verpackung in Ausliefergebinde"),
        p("Da sowohl an den Montagetischen als auch an den Montageautomaten größtenteils fertige, versandfähige Teile produziert werden, die direkt ins Versandlager und anschließend zum Kunden gehen, fällt bei einem Großteil der Montage-Teile die Verpackung an."),
        akv("Aufgabe:", "Verpackung der fertigen Teile (aus Montagetischen und Montageautomaten) in die vorgesehenen Ausliefergebinde."),

        // ============ 7.5.3.5 ENDFERTIGUNG ============
        roleHeading("7.5.3.5 Teamleitung Endfertigung"),
        note("Führungsrolle im Hauptprozess (siehe oben). Teamleitung Endfertigung = Produktionskoordination in Personalunion, daher keine regelmäßige operative Mitarbeit wie bei Teamleitung Montage."),

        blockHeading("1. Aufgabenbereich Fertigungsschritte"),
        p("Endfertigung übernimmt Fertigungsschritte, die nicht bereits im Spritzguss integriert sind – insbesondere nachträgliches Entgraten/Schleifen von Spritzgussteilen, Stanzen sowie Kleben von Zusatzteilen (unlösbares Fügen). Abgrenzung zu Montage: Montage komplettiert/fügt lösbar (z. B. Verschrauben), Endfertigung führt Fertigungsschritte aus bzw. fügt unlösbar. Der Aufgabenumfang ist dynamisch, da Fertigungsschritte nach Möglichkeit vorgelagert in den Spritzguss integriert werden."),
        akv("Aufgabe:", "Im Unterschied zu Teamleitung Montage arbeitet die Teamleitung Endfertigung nicht regelmäßig operativ mit – sie übernimmt zusätzlich die Funktion Produktionskoordination (Personalunion). Operative Mitarbeit erfolgt nur ausnahmsweise bei Bedarfsspitzen, im Sinne ihrer Verantwortung für die Liefertreue."),

        blockHeading("2. Überwachung Produktionsparameter und Vormaterialien/Betriebsstoffe"),
        akv("Aufgabe:", "Überwachung und Einhaltung der Produktionsparameter sowie der ausschließlichen Verwendung geeigneter Vormaterialien/Betriebsstoffe – insbesondere Sicherstellung der Haltbarkeit/Gültigkeit des verwendeten Klebstoffs (kein Einsatz abgelaufener Klebstoffchargen)."),

        // ============ 7.5.3.6 PRODUKTIONSKOORDINATION ============
        roleHeading("7.5.3.6 Produktionskoordination (Vertretung des Produktionsleiters – Organisation/Personal)"),
        note("= Teamleitung Endfertigung in Personalunion (eine Person, zwei Funktionen) – hier wird nur die Vertretungsfunktion (Organisation/Personal) behandelt. Vertretung des Produktionsleiters, Bereich 1 von 3 (Organisation/Personal); siehe Produktionsleiter, Abschnitt „Vertretung“ für die Gesamtstruktur der drei Vertretungsbereiche."),

        blockHeading("1. Unterstützung des Produktionsleiters in Personal- und Organisationsthemen"),
        p("Die nachfolgenden Punkte erfolgen jeweils als Vorschlag/Konzept und Vorbereitung zur Umsetzung sowie Umsetzungsunterstützung; die Entscheidung liegt beim Produktionsleiter."),
        akvLabel("Aufgabe:"),
        bullet("Urlaubsplanung (Abwesenheitsübersicht im digitalen Arbeitsplatz-Portal „Kienformation-Center“)"),
        bullet("Personalauswahl und -entwicklung"),
        bullet("Erstellung von Schulungsprogrammen und Qualifizierungsunterlagen im Lernmanagementsystem (LMS)"),
        bullet("Konzeptionelle Erarbeitung von Arbeitszeitmodellen (z. B. zur Flexibilisierung und Effizienzsteigerung)"),
        note("Charakter: überwiegend wiederkehrend zu bestimmten Zeitpunkten (z. B. vor Betriebsurlauben, Weihnachtsschließtagen), selten anlassbezogen."),

        blockHeading("2. Abgrenzung zu HR (Personalabteilung)"),
        p("Die Produktionskoordination übt in den genannten Themen eine ergänzende, praxisnahe Funktion aus und ersetzt nicht die Personalabteilung (HR). Sie verbindet zentrale HR-Konzepte und -Methoden stärker mit dem betrieblichen Praxisbezug der Produktion (z. B. Anpassung/Umsetzung zentraler HR-Vorgaben auf die konkreten Abläufe und Bedürfnisse des Produktionsbereichs). Grundsätzliche HR-Zuständigkeiten (z. B. arbeitsrechtliche Themen, Vertragsgestaltung, zentrale Personalprozesse) bleiben unberührt."),

        // ============ 7.5.3.7 LAGER ============
        roleHeading("7.5.3.7 Teamleitung Lager"),
        note("Führungsrolle im Hauptprozess (siehe oben). Organisatorisch ist die Teamleitung Lager dem Abteilungsleiter SCM/Logistik unterstellt, nicht dem Produktionsleiter – abweichend von den übrigen Rollen dieser Gruppe (siehe Themenblock D). Der Produktionsleiter ist nur für die Schnittstelle Lager↔Produktion im Rahmen dieses Dokuments zuständig, nicht für die Lagerprozesse oder die Personalführung allgemein."),

        blockHeading("1. Warenannahme und -ausgang"),
        akv("Aufgabe:", "Be- und Entladen von LKWs (Wareneingang/-ausgang); Kommissionierung und Versand der Aufträge."),

        blockHeading("2. Lagerorganisation"),
        akv("Aufgabe:", "Organisation der (zentralen) Lagerbereiche, Lagerstand und Kennzeichnung; Einlagerung der von den Produktionsbereichen (Spritzguss, Montage, Endfertigung) produzierten Ware."),

        blockHeading("3. Materialvorbereitung Spritzguss"),
        akv("Aufgabe:", "Vortrocknung und Bereitstellung der Rohstoffe (Granulat) sowie Verwaltung und Vorbereitung der Einlegeteile für den Spritzguss."),

        blockHeading("4. Administrative Tätigkeiten"),
        akv("Aufgabe:", "Buchungen im ERP-System (FOSS); Bestellanforderungen an den Einkauf; Bedarfsmeldung bei der Abfallentsorgung."),

        blockHeading("5. Transport gesperrter Ware"),
        akv("Aufgabe:", "Durchführung des Transports gesperrter Ware ins Gesperrt-Lager, auf Anweisung der jeweiligen Teamleitung/Schichtführung."),

        blockHeading("6. Gebinde-Versorgung"),
        akv("Aufgabe:", "Versorgung der Produktion mit Gebinden – bevorzugt möglichst direkt mit Ausliefergebinden, zur Vermeidung von Umpackaufwänden. Falls Auslieferbehälter nicht rechtzeitig zur Verfügung standen: Umpacken der Ware von internen Gebinden in Auslieferungsgebinde."),

        blockHeading("7. Kundenspezifische Komplettierungen (Ausnahmefall)"),
        p("Um unnötigen Aufwand in der Produktion durch Varianten zu vermeiden (kundenspezifische Variantenbildung möglichst spät im Prozess), werden manche kleinere, kundenspezifische Komplettierungsschritte erst im Lager statt in der Montage durchgeführt."),
        akv("Aufgabe:", "Selten Durchführung kleinerer, kundenspezifischer Komplettierungsschritte im Lager gemäß Arbeitsanweisung – eigentlich Montagetätigkeiten, die hier ausnahmsweise vor Versand erledigt werden."),

        // ============ 7.5.3.8 WERKER ============
        roleHeading("7.5.3.8 Werker (Maschinenpersonal, Montagepersonal, Personal Endfertigung)"),
        note("„Werker“ ist kein Einzelbereich, sondern der Sammelbegriff für das operativ tätige Fertigungspersonal in den Bereichen Maschinenpersonal (Spritzguss-Produktion), Montagepersonal und Personal Endfertigung. Der nachfolgende Themenblock gilt inhaltlich identisch für alle drei Bereiche."),

        blockHeading("1. Fertigungstätigkeiten und Qualitätssicherung am Arbeitsplatz"),
        akvLabel("Aufgabe:"),
        bullet("Eigenverantwortliches Beurteilen der produzierten Teile lt. Arbeitsanweisung (AAW)"),
        bullet("Sofortige Meldung von Auffälligkeiten/NIO-Teilen an Schichtführer/Teamleitung bzw. PQB"),
        bullet("Beachten zusätzlicher Q-Hinweise (z. B. temporäre Arbeitsanweisungen)"),
        bullet("Teile entgraten oder montieren lt. Anweisung"),
        bullet("Verpacken und Etikettieren der als i. O. beurteilten Teile lt. Verpackungsvorschrift"),
        bullet("Mitwirkung bei Erststück-/Letztstückfreigabe"),
        bullet("Rückmeldung von Produktionsdaten (Stückzahlen, Ausschussmengen) im FOSS"),
        bullet("Ordnung und Sauberkeit am eigenen Arbeitsplatz (5S)"),
        bullet("Sorgfältiger Umgang mit Prüfmitteln (z. B. Lehren, Messschieber); Meldung bei Beschädigung oder Verlust"),
        akvLabel("Kompetenz-Abgrenzung:"),
        bullet("Keine Abstell-Kompetenz: Die Entscheidung über das Abstellen der Maschine bei Auffälligkeiten liegt beim Schichtführer/der Teamleitung, nicht beim Werker"),
        bullet("Keine Freigabekompetenz für (vermutete) NIO-Teile: Diese dürfen nicht verpackt oder fertiggemeldet werden, bis Schichtführer/Teamleitung gemeinsam mit PQB entschieden haben"),

        // ============ 7.5.3.9 BOXENBAUER ============
        roleHeading("7.5.3.9 Boxenbauer"),

        blockHeading("1. Gebinde-Versorgung und -Rückführung"),
        akvLabel("Aufgabe:"),
        bullet("Abholung voller Gebinde direkt von den Maschinen; Buchung im FOSS (Funk-Modul, QR-Code-Scanner)"),
        bullet("Vorbereitung der Gebinde für die Beschickung: Behälter zusammenbauen/aufklappen, auskleiden bzw. Gefache einbringen, damit die Werker direkt beschicken können; Verschließen und Abtransport befüllter Behälter"),
        bullet("Zerlegen und Abtransportieren kurzfristig nicht benötigter Behälter (z. B. Holzaufsetzrahmen)"),
        bullet("Prüfung der Leergebinde und des Verpackungsmaterials auf ordnungsgemäßen Zustand (beschädigungsfrei, sauber, trocken); Aussonderung mangelhafter Gebinde und Rückmeldung an die Lagerlogistik"),
        bullet("Übergabe von übrig gebliebenem/zu viel bereitgestelltem Material (Leergut, Zwischenlagen, Auskleidungen etc.) an das Lager"),
        bullet("Materialrückbuchungen (Restmengen) im FOSS, durch den Boxenbauer selbst"),

        blockHeading("2. Reinigung Granulattrichter (separate Tätigkeit)"),
        akv("Aufgabe:", "Reinigung des Granulattrichters bei Auftragswechsel an Großmaschinen; Vorbereitung für die nächste sortenreine Befüllung."),
        note("Boxenbauer ist pro Schicht eine exklusive Einteilung (kein Mischbetrieb mit anderen Produktionstätigkeiten am selben Tag)."),

        // ============ 7.5.3.10 PRODUKTIONSLOGISTIKER ============
        roleHeading("7.5.3.10 Produktionslogistiker"),

        blockHeading("1. Materialversorgung und -rückführung Montage"),
        akvLabel("Aufgabe:"),
        bullet("Verwaltung und Sicherstellung der Versorgung mit Kaufteilen, Kartonagen und internen Leergebinden"),
        bullet("Durchführen von Reinigungsarbeiten an Einlegeteilen und Gebinden"),
        bullet("Zu- und Abtransport von Halbfertigteilen (HF) und Fertigteilen (FT) (Gebinde) aus der Montage"),
        bullet("Übergabe der Versandeinheiten an das Lager auf definierten Platz"),
        bullet("Bereitstellung von Leergebinden und Verpackungsmaterial in der Montage"),

        blockHeading("2. Administrative Tätigkeiten (FOSS)"),
        akvLabel("Aufgabe:"),
        bullet("Buchungen prüfen und Korrekturen durchführen"),
        bullet("Korrektur und Rückmeldung von falschen Gewichtsangaben"),
        bullet("Kommunikation mit Lagerverantwortlichen bei Abweichungen"),
        bullet("Abschließen von Produktionsaufträgen im System"),
        bullet("Mitwirkung bei der Pflege/Überprüfung von Stammdaten im ERP-System (z. B. Teilegewicht, Stückliste)"),

        blockHeading("3. Ausschussentsorgung (bereichsübergreifend)"),
        akv("Aufgabe:", "Abwiegen und Entsorgen/Zuführen von Ausschüssen (Recyclingmaterial), Papier, Kartonagen – bereichsübergreifend in allen Produktionsbereichen (nicht auf Montage beschränkt)."),

        // ============ 7.5.3.11 PRODUKTIONSPLANUNG UND -STEUERUNG ============
        roleHeading("7.5.3.11 Produktionsplanung und -steuerung"),
        akv("Verantwortung:", "Die Produktionsplanung und -steuerung ist die zeitliche „Taktgeber“-Funktion der Produktion – sämtliche zeitlichen Abläufe (Auftragsreihenfolge, Kapazitäten, Personaleinsatz) werden von hier aus koordiniert; keine andere Funktion führt Tätigkeiten zeitlich unabhängig von dieser Instanz durch."),

        blockHeading("1. Produktionsfeinplanung und Personalkapazitäten"),
        akvLabel("Aufgabe:"),
        bullet("Produktionsfeinplanung: Einlastung freigegebener FOSS-Aufträge, übersichtliche Darstellung in TIG und auf der Planungstafel (entspricht 7.5.4.2 Feinplanung)"),
        bullet("Zentrale Instanz für die Planung der Personalkapazitäten (Personaleinsatzplanung)"),
        bullet("Einplanung der Betriebsaufträge in der Produktion zur Erfüllung aller relevanten Kundenbedarfe, inkl. Bemusterungsaufträge für Neuprojekte oder Änderungen"),
        bullet("Die Planungslogik ist prozessstufenabhängig: Der Formgebungsprozess (Spritzguss) wird auf Basis von Kundendaten (Lieferpläne/Liefervorschauen) prognosebasiert produziert; die nachgelagerten Prozesse (Endfertigung, Montage, Kommissionierung) sind demgegenüber auftragsbezogen, gesteuert durch konkrete JIT-/JIS-Abrufe"),

        blockHeading("2. Schnittstelle zu Werkzeugbau und Instandhaltung"),
        akv("Aufgabe:", "Abstimmung mit den Teamleitungen Werkzeugbau und Instandhaltung zur Berücksichtigung von deren eigenverantwortlich geplanten Wartungs-/Reparaturthemen im Produktionsplan (Kapazitätsauswirkungen). Die Planungshoheit für diese Themen liegt bei den jeweiligen Teamleitungen selbst."),

        blockHeading("3. Prozess- und Projektarbeit"),
        akv("Aufgabe:", "Anstoß und Mitwirkung bei der Optimierung von Prozessen und Maßnahmen zur Qualitäts- oder Wirtschaftlichkeitsverbesserung sowie bei logistischen und produktionswirtschaftlichen Projekten."),

        blockHeading("4. Operative und administrative Tätigkeiten"),
        akvLabel("Aufgabe:"),
        bullet("Operative Vorbereitung der Produktionsaufträge, Erstellung unterschiedlicher Listen/Tabellen"),
        bullet("Archivierung von Betriebsauftragsdokumenten"),
        bullet("Erstellung der Produktionsaufträge im ERP-System (FOSS)"),
        bullet("Einplanung der Produktionsaufträge im MES-System (Authentig)"),
        bullet("Dokumentation im DocuWare anlegen"),
        bullet("Erstellung und Pflege von Auswertungen, Berichten und Übersichten (Kapazitätsübersichten, Personalzuordnungen, Plantafel, …) im Zusammenhang mit der Produktionsplanung und -steuerung"),

        // ============ 7.5.3.12 DIGITALE PROZESSENTWICKLUNG & LEAN MANAGEMENT ============
        roleHeading("7.5.3.12 Digitale Prozessentwicklung & Lean Management"),
        note("Überschneidungen mit Produktionsplanung und -steuerung: Auftragserstellung im FOSS sowie allgemeine Kapazitätsplanung liegen bei Produktionsplanung und -steuerung; diese Rolle erstellt spezifisch Werkzeugbau-/Bemusterungsaufträge bei Werkzeugänderungen. Projektmitarbeit (Themenblock 3) gilt für beide Rollen gemeinsam."),

        blockHeading("1. Stammdaten- und Prozessoptimierung"),
        akvLabel("Aufgabe:"),
        bullet("Stammdatenpflege von Objekten (Schwerpunkt Werkzeuge und Betriebsmittel) im FOSS/MES"),
        bullet("Prozessdaten- und Werkzeugoptimierung"),
        bullet("Anstoß/Mitwirkung zu/bei IT-Anwendungen (z. B. ERP, DMS, MES, …)"),
        bullet("Anstoß/Mitwirkung bei Digitalisierungsprojekten (3D-Scan, 3D-Druck, RFID, …)"),

        blockHeading("2. Werkzeugänderungen und Neuprojekte"),
        akvLabel("Aufgabe:"),
        bullet("Erstellung von Werkzeugbau-Aufträgen und Bemusterungsaufträgen aufgrund von Werkzeugänderungen (als Ergänzung zur Rolle Produktionsplanung und -steuerung)"),
        bullet("Machbarkeitsprüfungen bzgl. rechtzeitiger Bereitstellung von Werkzeugen und Vorrichtungen im Rahmen dieser Werkzeugänderungen/Neuprojekte"),
        bullet("Vergabe und Verwaltung von Lagerplätzen für Werkzeuge, Vorrichtungen, Mess-/Hilfsmittel (Systematik/Zuweisung im Lagerverwaltungssystem; operative Pflege/Zustand liegt bei Teamleitung Werkzeugbau)"),

        blockHeading("3. Mitwirkung bei Projekten"),
        akv("Aufgabe:", "Mitarbeit bei logistischen und produktionswirtschaftlichen Projekten (analog Produktionsplanung und -steuerung)."),

        blockHeading("4. Digitale Standards und Visualisierung"),
        akv("Aufgabe:", "Erstellung und Pflege digitaler Arbeitsanweisungen und visueller Standards (elektronische Plantafeln, Bildschirminformationen)."),

        blockHeading("5. Lean-/KVP-Koordination"),
        akvLabel("Aufgabe:"),
        bullet("Konzeptionelle und koordinierende Funktion für das betriebliche KVP-/Lean-Programm (Methodik, Workshops, Wertstromanalysen); operative Umsetzung erfolgt durch die einzelnen Teamleitungen"),
        bullet("Mitwirkung bei der Betreuung des digitalen Verbesserungsvorschlagswesens „Gut+ Vorschläge“ (App im Arbeitsplatz-Portal „Kienformation-Center“)"),

        blockHeading("6. Konzeption von Poka-Yoke-/Fehlervermeidungslösungen"),
        akv("Aufgabe:", "Konzeption von Poka-Yoke-/Fehlervermeidungslösungen (z. B. ad-hoc-Hilfsmittel via 3D-Druck); Gegenstück zur laufenden Verifizierung („Dummy-Prüfung“), die bei den Teamleitungen liegt."),

        // ============ 7.5.3.13 PQB ============
        roleHeading("7.5.3.13 Qualitätsprüfer/in (PQB)"),
        note("PQB ist keine Teamleitungsfunktion und wird daher vollständig eigenständig beschrieben, auch dort, wo PQB und Teamleitung im selben Prozess zusammenwirken (z. B. Sperrentscheidung, Freigabeprüfungen). PQB sind schichtbezogen aufgeteilt; QS (Qualitätssicherung Produktion) koordiniert übergreifend und ist organisatorisch übergeordnet."),

        blockHeading("1. Fertigungsbegleitende Qualitätsprüfung und Dokumentation"),
        akvLabel("Aufgabe:"),
        bullet("Durchführung von fertigungsbegleitenden Qualitätsprüfungen"),
        bullet("Dokumentation der Prüf- und Messergebnisse im Prüfdaten-System (Q Studio)"),
        bullet("Erfassen von festgestellten Fehlern"),

        blockHeading("2. Reklamationsbearbeitung und Maßnahmenverfolgung"),
        akvLabel("Aufgabe:"),
        bullet("Mitarbeit bei der Reklamationsbearbeitung"),
        bullet("Maßnahmenverfolgung bei Prozessverbesserungen, die durch vorangegangene Q-Abweichungen (unabhängig ob intern oder extern) ausgelöst wurden"),

        blockHeading("3. Qualitätsschulungen"),
        akv("Aufgabe:", "Durchführung von Qualitätsschulungen, Schwerpunkt Werker."),

        blockHeading("4. Sperrentscheidung bei Qualitätsabweichungen"),
        akvLabel("Aufgabe:"),
        bullet("Eigenständiges, unmittelbares Tätigwerden bei Qualitätsabweichungen, die im Rahmen der eigenen laufenden Prüftätigkeit vor Ort festgestellt werden (der PQB ist überwiegend in der Produktion anwesend)"),
        bullet("Hinzuziehung durch die Teamleitung bei durch Werker oder Teamleitung festgestellten Abweichungen, die nicht behoben werden können oder deren Teilequalität unklar ist; gemeinsame Beratung mit der Teamleitung über die Teilequalität"),
        akv("Kompetenz:", "Eigenständige Entscheidung, den Prozess und/oder die betroffenen Teile unmittelbar zu stoppen, eindeutig zu kennzeichnen und abzusondern, wenn die Qualität nicht ausreicht – bis eine Lösung gefunden bzw. die Freigabe erteilt ist."),

        blockHeading("5. Freigabeprüfungen"),
        akv("Aufgabe:", "Gemeinsam mit der Teamleitung: Erststück-/Letztstückfreigabe sowie erneute Freigabe nach geplanten/ungeplanten Produktionsunterbrechungen über 30 Minuten, laut Prüfbegleitkarte."),

        // ============ 7.5.3.14 ALLE MITARBEITER ============
        roleHeading("7.5.3.14 Alle Mitarbeiter"),
        note("Generische Rolle – gilt für jeden Beschäftigten, zusätzlich zu den jeweiligen rollenspezifischen AKV-Punkten."),

        blockHeading("1. Information und Arbeitserbringung"),
        akvLabel("Aufgabe:"),
        bullet("Informationen auf der Anschlagtafel sowie auf digitalen Informationsmedien beachten (Bildschirminformationen sowie das digitale Arbeitsplatz-Portal „Kienformation-Center“, u. a. für aushangpflichtige Gesetze/Mitteilungen)"),
        bullet("Qualitative und quantitative Arbeitserbringung"),
        bullet("Bewusstsein für die Auswirkungen der eigenen Tätigkeit auf Kundenanforderungen und Produktqualität"),

        blockHeading("2. Umwelt und Ressourcen"),
        akvLabel("Aufgabe:"),
        bullet("Durchgängiges Umweltbewusstsein"),
        bullet("Sorgsamer Umgang mit Ressourcen"),

        blockHeading("3. Verbesserung und Ordnung"),
        akvLabel("Aufgabe:"),
        bullet("Aktive Mitarbeit bei Verbesserungsmaßnahmen"),
        bullet("Ordnung und Sauberkeit am Arbeitsplatz (5S)"),

        blockHeading("4. Pflichten gemäß ArbeitnehmerInnenschutzgesetz (ASchG)"),
        akvLabel("Aufgabe:"),
        bullet("Befolgen der Sicherheitsvorschriften und Anweisungen"),
        bullet("Bestimmungsgemäße Verwendung von Maschinen, Arbeitsmitteln, Arbeitsstoffen und persönlicher Schutzausrüstung (PSA)"),
        bullet("Sicherheitseinrichtungen nicht eigenmächtig entfernen oder außer Betrieb setzen"),
        bullet("Unverzügliche Meldung festgestellter Mängel oder Gefahren an die vorgesetzte Stelle bzw. Sicherheitsvertrauensperson (Kontaktdaten über die Liste „Beauftragte Personen“ im Kienformation-Center auffindbar, dort auch Sicherheitsfachkraft und Ersthelfer gelistet)"),
        bullet("Teilnahme an Sicherheits- und Gesundheitsunterweisungen"),
        bullet("Rücksichtnahme auf die Sicherheit und Gesundheit anderer Personen, die von der eigenen Tätigkeit betroffen sein können"),

        blockHeading("5. Allgemeine arbeits-/dienstvertragsrechtliche Pflichten"),
        akvLabel("Aufgabe:"),
        bullet("Sorgfältiger Umgang mit anvertrautem Eigentum und Arbeitsmitteln des Arbeitgebers"),
        bullet("Melde-/Informationspflichten (z. B. Verhinderungsgründe, Krankmeldung)"),

        // ============ GEMEINSAME BASIS: FÜHRUNGSROLLEN IN UNTERSTÜTZUNGSPROZESSEN ============
        h("Gemeinsame AKV-Basis: Führungsrollen in Unterstützungsprozessen", HeadingLevel.HEADING_2),
        note("Gilt für Teamleitung Instandhaltung und Teamleitung Werkzeugbau – Fach-/Führungsrollen, die Ressourcen/Betriebsmittel bereitstellen bzw. betriebsbereit halten, aber nicht Teil des Material-/Auftragsflusses selbst sind (im Unterschied zu den Rollen oben)."),

        blockHeading("A. Personalverantwortung"),
        akv("Verantwortung:", "Personalverantwortung für die unterstellten Mitarbeiter des Bereichs, inkl. Sicherheit, Ordnung und Sauberkeit am Arbeitsplatz. Erstverantwortung für disziplinarische Maßnahmen (Produktionsleiter als Eskalationsstufe)."),
        akv("Aufgabe:", "Personalführung des Bereichs (Einteilung, Feedback, Konfliktmanagement)."),

        blockHeading("B. Aufgabenliste als zentraler Eingangskanal"),
        akv("Aufgabe:", "Abarbeitung/Priorisierung der Aufgabenliste, in die verschiedene Stakeholder (andere Teamleitungen, Produktionsleitung) Störungen/Anliegen eintragen."),

        // ============ 7.5.3.15 INSTANDHALTUNG ============
        roleHeading("7.5.3.15 Teamleitung Instandhaltung"),
        note("Zuständig für Maschinen, Anlagen und Infrastruktur inkl. Betriebsmittel, Fertigungshilfsmittel, Roboter und automatisierte Anlagen. Berichtet im Regelbetrieb direkt an den Produktionsleiter."),

        blockHeading("1. TPM-System"),
        akv("Verantwortung:", "Betrieb eines dokumentierten, geplanten Instandhaltungssystems für die prozessrelevanten Anlagen; Einhaltung sicherheitstechnischer und gesetzlicher Bestimmungen."),
        akvLabel("Aufgabe:"),
        bullet("Durchführung von Reparaturen an Anlagen, Maschinen, Infrastruktur und Betriebsmitteln (reaktive Instandsetzung)"),
        bullet("Planung, Anfertigung und Installation neuer/geänderter Betriebsmittel (z. B. Vorrichtungen, Anbaugeräte, Temperiergeräte)"),
        bullet("Optimierung bestehender Anlagen"),
        bullet("Mitwirkung an KVP/5S/Kaizen"),
        bullet("Vorausschauende und ggf. vorbeugende Instandhaltung nach Wartungsplan"),
        bullet("Ersatzteilhaltung: Kleinmateriallager für elektrische, pneumatische, elektronische und hydraulische Standardkomponenten (inkl. Kabel, Stecker u. Ä.); größere Komponenten (z. B. Hydraulikpumpen, Förderschnecken) an verschiedenen Lagerorten (u. a. Werkzeuglager). Kritische, wertige Ersatzteile werden im ERP-System (FOSS) bestandsgeführt, Verbrauchsmaterialien nicht separat. Da die meisten Ersatzteile von den Maschinenherstellern kurzfristig (binnen weniger Tage, bei Bedarf express) zur Verfügung gestellt werden, erfolgt die Beschaffung überwiegend anlassbezogen statt über große eigene Lagerbestände"),
        bullet("Verpackung/Konservierung von Anlagen/Betriebsmitteln bei Lagerung"),
        bullet("Jährliche Überprüfung des Wartungsplans"),
        bullet("Anlage und Pflege der Objektstammdaten (FOSS) für alle relevanten Anlagen, Betriebsmittel, Vorrichtungen etc., inkl. hinterlegter zyklischer Wartungszeitpunkte"),
        bullet("Beauftragung und Beaufsichtigung relevanter Prüfstellen für gesetzlich vorgeschriebene Prüfungen (z. B. Leitern, Hebezeuge, Anschlagmittel)"),
        bullet("Abarbeitung der Aufgabenliste (Störungsmeldungen)"),
        akv("Kompetenz:", "Festlegung von Instandhaltungszielen/-kennzahlen (z. B. OEE, MTBF, MTTR); bei Gefahr im Verzug Anlagen abstellen (Not-Halt-Kompetenz), mit Informationspflicht an die vorgesetzte Stelle. Meldepflicht bei Anlagenstörungen/Unfällen an die vorgesetzte Stelle."),

        blockHeading("2. Abgrenzung zu Hersteller, Fremdfirmen und Automatisierung"),
        p("Instandhaltung deckt Wartung/Reparatur im Rahmen der eigenen Kapazitäten und Fachkenntnisse ab. Bei Reparaturen, die spezielles Herstellerwissen/-ersatzteile erfordern, erfolgt eine Beauftragung/Koordination mit dem jeweiligen Anlagenhersteller."),
        p("Für Infrastrukturthemen außerhalb der eigenen Fachkenntnisse (z. B. Klimaanlagen, Heizung) werden Wartung und Reparatur durch externe Fremdfirmen durchgeführt, die von der Instandhaltung regelmäßig beauftragt werden."),
        p("Bei automatisierten Anlagen: mechanische/elektrische Instandhaltung liegt bei Instandhaltung, Programmierung/Konfiguration und tiefergehende automatisierungstechnische Themen liegen bei der Rolle Automatisierung."),

        // ============ 7.5.3.16 WERKZEUGBAU ============
        roleHeading("7.5.3.16 Teamleitung Werkzeugbau"),
        note("Zuständig für Werkzeugbau sowie Werkzeugwartung, -reparatur und -instandhaltung. Berichtet im Regelbetrieb direkt an den Produktionsleiter. Zusätzlich Lehrlingsausbildner für Werkzeugbautechniker."),
        note("Rollenstruktur: Die Teamleitungsfunktion ist eine Funktion und umfasst die organisatorischen, personellen und disziplinarischen Aufgaben. Vertiefte fachlich-technische Kompetenzen (Werkzeugbau-Handwerk) werden durch langjährig erfahrene Mitarbeiter ergänzt, die keine eigene Führungsfunktion innehaben."),

        blockHeading("1. Werkzeug-/Betriebsmittelmanagement"),
        akv("Verantwortung:", "Werkzeugbau sowie Wartung/Reparatur/Instandhaltung der Werkzeuge (inkl. Kundenwerkzeuge)."),
        akvLabel("Aufgabe:"),
        bullet("Werkzeugkennzeichnung (Kennnummer, Status, Eigentümer, Standort) – Kundenwerkzeuge dauerhaft/sichtbar gekennzeichnet"),
        bullet("Lagerung und Schutz der Werkzeuge vor Beschädigung/Verschleiß"),
        bullet("Rüst-/Werkzeugwechselprozesse"),
        bullet("Verschleißteile-Management: systematischer Umgang mit Verschleißteilen am Werkzeug (Erkennung, Austausch, Dokumentation). Eine Wartungsstrategie mit hinterlegten Soll-Schusszahlen, erfassten Ist-Schusszahlen und Erreichungsgrad löst die Wartung aus. Werkzeuge werden während Wartung/Reparatur über den LCST (LifeCycle Status) bzw. den Betriebsmittelstatus für die Produktion gesperrt und nach Abschluss wieder für die Planung und Steuerung freigegeben"),
        bullet("Dokumentation von Werkzeugänderungen/-modifikationen inkl. Änderungsstand"),
        bullet("Abarbeitung der Aufgabenliste"),
        akv("Kompetenz:", "Entscheidung über Werkzeugstatus (Produktion/Reparatur/Aussonderung); Sperren von Werkzeugen/Vorrichtungen und Einleitung von Korrekturmaßnahmen; Produktionsstopp bei Gefahr oder Formbeschädigung (Not-Halt-Kompetenz)."),

        blockHeading("2. Ergänzende Aufgaben"),
        akvLabel("Aufgabe:"),
        bullet("Bedarfserhebung und Bestellabwicklung von Roh-, Hilfs- und Betriebsstoffen/-mitteln für den Werkzeugbau"),
        bullet("Gestaltung der Arbeitsplätze und Arbeitsvorbereitung im Werkzeugbau"),
        bullet("Fehlermeldung bei Produktionsstörungen durch Werkzeuge an den Produktionsleiter"),

        blockHeading("3. Abgrenzung zu Prozesstechnik und Bemusterung/Produkt-Projekttechnik"),
        p("Werkzeugbau ist zuständig für Bau, Wartung, Reparatur und Instandhaltung der Werkzeuge auf Basis der bestehenden, freigegebenen technischen Spezifikation. Technische Änderungen am Werkzeug (Designänderungen, die Form/Funktion betreffen und ggf. eine erneute Kundenfreigabe erfordern) liegen nicht in der Entscheidungskompetenz des Werkzeugbaus, sondern werden über Prozesstechnik und Bemusterung bzw. die Produkt-/Projekttechnik entschieden."),

        blockHeading("4. Umgang mit Kundenwerkzeugen"),
        akv("Verantwortung:", "Ordnungsgemäßer Umgang mit im Eigentum des Kunden stehenden Werkzeugen."),
        akvLabel("Aufgabe:"),
        bullet("Nutzung ausschließlich für den vom Kunden vorgesehenen Zweck"),
        bullet("Doppelte Kennzeichnung: Typenschild sowie zusätzliche, dauerhafte Werkzeug-Beschriftung (eingeschweißter Zettel)"),
        bullet("Verwaltung der Werkzeugstammdaten im ERP-System (FOSS): eindeutige Werkzeugnummer, Kundenzuordnung, Änderungsstand, Wartungs-/Reparaturhistorie"),
        bullet("Schutz vor Fremdzugriff: trockene, gesicherte Verwahrung in verschlossenen Hallenbereichen"),
        bullet("Information des Kunden und gemeinsame Abstimmung weiterer Maßnahmen bei Verlust, Beschädigung oder technischen Problemen (Nichteignung)"),
        bullet("Bei Erreichen/Überschreiten der vereinbarten Schusszahl: Anfrage an den Kunden zur Freigabe weiterer Wartungs-/Reparaturkosten und Kostenübernahme"),
        akv("Kompetenz:", "Keine eigenständige Entscheidung über Kostenübernahme oder Weiterverwendung des Werkzeugs jenseits der vereinbarten Schusszahl – diese Entscheidung liegt beim Kunden."),

        // ============ 7.5.3.17 AUTOMATISIERUNG ============
        roleHeading("7.5.3.17 Automatisierung"),
        note("Gehört konzeptionell zur Gruppe Unterstützungsprozesse (analog Werkzeugbau/Instandhaltung), berichtet im Regelbetrieb direkt an den Produktionsleiter. Die Rolle arbeitet teilweise mit externen Partnern zusammen; eine anteilige Ressource kann aus der Instandhaltung stammen."),

        blockHeading("1. Programmierung und Inbetriebnahme"),
        akvLabel("Aufgabe:"),
        bullet("Programmierung und Inbetriebnahme von Automatisierungsanlagen, Robotern und Steuerungstechnik"),
        bullet("Zusammenarbeit mit externen Partnern (z. B. Systemintegratoren, Hersteller-Support) bei komplexeren Anlagen"),

        blockHeading("2. Abgrenzung zu Instandhaltung (Störungsbehebung)"),
        akvLabel("Aufgabe:"),
        bullet("Reguläre Störungen an automatisierten Anlagen werden nach Projektübergabe eigenverantwortlich durch die Instandhaltung behoben"),
        bullet("Hinzuziehung der Automatisierung bei aus der Projektübergabe ungeklärten Punkten oder bei Fehlern, deren Ursache aus dem Zusammenspiel von Mechanik, Elektrik, Elektronik und Programmierung unklar ist (Störungsanalyse)"),

        blockHeading("3. Weiterentwicklung und Automatisierungsgrad"),
        akvLabel("Aufgabe:"),
        bullet("Laufende Verbesserung bestehender Automatisierungslösungen"),
        bullet("Umstellung von manuellen auf (teil-)automatisierte Prozesse aufgrund wirtschaftlicher, qualitativer oder ergonomischer Verbesserungspotenziale oder Notwendigkeiten"),
        bullet("Der Anstoß solcher Projekte kann eigenständig durch die Automatisierung selbst erfolgen oder durch andere Funktionen ausgelöst werden – insbesondere auch durch die Produkt-/Projekttechnik, die ebenfalls eine wesentliche Quelle automatisierungsrelevanter Veränderungen ist"),
        bullet("Die Umsetzung erfolgt stets im multidisziplinären Ansatz, unter Einbindung der relevanten Funktionen (z. B. Prozesstechnik und Bemusterung, QS, Instandhaltung, Produktionsplanung und -steuerung sowie der betroffenen Teamleitungen)"),
        bullet("Nach Umsetzung einer automatisierungsbedingten Prozessänderung: Rückkopplung zu den erforderlichen Prozessfreigaben (Verifizierung/Validierung, dass die Änderung die Produktkonformität nicht beeinträchtigt, vor Wiederaufnahme der Serienproduktion)"),

        blockHeading("4. CE-Konformität bei Gesamtanlagen"),
        akv("Verantwortung:", "Sicherstellung der CE-Konformität bei durch die Automatisierung erstellten/integrierten Gesamtanlagen (die Zusammenführung mehrerer Einzelmaschinen/-komponenten zu einer funktionalen Einheit macht die Automatisierung gemäß Maschinenrichtlinie zum „Hersteller“ der Gesamtanlage)."),
        akvLabel("Aufgabe:"),
        bullet("Durchführung der Risikobeurteilung für die Gesamtanlage"),
        bullet("Erstellung der technischen Dokumentation"),
        bullet("Ausstellung der Konformitätserklärung und Anbringung der CE-Kennzeichnung"),

        // ============ 7.5.3.18 PROZESSTECHNIK UND BEMUSTERUNG ============
        roleHeading("7.5.3.18 Prozesstechnik und Bemusterung"),
        note("Vertretung des Produktionsleiters, Bereich 2 von 3 (Technik). „Bemusterung“ bezeichnet hier die technische Erprobung eines Werkzeugs (Spritzversuche), bei der iterativ passende Spritzparameter ermittelt und ggf. Werkzeugkorrekturen vorgenommen werden, bis ein serienreifes Spritzgussteil erreicht ist – nicht identisch mit der „Erstbemusterung“/dem Erstmusterprüfbericht (PPAP-analog). Fokus dieser Rolle liegt auf der Serie; Vorserienprozesse bei Neuprojekten sind in einer eigenen Anweisung beschrieben."),

        blockHeading("1. Technische Bemusterung im Serienbetrieb"),
        akv("Verantwortung:", "Verifizierung/Validierung von Änderungen am Produktionsprozess (Werkzeuganpassungen, Produktänderungen, Materialwechsel, Chargenschwankungen) vor Wiederaufnahme der Serienproduktion, um sicherzustellen, dass die Produktkonformität nicht beeinträchtigt ist. Abstimmung der Triade Maschine/Werkzeug/Material, dokumentiert in den Einstelldatenblättern mit den jeweiligen Produktionsparametern."),
        akvLabel("Aufgabe:"),
        bullet("Technische Durchführung der Bemusterung (Spritzversuche) bei Werkzeuganpassungen/-reparaturen, Produktänderungen, Materialwechseln oder Chargenschwankungen im laufenden Serienbetrieb – unabhängig davon, ob die zugrunde liegende Werkzeugänderung/-neuanfertigung intern (Werkzeugbau) oder extern gefertigt wurde"),
        bullet("Ermittlung/Festlegung geeigneter Spritzparameter zur Erreichung eines serienreifen Spritzgussteils (Maßhaltigkeit/Toleranzen, Oberflächenbeschaffenheit, Freiheit von Deformationen wie Einfallstellen)"),

        blockHeading("2. Dokumentation"),
        akvLabel("Aufgabe:"),
        bullet("Erstellung von Musterberichten"),
        bullet("Aktualisierung der Einstelldatenblätter"),
        bullet("Ausfüllen von Werkzeugabnahmeprotokollen"),

        blockHeading("3. Abgrenzung zu Produkt-/Projekttechnik und zum Vorserienprozess"),
        p("Koordination mit Werkzeugherstellern (intern/extern), einschließlich Rückmeldung zu Werkzeuganpassungen, Sichtung der Bemusterungsberichte, Ableitung weiterführender Maßnahmen sowie ggf. Vorstellung der Teile beim Kunden, liegen bei der Produkt-/Projekttechnik – außerhalb dieser Rolle und außerhalb des Geltungsbereichs dieses Dokuments."),
        p("Ebenso liegt die Pflege des Lenkungsplans (Control Plan) bei einer Rolle der Produkt-/Projekttechnik, in multidisziplinärer Abstimmung mit RPP (Robust Production Processes) – einem eigenen Team innerhalb der Qualitätsmanagement-Abteilung –, angestoßen durch Kundenforderungen und abgeglichen mit den Ergebnissen/Implikationen der Bemusterung – die Bemusterungsergebnisse dieser Rolle fließen also ein, die Pflege des Dokuments selbst erfolgt aber dort."),
        note("Die formale Erstbemusterung/der Erstmusterprüfbericht bei Neuprojekten liegt bei Produkt-/Projekttechnik gemeinsam mit der Qualitätsmanagement-Abteilung und ist in einer eigenen Anweisung zum Vorserienprozess beschrieben."),

        blockHeading("4. Vertretungsfunktion des Produktionsleiters (Technik)"),
        akv("Aufgabe:", "Vertretung des Produktionsleiters in allen technischen Belangen (Bereich 2 von 3 der Vertretungsstruktur)."),
        akv("Kompetenz:", "Bei Abwesenheit des Produktionsleiters: Eskalationsstelle für technische Fragen, die von Teamleitung Werkzeugbau bzw. Teamleitung Instandhaltung eskaliert werden."),

        // ============ 7.5.3.19 QS ============
        roleHeading("7.5.3.19 QS (Qualitätssicherung Produktion)"),
        note("Vertretung des Produktionsleiters, Bereich 3 von 3 (Qualität) – bewusst außerhalb der Produktionsabteilung angesiedelt (4-Augen-Prinzip, siehe Themenblock 5). Organisatorisch übergeordnet zu den PQB (schichtbezogen aufgeteilt) – QS koordiniert deren Tätigkeit übergreifend."),

        blockHeading("1. Interne Qualitätssicherung und Korrekturmaßnahmen"),
        akvLabel("Aufgabe:"),
        bullet("Interne Qualitätsbelange: Sperren, Beurteilung, Grenzmusterkataloge, Erststückfreigaben sowie interne Maßnahmen zur Verbesserung und Vermeidung von Reklamationen"),
        bullet("Beratung des Produktionsleiters (als Herstellungsverantwortlicher) bei der strukturierten Problemlösung (z. B. 8D-Report) bei internen Qualitätsabweichungen; Beurteilung der vom Produktionsleiter gesetzten Sofort- und Korrekturmaßnahmen; gemeinsame Prüfung der Wirksamkeit"),
        bullet("Freigabe/Entscheidung, ob und wie fehlerhafte Teile nachgearbeitet oder repariert werden dürfen, inkl. erneuter Prüfung danach"),
        note("Ablauf bei Korrekturmaßnahmen: QS stellt Bedarf fest → Produktionsleitung (als Herstellungsverantwortlicher) entscheidet über die konkrete Maßnahme → QS prüft gemeinsam mit der Produktionsleitung die Wirksamkeit und gibt frei (z. B. Entsperren von Teilen/Prozessen)."),

        blockHeading("2. Audits und Prozessüberwachung"),
        akvLabel("Aufgabe:"),
        bullet("Durchführung/Koordination interner Prozess- und Produktaudits in der Produktion (systematische Verifizierung der Prozess-/Produktkonformität, über die laufende PQB-Prüfung hinaus)"),
        bullet("Überwachung, ob bei Prozessabweichungen die im Lenkungsplan festgelegten Reaktionspläne eingehalten werden"),

        blockHeading("3. Koordination der PQB"),
        akv("Aufgabe:", "Organisatorisch übergeordnet zu den schichtbezogen aufgeteilten PQB; koordiniert deren Tätigkeit übergreifend."),

        blockHeading("4. Vertretungsfunktion des Produktionsleiters (Qualität)"),
        akvLabel("Aufgabe:"),
        bullet("Vertritt den Produktionsleiter in allen qualitätsrelevanten Fragen: fehlerhafte Teile im Haus, Reklamationen, Sperren, Nacharbeit, Maschinen abstellen/stoppen"),
        bullet("Korrespondenzfunktion zur Produktionsleitung auf Gesamtebene (analog QMB ↔ Schichtführer/Teamleitung auf Schicht-/Team-Ebene)"),
        akv("Kompetenz:", "Befugnis, die Produktion/den Versand zu stoppen, um Qualitätsprobleme zu korrigieren."),

        blockHeading("5. Organisatorische Sonderstellung"),
        akvLabel("Hinweise:"),
        bullet("Bewusst außerhalb der Produktionsabteilung angesiedelt (4-Augen-Prinzip); organisatorisch der Qualitätsabteilung zugeordnet, die vom QMB auf Abteilungsleiter-Ebene (gleichrangig mit dem Produktionsleiter) geführt wird"),
        bullet("Der Produktionsleiter hat keine Weisungsbefugnis gegenüber QS"),
        bullet("Umgekehrt hat QS fachliche Weisungsbefugnis gegenüber dem Produktionsleiter in Q-Themen (spätestens über den QMB durchsetzbar)"),
        note("Abgrenzung zu QMB: QS deckt interne Qualitätsbelange ab; QMB vertritt extern (Kunden, Lieferanten, Netzwerkpartner/Lohnfertiger)."),

        // ============ MITGELTENDE UNTERLAGEN ============
        h("Mitgeltende Unterlagen", HeadingLevel.HEADING_2),
        p("Verfahrensanweisungen aus weiteren Kernprozessen sowie aus Führungs- und Unterstützungsprozessen, die mit dieser Anweisung an bestimmten Punkten interagieren, insbesondere:"),
        bullet("die Anweisung zum Vorserienprozess (Kernprozess Produktentstehung) – wirkt z. B. bei Neuteilen auf die Aufgaben von Bemusterung, Automatisierung und Werkzeugbau ein"),
        bullet("die Verfahrensanweisung(en) zur Qualitätssicherung (Unterstützungsprozess) – wirkt z. B. bei Freigabeprüfungen, Sperrentscheidungen und Reaktionsplänen bei Prozessabweichungen ein"),

        // ============ 7.5.4 VERFAHREN ============
        h("7.5.4 Verfahren", HeadingLevel.HEADING_2),
        p("Zur Sicherheit der Produktionsabläufe wurden entsprechende Prüf- und Arbeitsanweisungen erstellt. In den Produktionsaufträgen und Produktdatenblättern sind alle Informationen zur Herstellung der Produkte enthalten. Der Ablauf ist im Flow Chart (siehe separate Grafik / Anhang) dargestellt."),

        h("7.5.4.1.1 Grobplanung", HeadingLevel.HEADING_3),
        p("Kundenbestellungen werden vom Verkaufsinnendienst (VKI) geprüft und ins FOSS übergeben. Die Produktionsplanung und -steuerung ermittelt anhand des KPLI-Moduls die aktuellen Bedarfe und lastet die Produktionsaufträge entsprechend Lagerstand und Bedarf ein."),

        h("7.5.4.2 Feinplanung", HeadingLevel.HEADING_3),
        p("Die Feinplanung erfolgt auf Basis der freigegebenen FOSS-Aufträge durch die Produktionsplanung und -steuerung, einschließlich der Personaleinsatzplanung unter Berücksichtigung der Mitarbeiterqualifikationen. Die konkrete Vorgehensweise ist in einer eigenen Anweisung zur Feinplanung geregelt."),

        h("7.5.4.3 Zeitlich begrenzte Änderungen in der Produktionsprozesslenkung", HeadingLevel.HEADING_3),
        p("Änderungen werden generell als interne Projekte geführt und entsprechend den Erfordernissen an die Produktionsplanung und -steuerung mitgeteilt. In den regelmäßig stattfindenden Produktionsbesprechungen werden die Themen besprochen. Im FOSS-Modul ARPL (Arbeitsplanpflege) besteht die Möglichkeit, zeitlich begrenzte Änderungen mit Ablauftermin im Arbeitsplan einzutragen; diese Zusatzanweisungen sind an den Auftragspapieren ersichtlich, bis die Änderung terminlich abgelaufen ist. Temporäre Produktänderungen werden gemäß den Anforderungen der Produkt-/Projekttechnik und von RPP (Robust Production Processes, Team der Qualitätsmanagement-Abteilung) auf Konformität geprüft; es erfolgt eine Rückmeldung an die Produkt-/Projekttechnik über den Status des betreffenden Produktionsauftrags (PA) mittels Eintragung im Schichtlogbuch durch Teamleitung Spritzguss-Produktion/PQB. Ein Prüfmittelwechsel erfolgt generell nicht, da Prüfmittel nur in der benötigten Anzahl angefertigt werden (üblicherweise ein Satz); alle in der Produktion vorhandenen Messmittel haben einen gültigen Prüfstatus. Ein Wechsel des Werkzeuges von der Standardspritzgussmaschine auf die geeignete Ersatzmaschine ist grundsätzlich erlaubt, da in der Prozessentwicklungsphase Vorserie immer eine Ausweichmaschine mitbemustert wird. Derselbe Vorgang gilt, wenn der Standardladungsträger nicht verfügbar ist, mit alternativen Gebinden."),

        h("7.5.4.4 Abwicklung der Produktionsaufträge (exemplarisch für Spritzguss)", HeadingLevel.HEADING_3),
        p("Für die allgemeine Vorbereitung der Spritzgusswerkzeuge ist die Teamleitung Spritzguss-Produktion verantwortlich. Der Einbau der Werkzeuge erfolgt primär durch Einsteller/Rüster. Die Produktionslogistik ist für die rechtzeitige Vorbereitung der Einlegeteile zuständig, der Boxenbauer für die Gebindebereitstellung und interne Transporte von der Produktion ins Lager. Die Teamleitung Lager ist für die rechtzeitige Vorbereitung der Materialien zuständig. Die Teamleitung Spritzguss-Produktion wickelt die Produktion ab, führt die entsprechenden Qualitätskontrollen mittels Prüfbegleitkarte durch und behebt Vorkommnisse."),

        h("7.5.4.5 Abweichungsmanagement im laufenden Betrieb", HeadingLevel.HEADING_3),
        p("Störungen werden, wenn möglich, sogleich behoben. Die QS prüft anschließend, ob Korrekturmaßnahmen notwendig sind, um Wiederholungsfehler zu vermeiden. Laufende Qualitätskontrollen werden vom PQB nach geregelter Häufigkeit lt. Arbeits- und Prüfanweisung durchgeführt und protokolliert. Reklamationen mit externer Relevanz werden über einen 8D-Report bearbeitet: Der Auftrag dazu ergeht vom QMB an den Produktionsleiter, die QS unterstützt bei der Durchführung. Eine geregelte Wartung und Instandhaltung dient als vorbeugende Maßnahme zur Produktionssicherheit. Die Teamleitungen im Hauptprozess sind jeweils für die Qualität der in ihrem Bereich produzierten Teile sowie die Auswertung der Produktionsvorkommnisse verantwortlich und haben bei Bedarf Maßnahmen einzuleiten."),

        h("7.5.4.6 Material", HeadingLevel.HEADING_3),
        p("Alle Anlieferungen werden von der Wareneingangsprüfung (WEP) auf Identität geprüft. Die Produktionsplanung und -steuerung berücksichtigt bei der Einplanung der Produktionsaufträge die erforderliche Durchlaufzeit der Wareneingangsprüfung (WEP), damit freigegebenes Material rechtzeitig für die Produktion sowie die ggf. erforderliche Vortrocknung zur Verfügung steht. Um eine geforderte Vortrocknung von Originalmaterial rechtzeitig einzuleiten, werden die Trocknungsdetails am Arbeitsplan angedruckt (ARPL). Der Aushang erfolgt zuvor an der Plantafel. Restmaterial wird in sauberen, verschlossenen, beschrifteten Behältern/Säcken an das Lager retourniert, gebucht und aufbewahrt."),

        // ============ AUFZEICHNUNGEN ============
        h("Aufzeichnungen", HeadingLevel.HEADING_2),
        p("Im Rahmen dieses Prozesses werden u. a. folgende Aufzeichnungen geführt (Aufbewahrung gemäß der betrieblichen Aufbewahrungsfristenregelung):"),
        bullet("Schichtlogbuch – Schichtübergabe (Status je Maschine, Vorkommnisse, laufende Maßnahmen)"),
        bullet("Prüfbegleitkarte – Qualitätskontrollen/Freigaben (Erststück-/Letztstückfreigabe, erneute Freigabe nach Unterbrechung)"),
        bullet("Einstelldatenblatt – Produktionsparameter (Maschine/Werkzeug/Material)"),
        bullet("Musterbericht – Ergebnis der technischen Bemusterung"),
        bullet("Werkzeugabnahmeprotokoll – Abnahme von Werkzeugen nach Bemusterung"),
        bullet("Objektstammdaten (FOSS) – Anlagen/Betriebsmittel/Vorrichtungen"),
        bullet("8D-Report – strukturierte Problemlösung bei internen Qualitätsabweichungen"),
        bullet("CE-Konformitätsdokumentation (Risikobeurteilung, technische Dokumentation, Konformitätserklärung) – bei durch Automatisierung integrierten Gesamtanlagen"),

        // ============ BEGRIFFE/ABKÜRZUNGEN ============
        h("Begriffe/Abkürzungen", HeadingLevel.HEADING_2),
        bullet("AAW – Arbeitsanweisung"),
        bullet("ARPL – FOSS-Modul zur Pflege von Arbeitsplänen"),
        bullet("Aufgabenliste – Liste, die von Instandhaltung und Werkzeugbau geführt wird; verschiedene Stakeholder tragen dort Anliegen/Störungen ein"),
        bullet("DocuWare – internes Dokumentenmanagementsystem"),
        bullet("FOSS – ERP-System"),
        bullet("HF/FT – Halbfertigteile/Fertigteile"),
        bullet("IKK – Interdisziplinäre Koordinationsrunde Kernprozesse"),
        bullet("Kienformation-Center – digitales Arbeitsplatz-Portal für Fach-/Führungskräfte"),
        bullet("LMS – Lernmanagementsystem"),
        bullet("MES (Authentig) – Manufacturing Execution System"),
        bullet("Poka-Yoke-Verifizierung („Dummy-Prüfung“) – regelmäßige Funktionsprüfung integrierter Prüfanlagen mittels Referenzteilen"),
        bullet("PA – Produktionsauftrag (eine von mehreren Betriebsauftragskategorien)"),
        bullet("PQB – Qualitätsprüfer/in"),
        bullet("Prüfbegleitkarte – Dokument für Qualitätskontrollen/Freigaben"),
        bullet("PT – Produkt-/Projekttechnik"),
        bullet("QMB – Qualitätsmanagementbeauftragte/r; bei Kienbacher wahrgenommen vom Abteilungsleiter der Qualitätsmanagement-Abteilung"),
        bullet("QS – Qualitätssicherung Produktion"),
        bullet("RPP – Robust Production Processes, Team innerhalb der Qualitätsmanagement-Abteilung"),
        bullet("WEP – Wareneingangsprüfung, eigene Organisationseinheit innerhalb der Qualitätsmanagement-Abteilung"),
        bullet("Schichtlogbuch – Dokumentationsmittel für die Schichtübergabe"),
        bullet("SFK – Sicherheitsfachkraft"),
        bullet("SVP – Sicherheitsvertrauensperson"),
        bullet("Teamleiter – Sammelbegriff für die den jeweiligen Abteilungsleitungen unterstellten Führungskräfte im Produktionsumfeld dieses Dokuments; mit Ausnahme der Teamleitung Lager (Abteilungsleiter SCM/Logistik) dem Produktionsleiter unterstellt"),
      ],
    },
  ],
});

Packer.toBuffer(doc).then((buffer) => {
  require("fs").writeFileSync(__dirname + "/../working/7V-5-1_Auftragsabwicklung_Produktion_ENTWURF.docx", buffer);
  console.log("done");
});
