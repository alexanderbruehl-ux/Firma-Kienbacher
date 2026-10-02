"""DXF des Logos (mit vergrößertem Signet) an der Abdeckung + 100er-Kreis als Bezugsgeometrie, zum Einfügen in Autodesk Fusion.
    pip install ezdxf shapely matplotlib
    python3 logo_dxf.py          ->  dxf/Logo_Abdeckung_100er.dxf, dxf/Logo_Abdeckung_100er_Vorschau.png
Koordinatensystem wie im CAD-Modell (blende_2a35.py / parameter.json): Einheit mm, Blendenvorderseite z=0, Lage und Drehung des Logos wie auf der
Blende (Breite 115 mm, parallel zur Unterkante, Unterkante Schrift 8 mm über der Blendenunterkante, Mittelachse durch den 100er-Mittelpunkt).
Layer: LOGO (Signet + Schriftzug, geschlossene Polylinien, Innenkonturen von R/&/... als eigene Polylinien), REF_100ER_KREIS (Kreis Ø118,2) und
REF_100ER_MITTE (Mittelpunkt als Kreuz). Nur Logo und Bezug, keine Blendenkontur."""
import json, math, os, sys, numpy as np, ezdxf
from shapely.geometry import Polygon
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.normpath(os.path.join(HERE,'..','..'))
sys.path.insert(0,os.path.join(ROOT,'03_konzepte','logo')); import mwlogo
P=json.load(open(os.path.join(ROOT,'parameter.json')))
ausschn=P['einbauschnittstelle']['ausschnitte']; c100=[a for a in ausschn if abs(a['d']-118.2)<0.5][0]; T0=np.array(c100['mitte'],float); D100=c100['d']
LOGO_W=105.0; LOGO_ANG=math.degrees(math.atan2(25.4,391.6)); LOGO_EDGE=8.0                       # wie blende_2a35.py
a=math.radians(LOGO_ANG); H=LOGO_W/mwlogo.ASPECT; n=np.array([math.sin(a),-math.cos(a)]); dT=np.dot(T0,-n); C=T0+(dT-(LOGO_EDGE+H/2))*n
polys=[]; mwlogo.draw(lambda p:polys.append(p), lambda ps:polys.extend(ps), lambda p:(float(p[0]),float(p[1])), C[0],C[1],LOGO_W,None,angle_deg=LOGO_ANG)
polys=[np.array(p,float) for p in polys if len(p)>=3]
simp=[]
for p in polys:                                                                                    # Punktzahl reduzieren: Toleranz 0,003 mm (Kontur bleibt unverändert)
    s=Polygon(p).simplify(0.003,preserve_topology=True); simp.append(np.array(s.exterior.coords)[:-1])
doc=ezdxf.new('R2010',setup=True); doc.units=ezdxf.units.MM; msp=doc.modelspace()
doc.layers.add('LOGO',color=7); doc.layers.add('REF_100ER_KREIS',color=1); doc.layers.add('REF_100ER_MITTE',color=1)
for p in simp: msp.add_lwpolyline([tuple(map(float,q)) for q in p],close=True,dxfattribs={'layer':'LOGO'})
msp.add_circle(tuple(T0),D100/2,dxfattribs={'layer':'REF_100ER_KREIS'})
for dx,dy in ((10,0),(0,10)): msp.add_line((T0[0]-dx,T0[1]-dy),(T0[0]+dx,T0[1]+dy),dxfattribs={'layer':'REF_100ER_MITTE'})
out=os.path.join(HERE,'dxf','Logo_Abdeckung_100er.dxf'); doc.saveas(out)
# --- Kontrolle: Datei neu einlesen ---
d2=ezdxf.readfile(out); ents=list(d2.modelspace()); from ezdxf import bbox
lg=bbox.extents([e for e in ents if e.dxf.layer=='LOGO'])
print('DXF geschrieben:',out,'| Objekte:',len(ents),'(Polylinien %d, Kreis 1, Linien 2)'%len(polys),'| Scheitelpunkte gesamt %d (vorher %d)'%(sum(len(p) for p in simp),sum(len(p) for p in polys)))
print('Logo-Ausdehnung x %.2f..%.2f, y %.2f..%.2f mm (Breite %.2f, Höhe %.2f) | Logo-Mitte (%.1f | %.1f) mm | 100er-Kreis Mitte (%.1f | %.1f) Ø%.1f'%(lg.extmin.x,lg.extmax.x,lg.extmin.y,lg.extmax.y,lg.size.x,lg.size.y,C[0],C[1],T0[0],T0[1],D100))
# kleinster Abstand Logo -> Kreis
from shapely.geometry import Point
ring=Point(*T0).buffer(D100/2).exterior; dmin=min(ring.distance(Polygon(p)) for p in simp); print('kleinster Abstand Logo -> Rand 100er-Kreis: %.2f mm'%dmin)
# --- Vorschau ---
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch, Circle
BL=np.array(P['blende_vorgaben']['kontur_foto_angepasst']['ecken'])
fig,ax=plt.subplots(figsize=(16,9)); ax.add_patch(plt.Polygon(BL,fill=False,ec='#bbbbbb',lw=1,ls='--'))
v=[];c=[]
for p in simp: v+=list(map(tuple,p))+[tuple(p[0])]; c+=[Path.MOVETO]+[Path.LINETO]*(len(p)-1)+[Path.CLOSEPOLY]
ax.add_patch(PathPatch(Path(v,c),fc='#1b2a4a',ec='none')); ax.add_patch(Circle(tuple(T0),D100/2,fill=False,ec='#d62728',lw=1.6))
ax.plot([T0[0]-10,T0[0]+10],[T0[1],T0[1]],color='#d62728',lw=1); ax.plot([T0[0],T0[0]],[T0[1]-10,T0[1]+10],color='#d62728',lw=1)
ax.set_aspect('equal'); ax.set_xlim(150,430); ax.set_ylim(-5,200); ax.grid(alpha=.25); ax.set_title('Logo_Abdeckung_100er.dxf – Logo (dunkel), 100er-Kreis Ø118,2 (rot), Blendenkontur nur zur Orientierung (grau, nicht in der DXF)',fontsize=11)
ax.set_xlabel('x [mm] (CAD-Koordinaten)'); ax.set_ylabel('y [mm]'); fig.savefig(os.path.join(HERE,'dxf','Logo_Abdeckung_100er_Vorschau.png'),dpi=150,bbox_inches='tight')
