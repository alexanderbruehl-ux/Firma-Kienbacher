"""Autodesk Fusion – automatisierte Konstruktion + Aussehen + Rendering.

Liest ../parameter.json (dieselbe Datei wie 04_cad/model.py), damit Fusion-Modell
und CadQuery-Modell identisch sind.

Ausführen am Desktop-PC:
  a) über das Fusion-MCP (Claude lässt dieses Skript in Fusion laufen), oder
  b) manuell: Fusion > Dienstprogramme > Add-Ins > Skripte und Zusatzmodule > "+" >
     Ordner 05_fusion wählen > fusion_build ausführen.

Ergebnis: neues Design mit Benutzerparametern (Zeitleiste bleibt editierbar),
Material + Aussehen gesetzt, Rendering als PNG in 05_fusion/render/.

HINWEIS: Die Render-API (design.renderManager) ist relativ neu. Die Aufrufe sind
in try/except gekapselt; schlägt das Cloud-/Lokal-Rendering fehl, wird als
Rückfallebene ein Ansichtsfenster-Screenshot gespeichert. Beim ersten Lauf am
Desktop-PC prüfen und bei Bedarf an die installierte Fusion-Version anpassen.
"""
import json
import os
import traceback

import adsk.core
import adsk.fusion

HERE = os.path.dirname(os.path.abspath(__file__))
PARAMS = os.path.join(HERE, "..", "parameter.json")
RENDER_DIR = os.path.join(HERE, "render")


def mm(v):
    return adsk.core.ValueInput.createByString(f"{v} mm")


def expr(s):
    return adsk.core.ValueInput.createByString(s)


def add_user_params(design, g):
    """Alle Maße als Fusion-Benutzerparameter – später in Fusion änderbar."""
    up = design.userParameters
    for key, val in g.items():
        existing = up.itemByName(key)
        if existing:
            existing.expression = f"{val} mm"
        else:
            up.add(key, mm(val), "mm", key)


def p3(x, y, z=0.0):
    # Fusion-API rechnet intern in cm
    return adsk.core.Point3D.create(x / 10.0, y / 10.0, z / 10.0)


def build(design, g):
    root = design.rootComponent
    feats = root.features

    # 1) Grundkörper
    sk = root.sketches.add(root.xYConstructionPlane)
    sk.name = "Grundkontur"
    L, B = g["laenge"], g["breite"]
    sk.sketchCurves.sketchLines.addCenterPointRectangle(p3(0, 0), p3(L / 2, B / 2))
    ext = feats.extrudeFeatures.addSimple(
        sk.profiles.item(0), expr("dicke"),
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    body = ext.bodies.item(0)
    body.name = "Bauteil"

    # 2) Eckradien (senkrechte Kanten)
    vert_edges = adsk.core.ObjectCollection.create()
    for e in body.edges:
        geo = e.geometry
        if isinstance(geo, adsk.core.Line3D):
            s, t = geo.startPoint, geo.endPoint
            if abs(s.x - t.x) < 1e-6 and abs(s.y - t.y) < 1e-6:
                vert_edges.add(e)
    fillet(feats, vert_edges, "eckradius")

    # 3) Tasche von oben
    top = max(body.faces, key=lambda f: f.centroid.z)
    sk2 = root.sketches.add(top)
    sk2.name = "Tasche"
    # Skizze auf Fläche: Koordinaten im Skizzensystem – über Modellpunkte setzen
    c0 = sk2.modelToSketchSpace(p3(0, 0, g["dicke"]))
    c1 = sk2.modelToSketchSpace(p3(g["tasche_laenge"] / 2, g["tasche_breite"] / 2, g["dicke"]))
    sk2.sketchCurves.sketchLines.addCenterPointRectangle(c0, c1)
    prof = min(sk2.profiles, key=lambda pr: pr.areaProperties().area)
    cut = feats.extrudeFeatures.addSimple(
        prof, expr("-tasche_tiefe"), adsk.fusion.FeatureOperations.CutFeatureOperation)
    pocket_edges = adsk.core.ObjectCollection.create()
    for f in cut.sideFaces:
        for e in f.edges:
            geo = e.geometry
            if isinstance(geo, adsk.core.Line3D) and abs(geo.startPoint.x - geo.endPoint.x) < 1e-6 \
                    and abs(geo.startPoint.y - geo.endPoint.y) < 1e-6:
                pocket_edges.add(e)
    fillet(feats, pocket_edges, "tasche_radius")

    # 4) Durchgangsbohrungen
    sk3 = root.sketches.add(root.xYConstructionPlane)
    sk3.name = "Bohrungen"
    ax, ay = g["bohrung_abstand_x"] / 2, g["bohrung_abstand_y"] / 2
    for sx in (-1, 1):
        for sy in (-1, 1):
            sk3.sketchCurves.sketchCircles.addByCenterRadius(p3(sx * ax, sy * ay), g["bohrung_d"] / 20.0)
    holes = adsk.core.ObjectCollection.create()
    for pr in sk3.profiles:
        if pr.profileLoops.count == 1 and pr.areaProperties().area < 1.0:
            holes.add(pr)
    ext_in = feats.extrudeFeatures.createInput(holes, adsk.fusion.FeatureOperations.CutFeatureOperation)
    ext_in.setAllExtent(adsk.fusion.ExtentDirections.PositiveExtentDirection)
    feats.extrudeFeatures.add(ext_in)

    # 5) Kantenfase an Außenkontur oben/unten
    ch_edges = adsk.core.ObjectCollection.create()
    zmax = max(f.centroid.z for f in body.faces)
    zmin = min(f.centroid.z for f in body.faces)
    for f in body.faces:
        if abs(f.centroid.z - zmax) < 1e-6 or abs(f.centroid.z - zmin) < 1e-6:
            for loop in f.loops:
                if loop.isOuter:
                    for e in loop.edges:
                        ch_edges.add(e)
    ch_in = feats.chamferFeatures.createInput2()
    ch_in.chamferEdgeSets.addEqualDistanceChamferEdgeSet(ch_edges, expr("kantenfase"), True)
    feats.chamferFeatures.add(ch_in)
    return body


def fillet(feats, edges, param):
    if edges.count == 0:
        return
    fi = feats.filletFeatures.createInput()
    try:
        fi.edgeSetInputs.addConstantRadiusEdgeSet(edges, expr(param), True)
    except AttributeError:  # ältere API
        fi.addConstantRadiusEdgeSet(edges, expr(param), True)
    feats.filletFeatures.add(fi)


def apply_material(app, design, body, p):
    """Physikalisches Material (Masse) + Render-Aussehen (Oberfläche)."""
    def find(libs, kind, name):
        for i in range(libs.count):
            lib = libs.item(i)
            coll = lib.materials if kind == "mat" else lib.appearances
            item = coll.itemByName(name)
            if item:
                return item
        return None

    mat = find(app.materialLibraries, "mat", p["werkstoff"]["fusion_material"])
    if mat:
        body.material = mat
    r = p["rendering"]
    appear = (find(app.materialLibraries, "app", r["fusion_appearance"])
              or find(app.materialLibraries, "app", r["fusion_appearance_fallback"]))
    if appear:
        local = design.appearances.itemByName(appear.name) or design.appearances.addByCopy(appear, appear.name)
        body.appearance = local
    return mat, appear


def render(app, design, p):
    os.makedirs(RENDER_DIR, exist_ok=True)
    w, h = p["rendering"]["aufloesung_px"]
    out = os.path.join(RENDER_DIR, f"{p['bauteil']['name']}_render.png")

    vp = app.activeViewport
    cam = vp.camera
    cam.viewOrientation = adsk.core.ViewOrientations.IsoTopRightViewOrientation
    cam.isFitView = True
    vp.camera = cam

    try:
        rm = design.renderManager
        # Szene: Umgebung / Boden-Reflexion (Namen je nach Fusion-Version)
        try:
            scene = rm.sceneSettings
            scene.isGroundReflectionsEnabled = True
            scene.isGroundShadowEnabled = True
        except Exception:
            pass
        try:
            env_name = p["rendering"]["umgebung"]
            envs = rm.renderEnvironments if hasattr(rm, "renderEnvironments") else None
            if envs:
                for i in range(envs.count):
                    if envs.item(i).name == env_name:
                        rm.renderEnvironment = envs.item(i)
        except Exception:
            pass
        future = rm.rendering.startLocalRender(out, vp.camera, w, h)
        return out, "Rendering gestartet (läuft im Hintergrund)", future
    except Exception:
        vp.saveAsImageFile(out, w, h)
        return out, "Rückfallebene: Ansichtsfenster-Screenshot (Render-API nicht verfügbar)", None


def run(context):
    app = adsk.core.Application.get()
    ui = app.userInterface
    try:
        with open(PARAMS, encoding="utf-8") as fh:
            p = json.load(fh)
        doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = adsk.fusion.Design.cast(app.activeProduct)
        design.designType = adsk.fusion.DesignTypes.ParametricDesignType
        add_user_params(design, p["geometrie"])
        body = build(design, p["geometrie"])
        body.name = p["bauteil"]["name"]
        mat, appear = apply_material(app, design, body, p)
        out, status, _ = render(app, design, p)

        # Export für Fertigung / Abgleich mit CadQuery
        exp_dir = os.path.join(HERE, "export")
        os.makedirs(exp_dir, exist_ok=True)
        em = design.exportManager
        em.execute(em.createSTEPExportOptions(os.path.join(exp_dir, p["bauteil"]["name"] + "_fusion.step")))

        props = body.physicalProperties
        ui.messageBox(
            f"Bauteil: {body.name}\n"
            f"Material: {mat.name if mat else 'NICHT gefunden'}\n"
            f"Aussehen: {appear.name if appear else 'NICHT gefunden'}\n"
            f"Masse: {props.mass * 1000:.1f} g\n"
            f"{status}\n{out}")
    except Exception:
        ui.messageBox("Fehler:\n" + traceback.format_exc())
