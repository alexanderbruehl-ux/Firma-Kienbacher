"""Blende Schwalbennest – Variante 2A (Alu hochglanzpoliert, Lochmuster „Sonnenblume“) + einfache Einbauszene.
Koordinaten: CAD-System der Einbauschnittstelle (mm), Blendenvorderseite = Rumpfoberfläche bei z = 0,
+z zeigt ins Cockpit. Ausgabe: export/*.step, export/*.stl
    python3 blende_2a.py
"""
import json, math, os, sys, numpy as np
import cadquery as cq
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.normpath(os.path.join(HERE,'..','..'))
OUT=os.path.join(HERE,'export'); os.makedirs(OUT,exist_ok=True)
P=json.load(open(os.path.join(ROOT,'parameter.json')))
sys.path.insert(0,os.path.join(ROOT,'03_konzepte','logo')); import mwlogo

# ---------------- Parameter ----------------
T=8.5                    # Blendendicke
SKIN=2.2                 # Restwand in den Lochfeldern
RECESS=0.6               # Absenkung Lochfeld vorne
RING=2.0                 # Breite Diamantschnitt-Konus
CHAMFER=0.5              # Glanzfase Außenkante
GROOVE=(12.0,1.2,0.6)    # Kantennut: Abstand zur rechten Kante (= 12-mm-Kantenband), Breite, Tiefe
LOGO_DEPTH=0.35
LOGO_W=115.0; LOGO_ANG=math.degrees(math.atan2(25.4,391.6)); LOGO_EDGE=8.0
BL=np.array(P['blende_vorgaben']['kontur_foto_angepasst']['ecken'])      # (0/0)(391.6/25.4)(460.7/209.6)(93.8/207)
HOLES=[(a['mitte'][0],a['mitte'][1],a['d']) for a in P['einbauschnittstelle']['ausschnitte']]
DK=np.array(P['einbauschnittstelle']['deckel_front'])
MAGNETS=[(23.2,16.1),(103.2,192.6),(364.5,38.1),(423.3,194.8)]
STEPS=6                  # Bohrstufen

def phyllotaxis(cx,cy,D):
    R=D/2-1.8; big=D>60; pitch=3.1 if big else 2.2
    n=int((R/pitch)**2*math.pi*0.92); c=R/math.sqrt(n); g=math.radians(137.50776); pts=[]
    for i in range(1,n):
        r=c*math.sqrt(i); a=i*g; t=r/R
        d=(0.9+1.9*t**1.25) if big else (0.7+0.9*t)
        if r+d/2>R: continue
        pts.append((cx+r*math.cos(a),cy+r*math.sin(a),d))
    return pts
def quantize(pts):
    ds=np.array([p[2] for p in pts]); lv=np.round(np.linspace(ds.min(),ds.max(),STEPS),1)
    return [(x,y,float(lv[np.argmin(abs(lv-d))])) for x,y,d in pts], lv

def poly_wp(pts,z=0.0):
    return cq.Workplane('XY',origin=(0,0,z)).polyline([tuple(map(float,p)) for p in pts]).close()

def offset_poly(poly,g):
    """konvexes Polygon um g nach außen versetzen"""
    c=poly.mean(0); L=[]
    for i in range(len(poly)):
        a=poly[i]; b=poly[(i+1)%len(poly)]; d=b-a; n=np.array([d[1],-d[0]])/np.linalg.norm(d)
        if np.dot(n,a-c)<0: n=-n
        L.append((a+n*g,d))
    out=[]
    for i in range(len(L)):
        (p1,d1),(p2,d2)=L[i-1],L[i]; t=np.linalg.solve(np.array([d1,-d2]).T,p2-p1); out.append(p1+t[0]*d1)
    return np.array(out)

def logo_faces():
    """Logo-Polygone (mm, gedreht, positioniert) -> CadQuery-Faces mit Punzen."""
    a=math.radians(LOGO_ANG); H=LOGO_W/mwlogo.ASPECT
    T0=np.array([286.1,120.7]); n=np.array([math.sin(a),-math.cos(a)]); dT=np.dot(T0,-n)
    C=T0+(dT-(LOGO_EDGE+H/2))*n
    polys=[]
    mwlogo.draw(lambda p:polys.append(p), lambda ps:polys.extend(ps), lambda p:(float(p[0]),float(p[1])), C[0],C[1],LOGO_W,None,angle_deg=LOGO_ANG)
    def area(p): p=np.array(p); return 0.5*abs(np.dot(p[:,0],np.roll(p[:,1],1))-np.dot(p[:,1],np.roll(p[:,0],1)))
    def inside(pt,poly):
        x,y=pt; c=False; p=np.array(poly)
        for i in range(len(p)):
            x1,y1=p[i]; x2,y2=p[i-1]
            if (y1>y)!=(y2>y) and x<(x2-x1)*(y-y1)/(y2-y1)+x1: c=not c
        return c
    polys=[p for p in polys if len(p)>=3 and area(p)>0.01]
    depth=[sum(inside(p[0],q) for q in polys if q is not p) for p in polys]
    faces=[]
    for i,p in enumerate(polys):
        if depth[i]%2: continue
        outer=cq.Wire.makePolygon([cq.Vector(x,y,0) for x,y in p],close=True)
        inners=[cq.Wire.makePolygon([cq.Vector(x,y,0) for x,y in q],close=True) for j,q in enumerate(polys) if depth[j]==depth[i]+1 and inside(q[0],p)]
        faces.append(cq.Face.makeFromWires(outer,inners))
    return faces, C

def build_blende():
    body=poly_wp(BL,-T).extrude(T)
    body=body.faces('>Z').edges().chamfer(CHAMFER)
    allpts=[]
    for x,y,D in HOLES:
        Rf=D/2
        cyl=cq.Workplane('XY',origin=(x,y,-T-1)).circle(Rf).extrude(T+2)
        cone=cq.Solid.makeCone(Rf,Rf+RING,RECESS,pnt=cq.Vector(x,y,-RECESS),dir=cq.Vector(0,0,1))
        body=body.cut(cyl).cut(cq.Workplane().add(cone))
        pts,lv=quantize(phyllotaxis(x,y,D)); allpts+=pts
        outer=cq.Wire.makeCircle(Rf,cq.Vector(x,y,0),cq.Vector(0,0,1))
        inners=[cq.Wire.makeCircle(d/2,cq.Vector(px,py,0),cq.Vector(0,0,1)) for px,py,d in pts]
        skin=cq.Solid.extrudeLinear(cq.Face.makeFromWires(outer,inners),cq.Vector(0,0,SKIN)).translate((0,0,-RECESS-SKIN))
        body=body.union(cq.Workplane().add(skin))
        print(f'  Feld Ø{D}: {len(pts)} Bohrungen, Stufen {list(lv)}')
    # Logo einfräsen
    faces,C=logo_faces()
    for f in faces:
        body=body.cut(cq.Workplane().add(cq.Solid.extrudeLinear(f,cq.Vector(0,0,LOGO_DEPTH+0.5)).translate((0,0,-LOGO_DEPTH))))
    # Kantennut parallel zur rechten Kante
    a,b=BL[1],BL[2]; d=(b-a)/np.linalg.norm(b-a); nrm=np.array([-d[1],d[0]])
    if np.dot(nrm,BL.mean(0)-a)<0: nrm=-nrm
    g0,w,dep=GROOVE
    strip=np.array([a+nrm*g0-d*20,b+nrm*g0+d*20,b+nrm*(g0+w)+d*20,a+nrm*(g0+w)-d*20])
    body=body.cut(poly_wp(strip,-dep).extrude(dep+1))
    # Magnettaschen hinten (Stahlscheibe Ø12 × 1,5)
    for mx,my in MAGNETS:
        body=body.cut(cq.Workplane('XY',origin=(mx,my,-T-0.1)).circle(6.2).extrude(1.6))
    print(f'  Bohrungen gesamt: {len(allpts)}')
    return body, allpts, C

def build_scene():
    op=np.array([(-3.2,-2.2),(733.2,45.5),(854.1,214.3),(92.5,209.0)])     # Öffnung Innenkante Einfassung (aus Entzerrung)
    op[0]=offset_poly(BL,2.0)[0]; op[3]=offset_poly(BL,2.0)[3]
    op[1]=offset_poly(BL,2.0)[0]+(op[1]-op[0]); op[2]=offset_poly(BL,2.0)[3]+(op[2]-op[3])
    hull=cq.Workplane('XY',origin=(-220,-160,-10)).rect(1300,560,centered=False).extrude(10)
    hull=hull.cut(poly_wp(op,-11).extrude(12))
    frame=poly_wp(offset_poly(op,9.0),0).extrude(1.6).cut(poly_wp(op,-1).extrude(4))
    frame=frame.edges('>Z').fillet(0.7)
    cav=np.vstack([offset_poly(op,4.0),DK+[[-4,-4],[4,-4],[4,4],[-4,4]]])
    from scipy.spatial import ConvexHull
    hullpts=cav[ConvexHull(cav).vertices]
    pocket=poly_wp(offset_poly(hullpts,6.0),-156).extrude(146).cut(poly_wp(hullpts,-150).extrude(141))
    corpus=poly_wp(DK,-149).extrude(139)
    return hull,frame,pocket,corpus

if __name__=='__main__':
    b,pts,C=build_blende()
    cq.exporters.export(b,os.path.join(OUT,'Blende_2A.step'))
    cq.exporters.export(b,os.path.join(OUT,'Blende_2A.stl'),tolerance=0.02,angularTolerance=0.15)
    for name,s in zip(['Rumpf','Einfassung','Fach','Korpus'],build_scene()):
        cq.exporters.export(s,os.path.join(OUT,f'Szene_{name}.stl'),tolerance=0.05,angularTolerance=0.2)
    v=b.val().Volume(); print(f'Blende 2A: Volumen {v/1000:.1f} cm³, Masse {v*2.70/1000:.0f} g (EN AW-6082)')
