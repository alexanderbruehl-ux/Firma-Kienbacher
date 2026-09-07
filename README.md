# QM-Dokument-Revision: 7V-5-1 „Auftragsabwicklung in der Produktion"

Revision der IATF-16949-Verfahrensanweisung 7V-5-1 (Version k → l), Kienbacher.
Ziel: Anpassung an den gelebten Ist-Zustand, strukturiert nach dem **AKV-Prinzip**
(Aufgaben / Kompetenzen / Verantwortung), ergänzt um Führung / Sicherheit / Umwelt.

## ⚠️ Wichtig für den Einstieg

**Lies zuerst `notes/PROJEKTSTATUS.md`** – dort steht der komplette inhaltliche
Diskussionsstand aus der bisherigen Konversation mit Claude. Ohne diese Datei
fehlt der gesamte Kontext, denn das `working/*.docx` ist nur ein technisches
Rohgerüst und enthält **noch nicht** die im Gespräch erarbeiteten Inhalte.

## Ordnerstruktur

```
source/     Original-PDF, Version k (Ausgangsdokument, unverändert, read-only Referenz)
working/    Aktueller Word-Zwischenstand (.docx) — technisches Rohgerüst, Inhalt noch NICHT aktualisiert
scripts/    build.js – node/docx-js-Skript, mit dem working/*.docx erzeugt wurde
notes/      Diskussionsprotokoll, offene Punkte, Entscheidungen (siehe unten)
```

## Notes-Dateien

- **PROJEKTSTATUS.md** – Gesamtüberblick: Vorgehen, Stand, nächste Schritte
- **PRODUKTIONSLEITER.md** – Detaillierte AKV-Ausarbeitung der Rolle Produktionsleiter (in Bearbeitung)
- **OFFENE_ROLLEN.md** – Neue/umbenannte Rollen, die zusätzlich zu den 11 bestehenden dokumentiert werden müssen
- **BEGRIFFE.md** – Geklärte Abkürzungen/Begriffe (KPLI, IKK, Teamleiter, …)

## Wie weiterarbeiten (Vorschlag für Claude Code)

1. `notes/PROJEKTSTATUS.md` und `notes/PRODUKTIONSLEITER.md` lesen, um den Stand zu übernehmen.
2. Rollen-für-Rolle-Diskussion mit dem Nutzer fortsetzen (Methode: siehe PROJEKTSTATUS.md, Abschnitt „Vorgehen").
3. Erst wenn eine Rolle **vollständig** abgestimmt ist, in `working/*.docx` einarbeiten
   (per unzip/XML-Edit, siehe docx-Skill, oder Neuaufbau über `scripts/build.js`).
4. Nach jeder abgeschlossenen Rolle: `notes/PROJEKTSTATUS.md` aktualisieren (Fortschritt, nächster Punkt).

## Technische Hinweise

- `working/*.docx` wurde mit `scripts/build.js` (Node.js, Paket `docx`) erzeugt.
- Version im Dokument ist als "l (Entwurf)" markiert, mit rotem Entwurfs-Hinweis am Anfang.
- Der ursprüngliche Flow Chart (S. 5 im Original-PDF) wurde noch nicht ins Word-Dokument übernommen
  (nur als Platzhaltertext referenziert) — bei Bedarf nachbauen oder als Grafik einfügen.
