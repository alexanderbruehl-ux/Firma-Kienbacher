# Testprojekt: KI-Designprozess → produzierbares Aluminium-Bauteil

Ziel: Die Fähigkeiten der KI in technischen und gestalterischen Fragen durchgängig testen.
Aus Referenzprodukten entsteht ein **völlig neues Bauteil** mit individuellem,
hochwertigem und herstellbarem Design. Es wird als 3D-Modell konstruiert, in
**Autodesk Fusion (über MCP am Desktop-PC)** automatisiert aufgebaut und mit Licht-
und Oberflächeneffekten gerendert.

> Getrennt vom QM-Projekt 7V-5-1 im übergeordneten Ordner.

## Ablauf (Phasen)

| # | Phase | Ergebnis | Ordner | Status |
|---|-------|----------|--------|--------|
| 1 | Referenzen sammeln | Produktbilder + was daran gefällt | `01_referenzen/` | 🔶 läuft (R01–R03, U01–U12 Web-Bilder Boot) |
| 2 | Designanalyse | Formensprache, Muster, Oberflächen, Fertigungsbezug | `02_designanalyse/` | 🔶 begonnen |
| 3 | Konzeptvarianten | K1 Leder, K2a–c Alu gefräst (`03_konzepte/KONZEPTE.md`), Logo nachgezeichnet | `03_konzepte/` | 🔶 Entwürfe liegen vor |
| 4 | **Designauswahl** (durch Kienbacher) | gewählte Variante + Änderungswünsche | `03_konzepte/AUSWAHL.md` | ⬜ |
| 5 | Parametrisches 3D-CAD | `parameter.json` → STEP/STL + Vorschau | `04_cad/` | ✅ Werkzeugkette getestet (Platzhalter) |
| 6 | Fusion: Konstruktion + Rendering | `fusion_blende.py` importiert das Blenden-STEP (identisch mit CadQuery), Material, Ansicht; `fusion_build.py` ist nur der Platzhalter-Test | `05_fusion/` | 🔶 Skript geschrieben, ⬜ am Desktop-PC testen |
| 7 | Fertigungsunterlagen | Zeichnung A3 aus den Modelldaten (`zeichnung_blende.py`): Ansicht, Detail Hochtöner, Schnitt Haut, Bohrtabelle | `06_zeichnung/` | 🔶 Entwurf, Bemaßung fehlt |

## Werkzeugkette

```
Referenzbilder ──► Designanalyse ──► Konzeptvarianten ──► Auswahl
                                                            │
                                                  parameter.json  (eine Quelle für alle Maße)
                                               ┌────────────┴────────────┐
                                     04_cad/model.py              05_fusion/fusion_build.py
                                     (CadQuery, Cloud/CI)         (Fusion-API, Desktop via MCP)
                                     STEP · STL · Vorschau        Zeitleiste · Material · Rendering · STEP
                                               └────────────┬────────────┘
                                                   06_zeichnung (Fertigung)
```

- **CadQuery** (Open Source, Python) erzeugt das Referenzmodell ohne Fusion, prüft
  Volumen/Masse und liefert STEP/STL für Abgleich und Muster.
- **Fusion** baut dasselbe Bauteil *nativ* (editierbare Zeitleiste, Benutzerparameter),
  weist Werkstoff und Aussehen zu und rendert es. Details: `05_fusion/ANLEITUNG_FUSION_MCP.md`.
- Fertigungsregeln für Aluminium: `docs/FERTIGUNGSRICHTLINIEN_ALU.md`.

## Befehle

```bash
pip install -r testprojekt-alu-bauteil/requirements.txt
python3 testprojekt-alu-bauteil/04_cad/model.py      # → 04_cad/export/
```

## Aktueller Inhalt von `parameter.json`

Ein neutrales **Platzhalter-Bauteil** (Halteplatte 120×60×12, Tasche, 4 Bohrungen),
nur zum Test der Werkzeugkette. Es wird nach der Designauswahl ersetzt.
