const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, LevelFormat } = require("docx");

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

const AUFGABEN = [
  "Sperren, Beurteilung, Pflege von Grenzmusterkatalogen, Erststückfreigaben (Systematik/Grundlagen) sowie interne Maßnahmen zur Verbesserung/Vermeidung von Reklamationen",
  "Beratung des Produktionsleiters bei strukturierter Problemlösung (8D) bei internen Qualitätsabweichungen",
  "Beurteilung der vom Produktionsleiter gesetzten Sofort-/Korrekturmaßnahmen; gemeinsame Prüfung der Wirksamkeit",
  "Entscheidung, ob und wie fehlerhafte Teile nachgearbeitet/repariert werden dürfen, inkl. erneuter Prüfung danach",
  "Durchführung/Koordination interner Prozess- und Produktaudits (über die laufende PQB-Prüfung hinaus)",
  "Überwachung, ob bei Prozessabweichungen die im Lenkungsplan festgelegten Reaktionspläne eingehalten werden",
  "Übergreifende Koordination/Steuerung der Tätigkeit der schichtbezogen aufgeteilten PQB",
  "Unterstützung des Produktionsleiters bei 8D-Reports zu Reklamationen mit externer Relevanz (Auftrag kommt vom QMB)",
  "Gemeinsame Definition von Vermeidungs-/Abstellmaßnahmen mit der Teamleitung bei Kundenreklamationen-Sofortmaßnahmen",
  "Prüfung nach Störungsbehebung, ob Korrekturmaßnahmen notwendig sind, um Wiederholungsfehler zu vermeiden",
  "Mitwirkung als Fachabteilung bei Unterweisungen (neben HR, SVP, SFK)",
  "Einbindung bei multidisziplinären, automatisierungsbedingten Prozessänderungen",
  "Kontrolle, Unterstützung und Einschulung neuen Personals (Qualitätsthemen)",
  "Kontrolle aller laufenden Aufträge: Teile- und Maschinenzustand, Ausschussquote, korrekte Ausschuss-Trennung direkt an der Maschine, korrekte Buchungen, ordnungsgemäße Auftragsvorbereitung (Erststück, Rückstellmuster, vollständig ausgefüllte Dokumente, gekennzeichnete Ausschussbehälter)",
];

const VERANTWORTLICHKEIT = [
  "Vertretung des Produktionsleiters in allen qualitätsrelevanten Fragen (Bereich 3 von 3 der Vertretungsstruktur)",
  "Befugnis, Produktion/Versand zu stoppen, um Qualitätsprobleme zu korrigieren",
  "Fachliche Weisungsbefugnis gegenüber dem Produktionsleiter in Q-Themen (spätestens über den QMB durchsetzbar)",
  "Organisatorisch übergeordnet zu den PQB",
  "Freigabe-/Entscheidungsbefugnis bei Korrekturmaßnahmen (gibt nach Wirksamkeitsprüfung frei, z. B. Entsperren von Teilen/Prozessen)",
  "Verantwortlich dafür, dass bei Prozessabweichungen die Reaktionspläne aus dem Lenkungsplan eingehalten werden",
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
