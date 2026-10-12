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
        text: "ENTWURF – Inhalt abgeleitet aus notes/OFFENE_ROLLEN.md, noch nicht im Detail mit Alexander abgestimmt.",
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

function note(text) {
  return new Paragraph({
    spacing: { after: 160 },
    children: [new TextRun({ text, italics: true, font: FONT, size: 20, color: "5C6169" })],
  });
}

function bullet(text) {
  return new Paragraph({
    numbering: { reference: "bullets", level: 0 },
    spacing: { after: 60 },
    children: [new TextRun({ text, font: FONT, size: 22 })],
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
        title("Stellenbeschreibung"),
        subtitle("QS – Qualitätssicherung Produktion"),
        draftBanner(),

        fieldLine("Unternehmen", "Kienbacher"),
        fieldLine("Zugehöriges QM-Dokument", "7V-5-1 Auftragsabwicklung in der Produktion (Referenz, Kap. 7.5.3)"),
        fieldLine("Status", "Entwurf – Rolle identifiziert, Inhalt noch nicht final abgestimmt"),

        h("Einordnung"),
        note("Organisatorische Stellung der Rolle, wie bisher in der Diskussion festgelegt (siehe notes/OFFENE_ROLLEN.md und notes/PROJEKTSTATUS.md)."),
        bullet("Vertretung des Produktionsleiters im Bereich Qualität (1 von 3 Vertretungsbereichen: Organisation/Personal, Technik, Qualität)"),
        bullet("Bewusst außerhalb der Produktionsabteilung angesiedelt – 4-Augen-Prinzip zwischen Produktions- und Qualitätsseite"),
        bullet("Organisatorisch übergeordnet gegenüber den PQB (Qualitätsprüfer/in, Rolle 7.5.3.9 in 7V-5-1), welche schichtbezogen aufgeteilt sind"),

        h("Verantwortung"),
        bullet("Vertretung des Produktionsleiters im Bereich Qualität"),
        bullet("Organisatorisch übergeordnet gegenüber den PQB"),

        h("Aufgaben"),
        bullet("Korrespondenzfunktion zur Produktionsleitung auf Gesamtebene (analog: QMB ↔ Schichtführer/Teamleiter auf Schicht-/Team-Ebene)"),
        bullet("Vertretung des Produktionsleiters in allen qualitätsrelevanten Fragen: fehlerhafte Teile im Haus, Reklamationen, Sperren, Nacharbeit, Maschinen abstellen/stoppen"),
        bullet("Feststellen von Korrekturmaßnahmenbedarf und Meldung an die Produktionsleitung"),
        bullet("Prüfung und Freigabe nach Wirksamkeitsnachweis (z.B.: Entsperren von Teilen/Prozessen), nachdem die Produktionsleitung die konkrete Maßnahme festgelegt hat"),

        h("Kompetenzen"),
        bullet("Entscheidungsbefugnis über Freigabe/Entsperren von Teilen und Prozessen nach Wirksamkeitsprüfung"),
        bullet("Koordinierende Befugnis gegenüber den PQB (schichtübergreifend)"),

        h("Ablauf Korrekturmaßnahmen (Zusammenspiel mit Produktionsleitung)"),
        bullet("1. QS stellt fest, dass Korrekturmaßnahmen erforderlich sind"),
        bullet("2. Produktionsleitung entscheidet, was konkret gemacht wird"),
        bullet("3. QS prüft das Ergebnis und gibt bei Erfüllung der Anforderungen frei (z.B.: Entsperren von Teilen/Prozessen)"),

        h("Qualifikation"),
        note("Platzhalter – Ausbildung, Berufserfahrung, fachliche Qualifikation noch mit Alexander abzustimmen."),

        h("Mindestanforderungen"),
        note("Platzhalter – Mindestvoraussetzungen (z. B. Kenntnisse, Zertifikate, Erfahrung) noch mit Alexander abzustimmen."),

        h("Noch offen / zu klären"),
        bullet("Qualifikation und Mindestanforderungen (siehe oben), Berichtslinie (disziplinarisch), Stellvertretung der Rolle selbst"),
        bullet("Finale Abstimmung mit Alexander zu allen obigen Punkten"),
      ],
    },
  ],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(__dirname + "/../stellenbeschreibungen/Stellenbeschreibung_QS_ENTWURF.docx", buf);
  console.log("written stellenbeschreibungen/Stellenbeschreibung_QS_ENTWURF.docx");
});
