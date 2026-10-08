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
  "Abgeschlossene technische Ausbildung (z. B. Kunststofftechnik, Maschinenbau, Produktionstechnik) — Lehrabschluss mit einschlägiger Weiterbildung oder höher",
  "Fundierte Kenntnisse gängiger Qualitätsmanagement-Methoden und -Werkzeuge (z. B. 8D-Problemlösung, Grenzmusterkataloge, Prüfmittelmanagement, Lenkungsplan/Control Plan)",
  "Sicherer Umgang mit den eingesetzten IT-Systemen (FOSS/ERP, Q-Studio, MES)",
  "Mehrjährige einschlägige Berufserfahrung in der Kunststoff-Spritzguss-Fertigung bzw. in der Qualitätssicherung eines Fertigungsbetriebs",
  "Grundkenntnisse der relevanten Normen (ISO 9001, IATF 16949)",
];

const KOMPETENZEN = [
  "Analytisches, strukturiertes Vorgehen bei der Problemlösung (Ursachenanalyse, Ableitung wirksamer Maßnahmen)",
  "Durchsetzungsvermögen und Kommunikationsstärke gegenüber Produktionsleitung, Teamleitungen und PQB",
  "Fähigkeit zu eigenständigen Entscheidungen unter Zeitdruck (Stopp-Kompetenz)",
  "Vermittlungs- und Schulungskompetenz (Koordination/Anleitung der PQB, Mitarbeiterschulungen)",
  "Durchsetzungsfähigkeit im Sinne des 4-Augen-Prinzips gegenüber der Produktion, bei gleichzeitiger Kooperationsfähigkeit",
  "Selbstständige, eigenverantwortliche Arbeitsweise",
];

const MINDESTANFORDERUNGEN = [
  "Abgeschlossene facheinschlägige Berufsausbildung im technischen Bereich",
  "Einschlägige Berufserfahrung in der Qualitätssicherung oder Produktion eines Fertigungsbetriebs",
  "Grundlegende Kenntnisse im Reklamations-/Problemlösungsmanagement (z. B. 8D)",
  "Gute EDV-Anwenderkenntnisse (ERP-/MES-Systeme)",
  "Kenntnis aller Bauteile (Produktportfolio, Qualitätsanforderungen, typische Fehlerbilder)",
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
        children: [new TextRun({ text: "Stellenbeschreibung: QS (Qualitätssicherung Produktion)", bold: true, font: FONT, size: 28 })],
      }),
      new Paragraph({
        spacing: { after: 200 },
        children: [new TextRun({ text: "Arbeitsentwurf — Basis: konsolidierte Rollenbeschreibung inkl. Ergänzungen von AIDA. Noch nicht Teil der Verfahrensanweisung 7V-5-1.", italics: true, font: FONT, size: 18 })],
      }),

      h("Organisatorische Einordnung"),
      bullet("Organisatorisch der Qualitätsabteilung zugeordnet, bewusst außerhalb der Produktionsabteilung angesiedelt (4-Augen-Prinzip)"),
      bullet("Vertretung des Produktionsleiters im Bereich Qualität (Bereich 3 von 3 der Vertretungsstruktur) bei dessen Abwesenheit"),
      bullet("Organisatorisch übergeordnet zu den schichtbezogen aufgeteilten PQB, koordiniert deren Tätigkeit übergreifend"),

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
  require("fs").writeFileSync(__dirname + "/../working/QS_Stellenbeschreibung_Arbeitsentwurf.docx", buffer);
  console.log("done");
});
