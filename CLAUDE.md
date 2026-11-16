# Firma Kienbacher — QM-Projekt 7V-5-1

**Kanonischer Arbeits-Branch: `claude/modest-euler-g7v1lp`**

Dieses Repo wird für mehrere, voneinander unabhängige Aufgaben genutzt. Für
das Projekt „QM-Dokumente überarbeiten" (Revision der Verfahrensanweisung
7V-5-1 Auftragsabwicklung in der Produktion; Ordner `notes/`, `scripts/`,
`working/`, `source/`) gilt:

- **Projektname** (z. B. für Fenstertitel wie bei der Dateivorschau):
  „QM-Dokumente überarbeiten" — nicht der Dokumenttitel „7V-5-1
  Auftragsabwicklung in der Produktion" und nicht der Repo-Name.

- Der einzige gültige, aktuelle Stand liegt auf Branch
  `claude/modest-euler-g7v1lp`. Bitte **IMMER zuerst**
  `git fetch origin claude/modest-euler-g7v1lp` ausführen und
  `notes/PROJEKTSTATUS.md` auf diesem Branch lesen, bevor irgendetwas an
  diesem Projekt bearbeitet wird.
- Falls diese Session auf einem anderen/neuen Branch gestartet wurde:
  **nicht unabhängig weiterarbeiten.** Stattdessen den obigen Branch
  auschecken/fortsetzen bzw. den Nutzer fragen, ob ein Merge nötig ist.
- Der bei GitHub hinterlegte Standard-Branch des Repos kann
  veraltet/falsch sein (historisch bedingt) — er ist **nicht**
  maßgeblich. Maßgeblich ist ausschließlich der oben genannte Branch.
- Alte Branches in diesem Repo (z. B. `claude/elegant-volta-*`,
  `claude/jolly-ride-*`, `claude/restore-deleted-project-*`,
  `claude/sub-agenten-definition-*`, `claude/zip-to-github-projects-*`)
  gehören zu anderen, abgeschlossenen oder überholten Aufgaben und
  sollten für dieses QM-Projekt nicht als Grundlage verwendet werden.

## Grundregel: Alles gehört ins Repo

Alles, was in einer Session für Alexander Brühl erarbeitet oder geändert
wird (Dokumente, Präsentationen, PDFs, Notizen, Skripte), wird **grundsätzlich
in dieses Repo committet und gepusht**, und zwar ungefragt und zeitnah nach jeder
sinnvollen Änderung. Nur so kann sowohl online (Cloud-Sessions, Handy) als
auch lokal am PC am selben Stand weitergearbeitet werden. Dateien, die nur
im Chat, in einem Artifact oder im Scratchpad liegen, gelten als nicht
gesichert. Ist eine Session ohne verbundenes Repo gestartet, wird dieses Repo
als Erstes eingebunden.

Jedes Projekt bekommt einen eigenen Ordner auf dem kanonischen Branch
`claude/modest-euler-g7v1lp`, keinen eigenen Branch:

- QM-Dokumente überarbeiten (7V-5-1): `notes/`, `scripts/`, `working/`, `source/`
- Visualisierung letzter Arbeitstag 2026: `letzter-arbeitstag/` (Stand und
  offene Punkte in `letzter-arbeitstag/README.md`)

## Grundregel: Microsoft 365 nur lesen (Planner, Teams, Outlook)

In **Planner, Teams und Outlook wird ohne ausdrückliche Zustimmung von
Alexander nichts verändert** — keine Aufgaben anlegen/ändern/abhaken,
keine Kommentare, keine Nachrichten oder Antworten posten, keine Mails
senden/entwerfen/verschieben/löschen, keine Termine anlegen/ändern/
zusagen.

**Lesen ist immer erlaubt, ohne Rückfrage** — Mails, Kalender, Teams-
Kanäle/Chats, Planner-Aufgaben, SharePoint/OneDrive, auch über den
Browser (z. B. Planner-Aufgabe öffnen und lesen), wenn der Connector
etwas nicht liefert.

Diese Regel gilt **immer**, auch wenn eine Session, ein Branch oder eine
Einstellung auf automatische Freigabe („Auto"/„Automatically approve")
steht. Die Zustimmung muss im Chat für die konkrete Änderung gegeben
werden; eine frühere Zustimmung gilt nicht für spätere Änderungen.

## Projektübergreifendes Prinzip

Die allgemeine Regel gegen unbemerktes Auseinanderdriften von Branches/
Sessions (für alle Projekte von Alexander Brühl, nicht nur dieses) liegt
nicht hier, sondern account-weit im Skill `project-continuity-check`
(im Profil gespeichert) sowie zusammengefasst in diesem Artifact:
https://claude.ai/artifact/46iz8v6ydL9jgAeh5GhFpE

Ebenso projektübergreifend (nicht nur dieses Projekt betreffend): der
Standard, jede für Menschen relevante Dateilieferung (DOCX/PPTX/XLSX/PDF/
Bilder — nicht Code) zusätzlich als Artifact-Vorschau sichtbar zu machen,
liegt account-weit im Skill `dateivorschau` (im Profil gespeichert) sowie
zusammengefasst in diesem Artifact:
https://claude.ai/artifact/RD8VYYvhiiyKhmiFys8sSH
