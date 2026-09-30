# Meisterwerke-Logo – VORLÄUFIG

**Status:** vorläufige Nachzeichnung, nur für Positionierung und Designentwürfe.
Wird ersetzt, sobald die **Original-Vektordatei** vorliegt (dann nur `mw_trace.json` bzw. die SVGs tauschen,
`mwlogo.py` bleibt die Schnittstelle für die Renderer).

| Datei | Inhalt |
|---|---|
| `Meisterwerke_Logo.svg` | Signet + Wortmarke |
| `Meisterwerke_Signet.svg` / `Meisterwerke_Wortmarke.svg` | Einzelteile |
| `mw_trace.json` | Vektorpfade (Einheit: Pixel der Vorlage 1024 × 266) |
| `mwlogo.py` | Laden/Zeichnen (Position, Breite, Drehung) für die Konzept-Renderer |
| `trace_logo.py` | Vektorisierung aus der Bilddatei (Potrace), Vorlage liegt im privaten Repo |
| `Logo_hell.png`, `Logo_dunkel.png` | Vorschau |

Entstehung: aus der Bilddatei „LOGO MW.jpg“ (privates Repo Privat-Meisterwerke) vektorisiert, keine
Fremdschrift. Signet als Polygon aus der Kontur, Wortmarke mit Potrace als Bézierkurven.

Position auf der Blende (Stand 30.09.2026): parallel zur Unterkante (3,7°), Mitte 15 mm rechts der
100er-Mitte, Logounterkante 8 mm über der Blendenunterkante, Breite 115 mm (Höhe ≈ 27,9 mm).
