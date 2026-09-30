# Renderer für Konzeptvorschauen

```bash
pip install pillow numpy fonttools potracer scikit-image
cd testprojekt-alu-bauteil/03_konzepte/render
python3 konzepte2.py        # aktuelle Vorschau: Vorschau_flach.jpg (+ Vorschau_Montage.jpg)
```

- `konzepte2.py` – aktuelle Vorschau (Variante 1 Leder sattelbraun, Variante 2 Alu hochglanzpoliert mit Lochmustern A/B/C)
- `konzepte.py` – Grundfunktionen (Geometrie, Leder, Logo, Kantennut, Edelstahlleiste) und ältere Konzepte K2a–c
- `render_v7.py` – entzerrtes, aufgehelltes Einbaufoto als Hintergrund (mm-Koordinaten). **Benötigt das Foto aus dem
  privaten Repo** `Privat-Meisterwerke` unter `/home/user/privat-meisterwerke/…/Referenzbilder/03-Schwalbennest.jpeg`.
  Ohne dieses Foto entstehen die flachen Ansichten nicht, weil die Geometrie dort mit definiert ist.
