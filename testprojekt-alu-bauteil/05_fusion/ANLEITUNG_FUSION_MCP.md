# Autodesk Fusion am Desktop-PC (über MCP)

## Voraussetzungen

1. Autodesk Fusion installiert und angemeldet (Windows oder macOS).
2. Fusion-MCP-Server bzw. -Add-In installiert und in Claude Desktop / Claude Code
   am selben PC eingetragen (Einrichtung laut Anleitung des MCP-Anbieters).
3. Dieses Repository am Desktop-PC geklont (`git pull` für den aktuellen Stand).

## Ablauf

1. `parameter.json` enthält die Maße der gewählten Designvariante.
2. Claude führt über das MCP `05_fusion/fusion_build.py` in Fusion aus (alternativ
   manuell: *Dienstprogramme → Add-Ins → Skripte und Zusatzmodule → „+“ → Ordner
   `05_fusion`*).
3. Das Skript
   - legt ein neues **parametrisches Design** an. Alle Maße werden als
     **Benutzerparameter** angelegt und bleiben in *Ändern → Parameter ändern* editierbar.
   - konstruiert das Bauteil nativ: Skizzen, Extrusion, Rundung, Tasche,
     Bohrungen, Fase.
   - weist den **Werkstoff** (Masse) und das **Aussehen** (Eloxal matt) zu.
   - rendert das Bauteil nach `05_fusion/render/*.png`.
   - exportiert `05_fusion/export/*_fusion.step` zum Abgleich mit `04_cad`.
4. Feinschliff des Renderings interaktiv oder per MCP: Umgebung (*Photo Booth*,
   *Plaza* …), Belichtung, Boden-Reflexion, Tiefenschärfe, Kamerawinkel.
   Für mehrere Oberflächen (z. B. matte Fläche + Glanzfacette) jeder Fläche
   ein eigenes Aussehen zuweisen.

## Beim ersten Lauf prüfen

- Die Namen der Aussehen und Materialien (`parameter.json → rendering`) hängen von
  der Sprache und Version der Fusion-Bibliothek ab. Bei „NICHT gefunden“ im
  Meldungsfenster den passenden Namen aus der Bibliothek eintragen.
- Die Render-API (`design.renderManager`) ist neu. Wenn sie fehlt, speichert das
  Skript stattdessen einen Screenshot des Ansichtsfensters (steht im Meldungsfenster).
- Masse in Fusion mit der Ausgabe von `04_cad/model.py` vergleichen
  (Platzhalter: ≈ 201 g).
