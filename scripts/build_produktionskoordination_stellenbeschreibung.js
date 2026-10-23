const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, LevelFormat } = require("docx");
const { GRUNDSAETZLICHES, AUFGABEN, VERANTWORTLICHKEIT } = require("./produktionskoordination_data");

const FONT = "Calibri";

function h(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 280, after: 160 },
    children: [new TextRun({ text, bold: true, font: FONT })],
  });
}

function p(text) {
  return new Paragraph({
    spacing: { after: 120 },
    alignment: AlignmentType.JUSTIFIED,
    children: [new TextRun({ text, font: FONT })],
  });
}

function bullet(text, level = 0) {
  return new Paragraph({
    numbering: { reference: "bullets", level },
    spacing: { after: 80 },
    alignment: AlignmentType.JUSTIFIED,
    children: [new TextRun({ text, font: FONT })],
  });
}

// Entwurf — noch nicht mit Alexander abgestimmt (im Unterschied zu
// GRUNDSAETZLICHES/AUFGABEN/VERANTWORTLICHKEIT, die direkt aus den
// bereits abgestimmten notes/*.md übernommen sind).
const QUALIFIKATIONEN = [
  "Abgeschlossene kaufmännische oder technische Ausbildung mit Bezug zu Personal-/Organisationsthemen (z. B. HR, Betriebswirtschaft, Produktionstechnik mit Personalverantwortung)",
  "Grundkenntnisse im Arbeitsrecht und in der Personalentwicklung",
  "Sicherer Umgang mit den eingesetzten IT-Systemen (Kienformation-Center, Lernmanagementsystem/LMS)",
  "Mehrjährige Erfahrung im Produktionsumfeld bzw. in produktionsnahen Personal-/Organisationsthemen",
];

const KOMPETENZEN = [
  "Kommunikations- und Vermittlungsstärke zwischen Produktion und HR",
  "Konzeptionelles, strukturiertes Arbeiten (Erarbeitung von Schulungsprogrammen, Arbeitszeitmodellen)",
  "Vertrauenswürdigkeit und Diskretion im Umgang mit personenbezogenen Themen",
  "Fähigkeit, bei Abwesenheit des Produktionsleiters selbstständig und entscheidungssicher zu vertreten",
];

const MINDESTANFORDERUNGEN = [
  "Abgeschlossene facheinschlägige Berufsausbildung",
  "Einschlägige Erfahrung in Personal- oder Organisationsthemen in einem Produktionsbetrieb",
  "Gute EDV-Anwenderkenntnisse",
];

const doc = new Document({
  numbering: {
    config: [{
      reference: "bullets",
      levels: [
        { level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } },
      ],
    }],
  },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 } } },
    children: [
      new Paragraph({
        children: [new TextRun({ text: "Stellenbeschreibung: Produktionskoordination (Organisation/Personal)", bold: true, font: FONT, size: 28 })],
      }),
      new Paragraph({
        spacing: { after: 200 },
        children: [new TextRun({
          text: "Arbeitsentwurf — Basis: PRODUKTIONSKOORDINATION.md. Behandelt ausschließlich die Vertretungsfunktion (Organisation/Personal); die separate Funktion als Teamleitung Endfertigung (Personalunion, siehe ENDFERTIGUNG.md) ist bewusst nicht Teil dieser Stellenbeschreibung. Noch nicht Teil der Verfahrensanweisung 7V-5-1.",
          italics: true, font: FONT, size: 18,
        })],
      }),

      h("Organisatorische Einordnung"),
      bullet("Stabsfunktion des Produktionsleiters („Organisationsteam“, Ebene A – Vertretungsfunktionen)"),
      bullet("Vertretung des Produktionsleiters im Bereich Organisation/Personal (Bereich 1 von 3 der Vertretungsstruktur)"),
      bullet("Keine Teamleitungsfunktion im Rahmen dieser Vertretungsfunktion"),

      h("Grundsätzliches"),
      ...GRUNDSAETZLICHES.map((t) => bullet(t)),

      h("Aufgaben"),
      ...AUFGABEN.map((t) => bullet(t)),

      h("Verantwortlichkeit (Kompetenz/Entscheidungsbefugnis)"),
      ...VERANTWORTLICHKEIT.map((t) => bullet(t)),

      h("Erforderliche Qualifikationen"),
      p("Entwurf — noch nicht mit Alexander abgestimmt:"),
      ...QUALIFIKATIONEN.map((t) => bullet(t)),

      h("Erforderliche Kompetenzen"),
      ...KOMPETENZEN.map((t) => bullet(t)),

      h("Mindestanforderungen an die Stelle"),
      p("Die folgenden Punkte stellen das Mindestniveau dar, unterhalb dessen die Stelle nicht ordnungsgemäß ausgeübt werden kann:"),
      ...MINDESTANFORDERUNGEN.map((t) => bullet(t)),
    ],
  }],
});

Packer.toBuffer(doc).then((buffer) => {
  require("fs").writeFileSync(__dirname + "/../working/PRODUKTIONSKOORDINATION_Stellenbeschreibung_Arbeitsentwurf.docx", buffer);
  console.log("done");
});
