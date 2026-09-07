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

function bullet(text) {
  return new Paragraph({
    numbering: { reference: "bullets", level: 0 },
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

// Footer/header info table used at top of each "page section" like the original
function infoTable(seite) {
  return new Table({
    width: { size: 9638, type: WidthType.DXA },
    columnWidths: [1600, 1200, 1400, 2400, 2600, 838],
    rows: [
      new TableRow({
        children: [
          "Dok. Nr.", "Version", "Datum", "erstellt", "geprüft u. freigegeben", "Seite",
        ].map((t) =>
          new TableCell({
            width: { size: 1600, type: WidthType.DXA },
            shading: { type: ShadingType.CLEAR, fill: "F2F2F2" },
            children: [new Paragraph({ children: [new TextRun({ text: t, bold: true, font: FONT, size: 16 })] })],
          })
        ),
      }),
      new TableRow({
        children: [
          "7V- 5-1", "l (Entwurf)", new Date().toLocaleDateString("de-DE"),
          "QMB / Karl Heinz Sixtl", "PL / Herbert Gutbrunner (ausstehend)", seite,
        ].map((t) =>
          new TableCell({
            width: { size: 1600, type: WidthType.DXA },
            children: [new Paragraph({ children: [new TextRun({ text: String(t), font: FONT, size: 16 })] })],
          })
        ),
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

        roleHeading("7.5.3.1 Aufgaben des Produktionsleiters"),
        bullet("Auftragsbesprechung mit LVK, Verwaltung der Produktionsplanung"),
        bullet("Produktionsbesprechung mit Abteilungsleitern"),
        bullet("Wirtschaftlicher Einsatz von Personal und Ressourcen"),
        bullet("Personalplanung"),
        bullet("Verantwortlich der jeweilig unterstellten Mitarbeiter"),
        bullet("Einleiten von Korrekturmaßnahmen in Absprache mit QMB"),
        bullet("Organisation / Überwachung der Wartung und Instandhaltung"),
        bullet("Prüfung der Produktionsaufzeichnungen"),
        bullet("In Zusammenarbeit mit QMB Maßnahmen nach Reklamationen durchführen"),
        bullet("Verantwortlich für die Lehrlingsausbildung"),
        bullet("Sperren von fehlerhaften Produkten"),
        bullet("Bemusterungs Nachbesprechung mit Technik"),
        bullet("Werkzeugoptimierungen in Absprache mit PT"),
        bullet("Optimieren der technischen Produktprozessentwicklung"),
        bullet("Schulungsplanung der Schichtführer u Einsteller"),

        roleHeading("7.5.3.2 Aufgaben der Schichtführer"),
        bullet("Überwachen der Produktionsmaschinen und richtige Materialförderung"),
        bullet("Umbau und Einstellung der Produktionsmaschinen und Produktionsfreigabe"),
        bullet("Sicherstellen der produzierten Qualität und Quantität"),
        bullet("Fehlerbewertung bei Fehlermeldung, Sperren von fehlerhaften Produkten"),
        bullet("Anweisung an den Lagerarbeiter / Produktionslogistiker zum Transport der gesperrten Ware ins gesperrte Lager"),
        bullet("Verantwortlich der jeweilig unterstellten Werker einschl. Sicherheit, Ordnung und Sauberkeit"),
        bullet("Durchführen der vereinbarten Produktions- u. Qualitätsaufzeichnungen"),
        bullet("Werkzeug Wartungstätigkeiten durchführen"),
        bullet("Ausgespritztes Material in Restmüllgebinde und vorgeschriebene Container"),
        bullet("Erststück / Letztstückfreigabe in Zusammenarbeit mit dem PQB lt. Prüfbegleitkarte"),
        bullet("Erneute Freigabe nach geplanten / ungeplanten Produktionsunterbrechungen >30 min lt. Prüfbegleitkarte"),

        roleHeading("7.5.3.3 Aufgaben des Maschinenpersonals (Werker)"),
        bullet("Eigenverantwortliches Beurteilen der produzierten Teile lt. AAW"),
        bullet("Fehlermeldung bei niO Teilen an SF/PQB"),
        bullet("Beachten von zus. Q-Hinweisen z.B.: temp. AAW"),
        bullet("Teile entgraten oder montieren (lt. Anweisung)"),
        bullet("Teile verpacken, etikettieren lt. Verpackungsvorschrift"),
        bullet("Mitwirkung Erststück / Letztstückfreigabe"),

        roleHeading("7.5.3.4 Aufgaben Fertigung Montage"),
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

        roleHeading("7.5.3.8 Aufgaben Arbeitsvorbereitung"),
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

        roleHeading("7.5.3.10 Aufgaben Lager (Materialvorbereitung)"),
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
        p("Störungen werden, wenn möglich, sogleich behoben. Vom QMB / PL wird dann geprüft, ob Korrekturmaßnahmen notwendig sind, um Wiederholungsfehler zu vermeiden. Laufende Qualitätskontrollen werden vom PQB nach geregelter Häufigkeit lt. Arbeits- und Prüfanweisung durchgeführt und protokolliert. Interne Reklamationen werden über den Reklamationsbericht dokumentiert; der interne Reklamationskoordinator führt die Maßnahmenverfolgung nach dem 8D-Verfahren durch. Eine geregelte Wartung u. Instandhaltung (siehe Wartungslisten) dient als vorbeugende Maßnahme zur Produktionssicherheit (6A-32-1). Der Teamleader ist für die Auslieferqualität, für die Auswertung der Produktionsvorkommnisse bzw. Schichtberichte (Todo-Liste, OneNote Prüfbegleitkarte) verantwortlich u. hat bei Bedarf Maßnahmen einzuleiten."),

        h("7.5.4.6 Material", HeadingLevel.HEADING_3),
        p("Alle Anlieferungen werden im WEP ident geprüft. Die Produktionsplanung erfolgt rechtzeitig. Um eine geforderte Vortrocknung von Originalmaterial rechtzeitig einzuleiten, werden die Trocknungsdetails am Arbeitsplan angedruckt (ARPL). Der Aushang erfolgt zuvor an der Plantafel. Restmaterial wird in sauberen, verschlossenen, beschrifteten Behältern / Säcken an das Lager retourniert, gebucht und aufbewahrt."),
      ],
    },
  ],
});

Packer.toBuffer(doc).then((buffer) => {
  require("fs").writeFileSync("/home/claude/qm_doc/7V-5-1_Auftragsabwicklung_Produktion_ENTWURF.docx", buffer);
  console.log("done");
});
