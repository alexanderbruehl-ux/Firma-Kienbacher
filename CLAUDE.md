# Firma Kienbacher — QM-Projekt 7V-5-1

**Kanonischer Arbeits-Branch: `claude/modest-euler-g7v1lp`**

Dieses Repo wird für mehrere, voneinander unabhängige Aufgaben genutzt. Für
das Projekt „Revision der Verfahrensanweisung 7V-5-1 Auftragsabwicklung in
der Produktion" (Ordner `notes/`, `scripts/`, `working/`) gilt:

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

## Allgemeines Prinzip (gilt projektübergreifend für Alexander Brühl)

Dieses Repo ist ein Beispiel für ein wiederkehrendes Problem: Wird eine
neue Claude-Code-Session gestartet, ohne eine bestehende Session
fortzusetzen, entsteht ein neuer, unabhängiger Branch — ohne Bezug zum
zuletzt bearbeiteten Stand. Das führt zu doppelter/parallel verlaufender
Arbeit (siehe `claude/restore-deleted-project-06650i`).

**Für jedes neue Projekt/Repo von Alexander Brühl gilt die gleiche Regel:**
Bevor an einem neuen oder unklaren Projekt gearbeitet wird, soll Claude
von sich aus prüfen, ob es bereits ähnliche/verwandte Repos, Branches
oder Sessions gibt (z. B. über `list_repos`, `git branch -a`,
`list_sessions`), und den Nutzer proaktiv darauf hinweisen, statt
stillschweigend einen neuen, isolierten Stand zu beginnen. Ein
entsprechender Skill-Hinweis ("Dedup-Check bei Projektstart") ist unter
`.claude/skills/` in diesem Repo hinterlegt und sollte bei Bedarf in
andere Projekte von Alexander übertragen werden.
