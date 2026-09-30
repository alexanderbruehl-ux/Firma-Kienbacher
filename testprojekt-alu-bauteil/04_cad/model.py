"""Parametrisches CAD-Modell (CadQuery) – liest ../parameter.json.

Erzeugt in 04_cad/export/:
  <name>.step   – Austauschformat für Fusion / Fertigung
  <name>.stl    – Netz für Vorschau / 3D-Druck-Muster
  <name>_iso.png, <name>_ansichten.svg – schnelle Vorschau (kein Rendering)

Aufruf:  python3 testprojekt-alu-bauteil/04_cad/model.py
"""
import json
from pathlib import Path

import cadquery as cq

ROOT = Path(__file__).resolve().parent.parent
EXPORT = Path(__file__).resolve().parent / "export"


def load_params():
    return json.loads((ROOT / "parameter.json").read_text(encoding="utf-8"))


def build(p):
    g = p["geometrie"]
    body = (
        cq.Workplane("XY")
        .rect(g["laenge"], g["breite"])
        .extrude(g["dicke"])
        .edges("|Z").fillet(g["eckradius"])
    )
    # Umlaufende Kantenfase an der Außenkontur oben/unten
    body = body.faces(">Z or <Z").edges().chamfer(g["kantenfase"])
    # Tasche von oben, Eckradius = Fräserradius
    tasche = (
        cq.Workplane("XY").workplane(offset=g["dicke"] - g["tasche_tiefe"])
        .rect(g["tasche_laenge"], g["tasche_breite"])
        .extrude(g["tasche_tiefe"])
        .edges("|Z").fillet(g["tasche_radius"])
    )
    body = body.cut(tasche)
    # Durchgangsbohrungen
    body = (
        body.faces("<Z").workplane()
        .rect(g["bohrung_abstand_x"], g["bohrung_abstand_y"], forConstruction=True)
        .vertices().hole(g["bohrung_d"])
    )
    return body


def export(body, p):
    EXPORT.mkdir(parents=True, exist_ok=True)
    name = p["bauteil"]["name"]
    cq.exporters.export(body, str(EXPORT / f"{name}.step"))
    cq.exporters.export(body, str(EXPORT / f"{name}.stl"), tolerance=0.05, angularTolerance=0.1)
    cq.exporters.export(
        body, str(EXPORT / f"{name}_ansichten.svg"),
        opt={"projectionDir": (1, -1, 0.8), "showHidden": False, "width": 800, "height": 500},
    )
    vol_cm3 = body.val().Volume() / 1000.0
    masse_g = vol_cm3 * p["werkstoff"]["dichte_g_cm3"]
    print(f"Volumen {vol_cm3:.2f} cm³  |  Masse {masse_g:.1f} g ({p['werkstoff']['bezeichnung']})")
    return EXPORT / f"{name}.stl"


def preview_png(stl_path, out_path):
    """Schattierte Schnellvorschau aus dem STL (ersetzt KEIN Fusion-Rendering)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    from stl import mesh

    m = mesh.Mesh.from_file(str(stl_path))
    light = np.array([0.4, -0.5, 0.8]); light /= np.linalg.norm(light)
    v = m.vectors
    n = np.cross(v[:, 1] - v[:, 0], v[:, 2] - v[:, 0])
    n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
    shade = 0.30 + 0.70 * np.abs(n @ light)
    colors = np.c_[np.outer(shade, [0.78, 0.80, 0.83]), np.ones(len(shade))]

    fig = plt.figure(figsize=(8, 5), dpi=150)
    ax = fig.add_subplot(projection="3d")
    ax.add_collection3d(Poly3DCollection(m.vectors, facecolors=colors, edgecolor="none"))
    pts = m.vectors.reshape(-1, 3)
    mid, span = pts.mean(0), (pts.max(0) - pts.min(0)).max() / 2
    for set_lim, c in zip((ax.set_xlim, ax.set_ylim, ax.set_zlim), mid):
        set_lim(c - span * 0.7, c + span * 0.7)
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=28, azim=-55)
    ax.set_axis_off()
    fig.savefig(out_path, bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    params = load_params()
    part = build(params)
    stl = export(part, params)
    preview_png(stl, EXPORT / f"{params['bauteil']['name']}_iso.png")
    print(f"Exporte in {EXPORT}")
