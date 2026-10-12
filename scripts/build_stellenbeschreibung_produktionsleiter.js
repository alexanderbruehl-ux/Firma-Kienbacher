const {
  Document, Packer, Paragraph, TextRun, HeadingLevel,
  AlignmentType, LevelFormat,
} = require("docx");
const fs = require("fs");

const FONT = "Calibri";

function title(text) {
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 100 },
    children: [new TextRun({ text, bold: true, font: FONT, size: 30 })],
  });
}

function subtitle(text) {
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 200 },
    children: [new TextRun({ text, font: FONT, size: 20, color: "5C6169" })],
  });
}

function draftBanner() {
  return new Paragraph({
    spacing: { before: 100, after: 300 },
    border: { top: { style: "single", size: 4, color: "CC0000" }, bottom: { style: "single", size: 4, color: "CC0000" } },
    children: [
      new TextRun({
        text: "ENTWURF – Themenblöcke 1–5 inhaltlich mit Alexander abgestimmt; restliche Punkte aus Version k noch in Diskussion.",
        italics: true, color: "CC0000", font: FONT, size: 18,
      }),
    ],
  });
}

function fieldLine(label, value) {
  return new Paragraph({
    spacing: { after: 60 },
    children: [
      new TextRun({ text: `${label}: `, bold: true, font: FONT, size: 20 }),
      new TextRun({ text: value, font: FONT, size: 20 }),
    ],
  });
}

function h(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 280, after: 120 },
    children: [new TextRun({ text, bold: true, font: FONT })],
  });
}

function h3(text, openItem = false) {
  return new Paragraph({
    spacing: { before: 220, after: 60 },
    children: [new TextRun({ text, bold: true, italics: true, font: FONT, size: 21, color: openItem ? "8A6D00" : undefined })],
  });
}

function bullet(text) {
  return new Paragraph({
    numbering: { reference: "bullets", level: 0 },
    spacing: { after: 60 },
    children: [new TextRun({ text, font: FONT, size: 22 })],
  });
}

const verantwortung = [
  "Wirtschaftlicher Einsatz von Personal und Ressourcen",
  "Personalverantwortung für die Mitarbeiter der Produktion inkl. Werkzeugbau und Instandhaltung",
  "Einhaltung aller relevanten Gesetze, insbesondere des Arbeitszeitgesetzes und des ArbeitnehmerInnenschutzgesetzes (ASchG)",
  "Disziplinarische Verantwortung bei WerkerInnen und Sachbearbeitern als Eskalationsstufe (Erstverantwortung liegt bei den jeweiligen Teamleitern, sofern im Organigramm zugeordnet)",
];

const aufgaben = [
  "Teilnahme an der Kapazitäts- und Planungsabstimmung Produktion/Logistik (aktuell: wöchentliches Meeting KPLI)",
  "Kontrolle/Prüfung der von der Rolle „Produktionsplanung“ erstellten Pläne",
  "Mitwirkung bei der Umsetzung kurzfristiger, ungeplanter Kapazitätsmaßnahmen (z.B.: Einsatz alternativer Anlagen, zusätzliche Schichten)",
  "Weiterentwicklung der Planungsmethodik und der eingesetzten Systeme",
  "Leitung der IKK (Interdisziplinäre Koordinationsrunde Kernprozesse) mit den Bereichen Produktion, Logistik, Produkt-/Projekttechnik, Business Development und Qualitätsmanagement: Top-Down Vorbereitung auf anstehende externe Themen (z.B.: Audits, neue Kundenprojekte/Werkzeuge, TISAX-Einführung); Bottom-Up Ableitung verallgemeinerter, systemischer Maßnahmen aus aktuellen operativen Problemen (Reklamationen, Werkzeug-/Ablaufschwierigkeiten, Ausschuss); Fokus auf den Kernprozess der Leistungserbringung inkl. vorgelagertem Vorserienprozess",
  "Sicherstellung des wirtschaftlichen Einsatzes von Personal und Ressourcen (laufende Steuerung/Überwachung im operativen Betrieb)",
  "Personalanforderung",
  "Führung von Mitarbeitergesprächen",
  "Bildungsbedarfsermittlung",
  "Sicherstellung der produktionsrelevanten Schulungen",
  "Mitwirkung an der Einführung geeigneter (flexibler) Arbeitszeitmodelle (gemeinsam mit HR)",
  "Sicherstellung der Urlaubsplanung",
  "Entscheidung über Art und Umsetzung von Korrekturmaßnahmen bei durch QS festgestelltem Handlungsbedarf (gesamtheitliche Ebene)",
];

const kompetenzen = [
  "Freigabe-/Entscheidungsbefugnis über die Produktionsplanung (Kontrollfunktion gegenüber der Rolle Produktionsplanung)",
  "Entscheidungsbefugnis bei ungeplanten Kapazitätskonflikten (z.B.: Freigabe alternativer Anlagen, Anordnung zusätzlicher Schichten)",
  "Entscheidungsbefugnis über die aus der IKK abgeleiteten Maßnahmen",
  "Entscheidung über Einstellung/Kündigung",
  "Disziplinarische Maßnahmen bei WerkerInnen/Sachbearbeitern (als Eskalationsinstanz – Teamleiter sind primär zuständig, wo zugeordnet)",
  "Entscheidungsbefugnis über die konkrete Maßnahmenwahl bei Korrekturmaßnahmen",
];

const offen = [
  "Organisation / Überwachung der Wartung und Instandhaltung",
  "Prüfung der Produktionsaufzeichnungen",
  "In Zusammenarbeit mit QMB Maßnahmen nach Reklamationen durchführen",
  "Verantwortlich für die Lehrlingsausbildung",
  "Sperren von fehlerhaften Produkten",
  "Bemusterungs Nachbesprechung mit Technik",
  "Werkzeugoptimierungen in Absprache mit PT",
  "Optimieren der technischen Produktprozessentwicklung",
  "Schulungsplanung der Schichtführer u. Einsteller",
];

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
        title("Stellenbeschreibung"),
        subtitle("Produktionsleiter"),
        draftBanner(),

        fieldLine("Unternehmen", "Kienbacher"),
        fieldLine("Zugehöriges QM-Dokument", "7V-5-1 Auftragsabwicklung in der Produktion (Referenz, Kap. 7.5.3.1)"),
        fieldLine("Status", "In Bearbeitung – Themenblöcke 1–5 abgestimmt, weitere Punkte in Diskussion"),

        h("Verantwortung"),
        ...verantwortung.map(bullet),

        h("Aufgaben"),
        ...aufgaben.map(bullet),

        h("Kompetenzen"),
        ...kompetenzen.map(bullet),

        h3("Noch offen – Diskussion ausständig (Version k, unverändert)", true),
        ...offen.map(bullet),
      ],
    },
  ],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(__dirname + "/../stellenbeschreibungen/Stellenbeschreibung_Produktionsleiter_ENTWURF.docx", buf);
  console.log("written stellenbeschreibungen/Stellenbeschreibung_Produktionsleiter_ENTWURF.docx");
});
