const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, LevelFormat } = require("docx");
const { GRUNDSAETZLICHES, AUFGABEN, VERANTWORTLICHKEIT } = require("./qs_data");

const FONT = "Calibri";

function h(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 280, after: 160 },
    children: [new TextRun({ text, bold: true, font: FONT })],
  });
}

function bullet(text) {
  return new Paragraph({
    numbering: { reference: "bullets", level: 0 },
    spacing: { after: 100 },
    children: [new TextRun({ text, font: FONT })],
  });
}

function blank() {
  return new Paragraph({
    spacing: { after: 300 },
    border: { bottom: { style: "single", size: 2, color: "AAAAAA" } },
    children: [new TextRun({ text: " ", font: FONT })],
  });
}

const doc = new Document({
  numbering: {
    config: [{
      reference: "bullets",
      levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } } }],
    }],
  },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 } } },
    children: [
      new Paragraph({
        children: [new TextRun({ text: "QS (Qualitätssicherung Produktion) — Rollenbeschreibung", bold: true, font: FONT, size: 28 })],
      }),
      new Paragraph({
        spacing: { after: 100 },
        children: [new TextRun({ text: "Arbeitsentwurf zum Ausdrucken — Review/Ergänzung gemeinsam mit AIDA", italics: true, font: FONT, size: 20 })],
      }),
      new Paragraph({
        spacing: { after: 200 },
        children: [new TextRun({ text: "Noch nicht Teil der Verfahrensanweisung 7V-5-1 — Basis für die Konsolidierung der QS-Rollenbeschreibung.", italics: true, font: FONT, size: 18 })],
      }),

      h("Grundsätzliches"),
      ...GRUNDSAETZLICHES.map(bullet),

      h("Aufgaben"),
      ...AUFGABEN.map(bullet),

      h("Verantwortlichkeit (Kompetenz/Entscheidungsbefugnis)"),
      ...VERANTWORTLICHKEIT.map(bullet),

      h("Ergänzungen / Anmerkungen von AIDA"),
      blank(), blank(), blank(), blank(), blank(), blank(), blank(), blank(),
    ],
  }],
});

Packer.toBuffer(doc).then((buffer) => {
  require("fs").writeFileSync(__dirname + "/../working/QS_Rollenbeschreibung_Arbeitsentwurf.docx", buffer);
  console.log("done");
});
