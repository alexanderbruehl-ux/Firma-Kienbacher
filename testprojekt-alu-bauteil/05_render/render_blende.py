"""Fotorealistisches Rendering der Alu-Blende im Schwalbennest (Blender/Cycles, headless via bpy).
    python3 render_blende.py [--hdri PFAD.hdr] [--samples 160] [--res 1600 900] [--shot gesamt|detail]
Eingaben: 04_cad/blende/export/*.stl  (vorher 04_cad/blende/blende_2a.py ausführen)"""
import bpy, bmesh, math, os, sys, argparse
from mathutils import Vector
HERE=os.path.dirname(os.path.abspath(__file__)); EXP=os.path.normpath(os.path.join(HERE,'..','04_cad','blende','export'))
ap=argparse.ArgumentParser(); ap.add_argument('--hdri',default=''); ap.add_argument('--samples',type=int,default=160)
ap.add_argument('--res',type=int,nargs=2,default=[1600,900]); ap.add_argument('--shot',default='gesamt'); ap.add_argument('--out',default=''); ap.add_argument('--blende',default='Blende_2C.stl')
a=ap.parse_args([x for x in sys.argv[1:]])
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene; sc.unit_settings.system='METRIC'
def imp(name):
    bpy.ops.wm.stl_import(filepath=os.path.join(EXP,name),global_scale=0.001)
    o=bpy.context.selected_objects[0]; o.name=name.replace('.stl',''); return o
def mat(name,base,metal=0.0,rough=0.5,coat=0.0,coat_rough=0.03):
    m=bpy.data.materials.new(name); m.use_nodes=True; b=m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value=(*base,1); b.inputs['Metallic'].default_value=metal; b.inputs['Roughness'].default_value=rough
    if coat: b.inputs['Coat Weight'].default_value=coat; b.inputs['Coat Roughness'].default_value=coat_rough
    return m
def smooth(o,angle=30):
    bpy.context.view_layer.objects.active=o; o.select_set(True)
    try: bpy.ops.object.shade_auto_smooth(angle=math.radians(angle))
    except Exception:
        try: bpy.ops.object.shade_smooth_by_angle(angle=math.radians(angle))
        except Exception: pass
    o.select_set(False)
# ---- Objekte ----
bl=imp(a.blende); hull=imp('Szene_Rumpf.stl'); frame=imp('Szene_Einfassung.stl'); pocket=imp('Szene_Fach.stl'); corpus=imp('Szene_Korpus.stl')
alu=mat('Alu_hochglanz',(0.93,0.935,0.94),1.0,0.035)
alu_sat=mat('Alu_satiniert',(0.86,0.87,0.88),1.0,0.32)
steel=mat('Edelstahl_poliert',(0.78,0.78,0.80),1.0,0.05)
gel=mat('Gelcoat_marineblau',(0.004,0.008,0.032),0.0,0.3,coat=1.0,coat_rough=0.015)
black=mat('Korpus_schwarz',(0.012,0.012,0.014),0.0,0.65)
# Teak prozedural (Maserung + dunkle Fugen, Maßstab in Metern)
teak=bpy.data.materials.new('Teak'); teak.use_nodes=True; nt=teak.node_tree; bs=nt.nodes['Principled BSDF']
tc=nt.nodes.new('ShaderNodeTexCoord'); mp=nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value=(4,60,4)
ns=nt.nodes.new('ShaderNodeTexNoise'); ns.inputs['Scale'].default_value=2.0; ns.inputs['Detail'].default_value=8
wv=nt.nodes.new('ShaderNodeTexWave'); wv.wave_type='BANDS'; wv.bands_direction='Y'; wv.inputs['Scale'].default_value=0.6; wv.inputs['Distortion'].default_value=8.0; wv.inputs['Detail'].default_value=6
cr=nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].color=(0.13,0.055,0.02,1); cr.color_ramp.elements[1].color=(0.33,0.15,0.06,1)
nt.links.new(tc.outputs['Object'],mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'],wv.inputs['Vector']); nt.links.new(wv.outputs['Fac'],cr.inputs['Fac']); nt.links.new(cr.outputs['Color'],bs.inputs['Base Color'])
bs.inputs['Roughness'].default_value=0.5
for o,m in ((hull,gel),(frame,steel),(pocket,teak),(corpus,black)): o.data.materials.append(m)
# Blende: Logogrund (z = -0,35 mm, Normale +z) satiniert
bl.data.materials.append(alu); bl.data.materials.append(alu_sat)
bm=bmesh.new(); bm.from_mesh(bl.data); n=0
for f in bm.faces:
    c=f.calc_center_median()
    if f.normal.z>0.99 and abs(c.z+0.00035)<0.00004: f.material_index=1; n+=1
bm.to_mesh(bl.data); bm.free(); print('Logo-Flächen satiniert:',n)
smooth(frame,50)   # Blende bleibt flach schattiert (ebene Flächen, keine Wellen)
bpy.ops.object.empty_add(location=(0,0,0)); root=bpy.context.object; root.name='Szene'
for o in (bl,hull,frame,pocket,corpus): o.parent=root
root.rotation_euler=(math.radians(90),0,0)
# Teakdeck unterhalb des Fachs
bpy.ops.mesh.primitive_plane_add(size=1,location=(0.35,-0.45,-0.20)); deck=bpy.context.object; deck.scale=(1.6,1.0,1)
deck.data.materials.append(teak)
# ---- Welt / Licht ----
w=bpy.data.worlds.new('W'); sc.world=w; w.use_nodes=True; wn=w.node_tree
bg=wn.nodes['Background']
if a.hdri and os.path.exists(a.hdri):
    env=wn.nodes.new('ShaderNodeTexEnvironment'); env.image=bpy.data.images.load(a.hdri)
    mapn=wn.nodes.new('ShaderNodeMapping'); tcw=wn.nodes.new('ShaderNodeTexCoord'); mapn.inputs['Rotation'].default_value=(0,0,math.radians(120))
    wn.links.new(tcw.outputs['Generated'],mapn.inputs['Vector']); wn.links.new(mapn.outputs['Vector'],env.inputs['Vector']); wn.links.new(env.outputs['Color'],bg.inputs['Color'])
    bg.inputs['Strength'].default_value=1.0
else:
    bg.inputs['Color'].default_value=(0.6,0.65,0.7,1); bg.inputs['Strength'].default_value=0.8
# weiche Flächenleuchte für den Glanzreflex auf dem Alu
bpy.ops.object.light_add(type='AREA',location=(0.30,-0.60,0.35)); L=bpy.context.object; L.data.energy=60; L.data.size=0.6; L.data.shape='RECTANGLE'; L.data.size_y=0.15
L.rotation_euler=(math.radians(65),0,0)
# ---- Kamera ----
bpy.ops.object.camera_add(); cam=bpy.context.object; sc.camera=cam
if a.shot=='detail':
    target=Vector((0.29,0.0,0.07)); cam.location=Vector((0.42,-0.26,0.14)); cam.data.lens=85
else:
    target=Vector((0.33,0.0,0.10)); cam.location=Vector((0.86,-0.72,0.46)); cam.data.lens=42
d=target-cam.location; cam.rotation_euler=d.to_track_quat('-Z','Y').to_euler()
cam.data.dof.use_dof=True; cam.data.dof.focus_distance=d.length; cam.data.dof.aperture_fstop=8 if a.shot=='gesamt' else 5.6
# ---- Render ----
sc.render.engine='CYCLES'; sc.cycles.device='CPU'; sc.cycles.samples=a.samples; sc.cycles.use_denoising=True
sc.cycles.max_bounces=8; sc.cycles.glossy_bounces=6
sc.render.resolution_x,sc.render.resolution_y=a.res; sc.render.resolution_percentage=100
sc.view_settings.view_transform='AgX'; sc.view_settings.look='AgX - Medium High Contrast'
sc.render.image_settings.file_format='PNG'
sc.render.filepath=a.out or os.path.join(HERE,f"{a.blende.replace('.stl','')}_{a.shot}.png")
import time; t=time.time(); bpy.ops.render.render(write_still=True); print('Render %.0fs -> %s'%(time.time()-t,sc.render.filepath))
