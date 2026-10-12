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
        text: "Inhalt unverändert 1:1 aus working/7V-5-1_*.docx (Abschnitt 7.5.3.9) übernommen.",
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

function bullet(text) {
  return new Paragraph({
    numbering: { reference: "bullets", level: 0 },
    spacing: { after: 60 },
    children: [new TextRun({ text, font: FONT, size: 22 })],
  });
}

const aufgaben = [
  "Durchführung von fertigungsbegleitenden Qualitätsprüfungen",
  "Dokumentieren der Prüf- und Messergebnisse in Q Studio",
  "Erfassen von festgestellten Fehlern",
  "Mitarbeit bei der Reklamationsbearbeitung",
  "Durchführung von Qualitätsschulungen",
  "Sperren von fehlerhaften Teilen",
  "Maßnahmenverfolgung bei Prozessänderungen",
  "Erststück / Letztstückfreigabe",
  "Erneute Freigabe nach Produktionsunterbrechung",
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
        subtitle("Qualitätsprüfer/in (PQB)"),
        draftBanner(),

        fieldLine("Unternehmen", "Kienbacher"),
        fieldLine("Zugehöriges QM-Dokument", "7V-5-1 Auftragsabwicklung in der Produktion (Referenz, Kap. 7.5.3.9)"),
        fieldLine("Status", "Inhalt aus Version k übernommen, AKV-Sortierung noch ausständig"),

        h("Aufgaben"),
        ...aufgaben.map(bullet),
      ],
    },
  ],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(__dirname + "/../stellenbeschreibungen/Stellenbeschreibung_PQB_ENTWURF.docx", buf);
  console.log("written stellenbeschreibungen/Stellenbeschreibung_PQB_ENTWURF.docx");
});
