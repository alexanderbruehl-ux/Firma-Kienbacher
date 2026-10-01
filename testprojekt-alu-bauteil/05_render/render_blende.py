"""Fotorealistisches Rendering der Alu-Blende im Schwalbennest (Blender/Cycles, headless via bpy).
    python3 render_blende.py [--hdri PFAD.hdr] [--samples 160] [--res 1600 900] [--shot gesamt|detail|hochtoener] [--exposure EV]
Eingaben: 04_cad/blende/export/*.stl  (vorher 04_cad/blende/blende_2a.py ausführen)"""
import bpy, bmesh, math, os, sys, argparse
from mathutils import Vector
HERE=os.path.dirname(os.path.abspath(__file__)); EXP=os.path.normpath(os.path.join(HERE,'..','04_cad','blende','export'))
ap=argparse.ArgumentParser(); ap.add_argument('--hdri',default=''); ap.add_argument('--samples',type=int,default=160)
ap.add_argument('--res',type=int,nargs=2,default=[1600,900]); ap.add_argument('--shot',default='gesamt'); ap.add_argument('--out',default=''); ap.add_argument('--blende',default='Blende_2C.stl'); ap.add_argument('--exposure',type=float,default=None)
a=ap.parse_args([x for x in sys.argv[1:]])
CACHE=os.path.join(HERE,'assets'); os.makedirs(CACHE,exist_ok=True)
def asset(name,url):
    p=os.path.join(CACHE,name)
    if not os.path.exists(p):
        import urllib.request; print('lade',url); urllib.request.urlretrieve(url,p)
    return p
PH='https://dl.polyhaven.org/file/ph-assets'
TEAK_COL=asset('teak_veneer_col.jpg',PH+'/Textures/jpg/2k/teak_veneer/teak_veneer_diff_2k.jpg')
TEAK_RGH=asset('teak_veneer_rough.jpg',PH+'/Textures/jpg/2k/teak_veneer/teak_veneer_rough_2k.jpg')
STUDIO=asset('studio_small_09_2k.hdr',PH+'/HDRIs/hdr/2k/studio_small_09_2k.hdr')
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
alu_sat=mat('Alu_satiniert',(0.62,0.63,0.65),1.0,0.48)   # Fräsgrund matt -> Logo lesbar
steel=mat('Edelstahl_poliert',(0.78,0.78,0.80),1.0,0.05)
gel=mat('Gelcoat_marineblau',(0.004,0.008,0.032),0.0,0.3,coat=1.0,coat_rough=0.015)
black=mat('Korpus_schwarz',(0.012,0.012,0.014),0.0,0.65)
# Teak: CC0-Furniertextur (Poly Haven „Teak Veneer“), Box-Projektion in Objektkoordinaten
def teak_mat(name,fugen=False):
    m=bpy.data.materials.new(name); m.use_nodes=True; nt=m.node_tree; bs=nt.nodes['Principled BSDF']
    tc=nt.nodes.new('ShaderNodeTexCoord'); mp=nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value=(2.2,2.2,2.2)
    ic=nt.nodes.new('ShaderNodeTexImage'); ic.image=bpy.data.images.load(TEAK_COL); ic.projection='BOX'; ic.projection_blend=0.2
    ir=nt.nodes.new('ShaderNodeTexImage'); ir.image=bpy.data.images.load(TEAK_RGH); ir.image.colorspace_settings.name='Non-Color'; ir.projection='BOX'
    nt.links.new(tc.outputs['Object'],mp.inputs['Vector'])
    for i in (ic,ir): nt.links.new(mp.outputs['Vector'],i.inputs['Vector'])
    col=ic.outputs['Color']
    if fugen:   # schwarze Fugen alle 45 mm (Teakdeck wie Frauscher)
        wv=nt.nodes.new('ShaderNodeTexWave'); wv.wave_type='BANDS'; wv.bands_direction='Y'; wv.wave_profile='SAW'; wv.inputs['Scale'].default_value=1.0/0.045/ (2*math.pi) * 2*math.pi
        mpw=nt.nodes.new('ShaderNodeMapping'); mpw.inputs['Scale'].default_value=(1,1.0/0.045,1); nt.links.new(tc.outputs['Object'],mpw.inputs['Vector'])
        sep=nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(mpw.outputs['Vector'],sep.inputs['Vector'])
        fr=nt.nodes.new('ShaderNodeMath'); fr.operation='FRACT'; nt.links.new(sep.outputs['Y'],fr.inputs[0])
        st=nt.nodes.new('ShaderNodeMath'); st.operation='LESS_THAN'; st.inputs[1].default_value=0.11; nt.links.new(fr.outputs[0],st.inputs[0])
        mx=nt.nodes.new('ShaderNodeMix'); mx.data_type='RGBA'; mx.inputs['B'].default_value=(0.012,0.010,0.009,1)
        nt.links.new(st.outputs[0],mx.inputs['Factor']); nt.links.new(col,mx.inputs['A']); col=mx.outputs['Result']
    nt.links.new(col,bs.inputs['Base Color']); nt.links.new(ir.outputs['Color'],bs.inputs['Roughness'])
    return m
teak=teak_mat('Teak'); teak_deck=teak_mat('Teakdeck',fugen=True)
for o,m in ((hull,gel),(frame,steel),(pocket,teak),(corpus,black)): o.data.materials.append(m)
# Blende: Logogrund (z = -0,5 mm, Normale +z) satiniert
bl.data.materials.append(alu); bl.data.materials.append(alu_sat)
bm=bmesh.new(); bm.from_mesh(bl.data); n=0
for f in bm.faces:
    c=f.calc_center_median()
    if f.normal.z>0.99 and (abs(c.z+0.0005)<0.00003 or abs(c.z+0.5)<0.03): f.material_index=1; n+=1   # Logogrund z = -0,5 mm
bm.to_mesh(bl.data); bm.free(); print('Logo-Flächen satiniert:',n)
smooth(frame,50)   # Blende bleibt flach schattiert (ebene Flächen, keine Wellen)
bpy.ops.object.empty_add(location=(0,0,0)); root=bpy.context.object; root.name='Szene'
for o in (bl,hull,frame,pocket,corpus): o.parent=root
root.rotation_euler=(math.radians(90),0,0)
# Teakdeck unterhalb des Fachs
bpy.ops.mesh.primitive_plane_add(size=1,location=(0.35,-0.45,-0.20)); deck=bpy.context.object; deck.scale=(1.6,1.0,1)
deck.data.materials.append(teak_deck)
# ---- Welt / Licht ----
w=bpy.data.worlds.new('W'); sc.world=w; w.use_nodes=True; wn=w.node_tree
bg=wn.nodes['Background']
if a.hdri and os.path.exists(a.hdri):
    env=wn.nodes.new('ShaderNodeTexEnvironment'); env.image=bpy.data.images.load(a.hdri)
    mapn=wn.nodes.new('ShaderNodeMapping'); tcw=wn.nodes.new('ShaderNodeTexCoord'); mapn.inputs['Rotation'].default_value=(0,0,math.radians(120))
    wn.links.new(tcw.outputs['Generated'],mapn.inputs['Vector']); wn.links.new(mapn.outputs['Vector'],env.inputs['Vector']); wn.links.new(env.outputs['Color'],bg.inputs['Color'])
    bg.inputs['Strength'].default_value=1.0
else:
    sky=wn.nodes.new('ShaderNodeTexSky')
    for t in ('MULTIPLE_SCATTERING','NISHITA','SINGLE_SCATTERING'):
        try: sky.sky_type=t; break
        except Exception: pass
    print('Sky:',sky.sky_type)
    sky.sun_elevation=math.radians(28); sky.sun_rotation=math.radians(215)
    try: sky.altitude=5
    except Exception: pass
    wn.links.new(sky.outputs['Color'],bg.inputs['Color']); bg.inputs['Strength'].default_value=0.35
    # Spiegelstrahlen sehen ein neutrales Studio (kein rosé/bronze Farbstich auf Hochglanz-Alu und Edelstahl)
    out=wn.nodes['World Output']; lp=wn.nodes.new('ShaderNodeLightPath')
    st=wn.nodes.new('ShaderNodeTexEnvironment'); st.image=bpy.data.images.load(STUDIO)
    bg2=wn.nodes.new('ShaderNodeBackground'); bg2.inputs['Strength'].default_value=0.30
    wn.links.new(st.outputs['Color'],bg2.inputs['Color'])
    mixs=wn.nodes.new('ShaderNodeMixShader')
    wn.links.new(lp.outputs['Is Glossy Ray'],mixs.inputs['Fac']); wn.links.new(bg.outputs['Background'],mixs.inputs[1]); wn.links.new(bg2.outputs['Background'],mixs.inputs[2])
    wn.links.new(mixs.outputs['Shader'],out.inputs['Surface'])
    try: sky.sun_intensity=0.25
    except Exception: pass
# weiche Flächenleuchte für den Glanzreflex auf dem Alu
bpy.ops.object.light_add(type='AREA',location=(0.30,-0.60,0.35)); L=bpy.context.object; L.data.energy=60; L.data.size=0.6; L.data.shape='RECTANGLE'; L.data.size_y=0.15
L.rotation_euler=(math.radians(65),0,0)
# ---- Kamera ----
bpy.ops.object.camera_add(); cam=bpy.context.object; sc.camera=cam
if a.shot=='hochtoener':   # Hochtöner-Feld (CAD 376,4/151,0) mit ausgefrästem Signet-M
    target=Vector((0.3764,0.0,0.151)); cam.location=Vector((0.44,-0.22,0.20)); cam.data.lens=100
elif a.shot=='detail':
    target=Vector((0.29,0.0,0.07)); cam.location=Vector((0.42,-0.26,0.14)); cam.data.lens=85
else:
    target=Vector((0.33,0.0,0.10)); cam.location=Vector((0.86,-0.72,0.46)); cam.data.lens=42
d=target-cam.location; cam.rotation_euler=d.to_track_quat('-Z','Y').to_euler()
cam.data.dof.use_dof=True; cam.data.dof.focus_distance=d.length; cam.data.dof.aperture_fstop={'gesamt':8,'hochtoener':11}.get(a.shot,5.6)
# ---- Render ----
sc.render.engine='CYCLES'; sc.cycles.device='CPU'; sc.cycles.samples=a.samples; sc.cycles.use_denoising=True
sc.cycles.max_bounces=8; sc.cycles.glossy_bounces=6
sc.render.resolution_x,sc.render.resolution_y=a.res; sc.render.resolution_percentage=100
sc.view_settings.view_transform='AgX'; sc.view_settings.look='AgX - Medium High Contrast'
sc.render.image_settings.file_format='PNG'
# ohne HDRI: physikalischer Himmel + Sonne, dafür Belichtung -2 (dunkelblaues Gelcoat, Teak, Hochglanz-Alu)
sc.view_settings.exposure=a.exposure if a.exposure is not None else (0.0 if a.hdri and os.path.exists(a.hdri) else -2.0)
sc.render.filepath=a.out or os.path.join(HERE,f"{a.blende.replace('.stl','')}_{a.shot}.png")
import time; t=time.time(); bpy.ops.render.render(write_still=True); print('Render %.0fs -> %s'%(time.time()-t,sc.render.filepath))
