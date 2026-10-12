const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, LevelFormat } = require("docx");
const { GRUNDSAETZLICHES, AUFGABEN, VERANTWORTLICHKEIT } = require("./pqb_data");

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

const QUALIFIKATIONEN = [
  "Grundkenntnisse im Lesen und Anwenden von Prüfplänen, Zeichnungen und Arbeitsanweisungen",
  "Kenntnisse gängiger Prüfmittel/Messmethoden (z. B. Lehren, Messschieber, Sichtprüfung)",
  "Sicherer Umgang mit dem Prüfdaten-System (Q-Studio)",
  "Erfahrung in der Kunststoff-/Spritzguss-Fertigung von Vorteil",
];

const KOMPETENZEN = [
  "Genaues, sorgfältiges Arbeiten und hohe Aufmerksamkeit für Details",
  "Fähigkeit zu eigenständigen Entscheidungen bei Qualitätsabweichungen (Stopp-/Absonderungskompetenz)",
  "Kommunikationsfähigkeit im Austausch mit Teamleitung und Werkern",
  "Vermittlungs-/Schulungskompetenz für Qualitätsschulungen",
  "Belastbarkeit bei Schichtarbeit",
];

const MINDESTANFORDERUNGEN = [
  "Abgeschlossene facheinschlägige Berufsausbildung oder vergleichbare praktische Erfahrung in der Fertigung",
  "Grundkenntnisse der Qualitätsprüfung und Messtechnik",
  "Bereitschaft zur Schichtarbeit",
  "Kenntnis aller Bauteile (Produktportfolio, Qualitätsanforderungen, typische Fehlerbilder)",
];

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
        children: [new TextRun({ text: "Stellenbeschreibung: PQB (Qualitätsprüfer/in)", bold: true, font: FONT, size: 28 })],
      }),
      new Paragraph({
        spacing: { after: 200 },
        children: [new TextRun({ text: "Arbeitsentwurf — Basis: PQB.md. Noch nicht Teil der Verfahrensanweisung 7V-5-1.", italics: true, font: FONT, size: 18 })],
      }),

      h("Organisatorische Einordnung"),
      bullet("Keine Teamleitungsfunktion — eigenständige Fachrolle"),
      bullet("Schichtbezogen aufgeteilt; organisatorisch der QS (Qualitätssicherung Produktion) zugeordnet, die übergreifend koordiniert"),
      bullet("Überwiegend direkt in der Produktion anwesend (fertigungsbegleitende Tätigkeit)"),

      h("Grundsätzliches"),
      ...GRUNDSAETZLICHES.map((t) => bullet(t)),

      h("Aufgaben"),
      ...AUFGABEN.map((t) => bullet(t)),

      h("Verantwortlichkeit (Kompetenz/Entscheidungsbefugnis)"),
      ...VERANTWORTLICHKEIT.map((t) => bullet(t)),

      h("Erforderliche Qualifikationen"),
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
  require("fs").writeFileSync(__dirname + "/../working/PQB_Stellenbeschreibung_Arbeitsentwurf.docx", buffer);
  console.log("done");
});
