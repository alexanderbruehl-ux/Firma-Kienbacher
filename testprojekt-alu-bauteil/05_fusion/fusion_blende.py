"""Autodesk Fusion: Alu-Blende Schwalbennest 2A-35 aus dem CadQuery-Modell übernehmen, Werkstoff/Aussehen setzen, Ansicht + Rendering.

Das Bauteil (1443 Bohrungen, gestufte Haut 2,2/2,85/3,5 mm mit 45°-Flanken und R2,5, Hochtöner-Feld mit 101 Bohrungen) wird NICHT in der Fusion-API
nachgebaut, sondern als STEP importiert: so ist das Fusion-Modell mit 04_cad/blende/blende_2a35.py identisch. Änderungen an der Geometrie
immer dort machen (python3 blende_2a35.py) und dieses Skript neu ausführen.

Ausführen am Desktop-PC (UNGETESTET, kein Fusion in der Entwicklungsumgebung):
  a) über das Fusion-MCP, oder
  b) Fusion > Dienstprogramme > Add-Ins > Skripte > "+" > Ordner 05_fusion > fusion_blende ausführen.
Voraussetzung: 04_cad/blende/export/Blende_2A35M.step vorhanden (liegt im Repository)."""
import os, traceback
import adsk.core, adsk.fusion

HERE = os.path.dirname(os.path.abspath(__file__))
STEP = os.path.normpath(os.path.join(HERE, "..", "04_cad", "blende", "export", "Blende_2A35M.step"))
RENDER_DIR = os.path.join(HERE, "render")
MATERIAL = "Aluminum 6061"          # Fusion hat EN AW-6082 nicht; Dichte 2,70 g/cm³ identisch, Masse im Modell ca. 1107 g
APPEARANCES = ("Aluminum - Polished", "Aluminum - Satin")


def find(libs, kind, name):
    for i in range(libs.count):
        coll = libs.item(i).materials if kind == "mat" else libs.item(i).appearances
        item = coll.itemByName(name)
        if item:
            return item
    return None


def run(context):
    app = adsk.core.Application.get(); ui = app.userInterface
    try:
        doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = adsk.fusion.Design.cast(app.activeProduct)
        root = design.rootComponent
        im = app.importManager
        opts = im.createSTEPImportOptions(STEP)
        opts.isViewFit = True
        im.importToTarget(opts, root)
        body = root.bRepBodies.item(0) if root.bRepBodies.count else root.occurrences.item(0).bRepBodies.item(0)
        body.name = "Blende_2A35M"
        mat = find(app.materialLibraries, "mat", MATERIAL)
        if mat:
            body.material = mat
        appear = None
        for n in APPEARANCES:
            appear = find(app.materialLibraries, "app", n)
            if appear:
                break
        if appear:
            local = design.appearances.itemByName(appear.name) or design.appearances.addByCopy(appear, appear.name)
            body.appearance = local
        os.makedirs(RENDER_DIR, exist_ok=True)
        vp = app.activeViewport
        cam = vp.camera; cam.viewOrientation = adsk.core.ViewOrientations.FrontViewOrientation; cam.isFitView = True; vp.camera = cam
        out = os.path.join(RENDER_DIR, "Blende_2A35M_ansicht.png"); vp.saveAsImageFile(out, 1920, 1080)
        props = body.physicalProperties
        ui.messageBox(f"Blende 2A-35 importiert\nMaterial: {mat.name if mat else 'NICHT gefunden'}\nAussehen: {appear.name if appear else 'NICHT gefunden'}\n"
                      f"Volumen: {props.volume:.1f} cm³ (Soll 410,1)\nMasse: {props.mass * 1000:.0f} g (Soll 1107)\n{out}")
    except Exception:
        ui.messageBox("Fehler:\n" + traceback.format_exc())
