"""Blende Schwalbennest links/rechts – Außenkontur nach Aufmaß, Ausgabe Skizze (DXF), Prüfschablone (PDF), Vorschau (PNG), STEP.

Ablauf
  1. python3 blende_aufmass.py schablone          -> Pruefschablone_links/rechts_1zu1.pdf + Aufmassskizze.png
  2. Schablone 1:1 drucken, auf den Deckel in die Öffnung legen (an den Treiberkreisen ausrichten),
     an M1–M6 den Spalt zur Innenkante der Edelstahleinfassung messen, in aufmass_<seite>.json eintragen.
  3. python3 blende_aufmass.py links|rechts|beide [--ohne-step]  -> zeichnungen/Kontur_<seite>.dxf/.png/.json, step/Blende_<seite>.step.zip

Geometrie: Ansichtskoordinaten (Blick aus dem Cockpit, x nach rechts, y nach oben, Vorderseite z = 0),
anschließend Transformation ins Koordinatensystem der Fusion-Lautsprechermodelle (Lautsprecher-links/-rechts.step).
Linke Seite: Korpus im Hinterschnitt links, Überstand rechts. Rechte Seite gespiegelt (Logo/M bleiben lesbar).
Korrektur: jede vermessene Kante wird als Gerade durch die beiden korrigierten Messpunkte neu bestimmt
(Winkel- und Maßfehler), Überstandskante bleibt Korpuskante + 17,5 mm."""
import json, math, os, sys, numpy as np
import cadquery as cq
HERE=os.path.dirname(os.path.abspath(__file__)); BLD=os.path.dirname(HERE)
sys.path.insert(0,BLD); import blende_2a35 as B
import mwlogo, signet_m
OUT=os.path.join(HERE,'zeichnungen'); os.makedirs(OUT,exist_ok=True)     # Skizzen, Schablonen, DXF (versioniert)
OUT3D=os.path.join(HERE,'export'); os.makedirs(OUT3D,exist_ok=True)      # STEP roh (groß, nicht versioniert)
ZIP3D=os.path.join(HERE,'step'); os.makedirs(ZIP3D,exist_ok=True)        # STEP gezippt (versioniert)
REF=json.load(open(os.path.join(HERE,'korpus_referenz.json')))
GAP=2.0                               # Soll-Spalt Blende ↔ Edelstahleinfassung
STATIONS={'oben':(0.25,0.75),'unten':(0.22,0.72),'schraeg':(0.22,0.78)}
D_SUB,D_TMT,D_HT=156.2,118.2,46.2

# ---------------- Geometrie je Seite (Ansichtskoordinaten) ----------------
BL_L=np.array([(0,0),(391.6,25.4),(460.7,209.6),(93.8,207.0)])   # Soll-Kontur links (CAD, Spalt 2 mm, Überstand 17,5)
W=float(BL_L[:,0].max())
def kabsch(src,dst):
    src=np.array(src,float); dst=np.array(dst,float); cs,cd=src.mean(0),dst.mean(0)
    H=(src-cs).T@(dst-cd); U,S,Vt=np.linalg.svd(H); R=Vt.T@U.T
    if np.linalg.det(R)<0: Vt[1]*=-1; R=Vt.T@U.T
    return R, cd-R@cs
def side_geometry(side):
    """Soll-Kontur (Ecken: unten-links, unten-rechts, oben-rechts, oben-links), Kanten-Indizes, Features, Transformation."""
    L=REF['links']; off=np.array(L['ansicht_offset'])
    view_L={k:np.array(v)-off for k,v in L['treiber'].items()}; magL=[np.array(m)-off for m in L['magnete']]
    if side=='links':
        poly=BL_L.copy(); R=np.eye(2); t=off
        drv=view_L; mags=magL
        edges={'unten':(0,1),'ueberstand':(1,2),'oben':(2,3),'schraeg':(3,0)}
    else:
        m=lambda p:np.array([W-p[0],p[1]])
        poly=np.array([m(BL_L[1]),m(BL_L[0]),m(BL_L[3]),m(BL_L[2])])
        src=[m(view_L[k]) for k in ('sub','tmt','ht')]+[m(p) for p in magL]
        Rr=REF['rechts']; dst=[Rr['treiber'][k] for k in ('sub','tmt','ht')]+Rr['magnete']
        R,t=kabsch(src,dst)
        res=np.array([R@s+t for s in src])-np.array(dst); print(f'  Einpassung rechts: Restfehler max {np.abs(res).max():.2f} mm')
        Ri=R.T; tov=lambda g:Ri@(np.array(g)-t)
        drv={k:tov(v) for k,v in Rr['treiber'].items()}; mags=[tov(g) for g in Rr['magnete']]
        edges={'unten':(0,1),'oben':(2,3),'schraeg':(1,2),'ueberstand':(3,0)}
    return dict(side=side,poly=poly,edges=edges,drv=drv,mags=mags,R=R,t=t)

def outward(poly,i,j):
    a,b=poly[i],poly[j]; d=(b-a)/np.linalg.norm(b-a); n=np.array([d[1],-d[0]])
    if np.dot(n,poly.mean(0)-a)>0: n=-n
    return d,n
def stations(G):
    out={}
    for k,(t1,t2) in STATIONS.items():
        i,j=G['edges'][k]; a,b=G['poly'][i],G['poly'][j]
        p=[a+(b-a)*t1,a+(b-a)*t2]
        p.sort(key=(lambda q:q[1]) if k=='schraeg' else (lambda q:q[0]))   # Nummerierung: links→rechts bzw. unten→oben
        out[k]=p
    return out
def apply_aufmass(G,meas):
    """Messwerte -> korrigierte Kontur. meas: dict Kante -> (g1,g2) gemessene Spalte (None = Soll)."""
    P=G['poly']; lines={}; st=stations(G)
    for k in ('unten','oben','schraeg'):
        i,j=G['edges'][k]; d,n=outward(P,i,j); g=[GAP if v is None else v for v in meas.get(k,(None,None))]
        p1=st[k][0]+n*(g[0]-GAP); p2=st[k][1]+n*(g[1]-GAP); lines[(i,j)]=(p1,p2-p1)
    i,j=G['edges']['ueberstand']; lines[(i,j)]=(P[i],P[j]-P[i])
    order=[(0,1),(1,2),(2,3),(3,0)]
    def X(l1,l2):
        (p1,d1),(p2,d2)=l1,l2; tt=np.linalg.solve(np.array([d1,-d2]).T,p2-p1); return p1+tt[0]*d1
    return np.array([X(lines[order[k-1]],lines[order[k]]) for k in range(4)])

def read_meas(side):
    J=json.load(open(os.path.join(HERE,f'aufmass_{side}.json')))
    return {'oben':(J['M1_oben_1'],J['M2_oben_2']),'unten':(J['M3_unten_1'],J['M4_unten_2']),'schraeg':(J['M5_schraeg_1'],J['M6_schraeg_2'])}

# ---------------- 3D-Aufbau ----------------
def pip(p,poly):
    c=False
    for k in range(len(poly)):
        (x1,y1),(x2,y2)=poly[k],poly[k-1]
        if (y1>p[1])!=(y2>p[1]) and p[0]<(x2-x1)*(p[1]-y1)/(y2-y1)+x1: c=not c
    return c
def segd(p,a,b):
    p,a,b=map(np.array,(p,a,b)); tt=np.clip(np.dot(p-a,b-a)/np.dot(b-a,b-a),0,1); return np.linalg.norm(p-(a+tt*(b-a)))
def field_holes(G,cx,cy,D):
    """Sonnenblumen-Löcher; rechts gespiegelt (Spirale gegenläufig, symmetrisch zur linken Blende)."""
    if G['side']=='links': return B.field_2a35(cx,cy,D)
    return [(2*cx-x,y,d) for x,y,d in B.field_2a35(cx,cy,D)]
def logo_polys(G,P):
    i,j=G['edges']['unten']; a,b=P[i],P[j]; e=(b-a)/np.linalg.norm(b-a)
    if e[0]<0: e=-e
    ang=math.degrees(math.atan2(e[1],e[0])); n=np.array([e[1],-e[0]])          # n: nach unten
    T0=G['drv']['tmt']; H=B.LOGO_W/mwlogo.ASPECT; dT=np.dot(T0-a,-n)
    C=T0+(dT-(B.LOGO_EDGE+H/2))*n
    polys=[]; mwlogo.draw(lambda p:polys.append(p),lambda ps:polys.extend(ps),lambda p:(float(p[0]),float(p[1])),C[0],C[1],B.LOGO_W,None,angle_deg=ang)
    return polys,ang,C
def logo_faces_from(polys):
    def area(p): p=np.array(p); return 0.5*abs(np.dot(p[:,0],np.roll(p[:,1],1))-np.dot(p[:,1],np.roll(p[:,0],1)))
    polys=[p for p in polys if len(p)>=3 and area(p)>0.01]
    depth=[sum(pip(p[0],q) for q in polys if q is not p) for p in polys]; faces=[]
    for k,p in enumerate(polys):
        if depth[k]%2: continue
        outer=cq.Wire.makePolygon([cq.Vector(x,y,0) for x,y in p],close=True)
        inners=[cq.Wire.makePolygon([cq.Vector(x,y,0) for x,y in q],close=True) for m,q in enumerate(polys) if depth[m]==depth[k]+1 and pip(q[0],p)]
        faces.append(cq.Face.makeFromWires(outer,inners))
    return faces
def build_solid(G,P):
    T=B.T; body=B.poly_wp(P,-T).extrude(T); body=body.faces('>Z').edges().chamfer(B.CHAMFER)
    feats=[('sub',D_SUB),('tmt',D_TMT),('ht',D_HT)]; nh=0
    for key,D in feats:
        x,y=G['drv'][key]; Rf=D/2
        body=body.cut(cq.Workplane('XY',origin=(x,y,-T-1)).circle(Rf).extrude(T+2))
        body=body.cut(cq.Workplane().add(cq.Solid.makeCone(Rf,Rf+B.RING,B.RECESS,pnt=cq.Vector(x,y,-B.RECESS),dir=cq.Vector(0,0,1))))
        pts=field_holes(G,x,y,D); sk=B.SKIN_HT if key=='ht' else B.SKIN
        inners=[]
        if key=='ht':
            M=signet_m.signet_poly(B.M_WIDTH,x,y+B.M_DY,ang=math.radians(B.M_ANG))
            pts=[(px,py,d) for px,py,d in pts if not pip((px,py),M) and min(segd((px,py),M[k-1],M[k]) for k in range(len(M)))-d/2>=0.8]
            inners.append(cq.Wire.makePolygon([cq.Vector(px,py,0) for px,py in M],close=True))
        inners+=[cq.Wire.makeCircle(d/2,cq.Vector(px,py,0),cq.Vector(0,0,1)) for px,py,d in pts]; nh+=len(pts)
        skin=cq.Solid.extrudeLinear(cq.Face.makeFromWires(cq.Wire.makeCircle(Rf,cq.Vector(x,y,0),cq.Vector(0,0,1)),inners),cq.Vector(0,0,sk)).translate((0,0,-B.RECESS-sk))
        body=body.union(cq.Workplane().add(skin.Solids()))
    polys,ang,C=logo_polys(G,P)
    for f in logo_faces_from(polys):
        body=body.cut(cq.Workplane().add(cq.Solid.extrudeLinear(f,cq.Vector(0,0,B.LOGO_DEPTH+0.5)).translate((0,0,-B.LOGO_DEPTH))))
    i,j=G['edges']['ueberstand']; d,n=outward(P,i,j); g0,w,dep=B.GROOVE; a,b=P[i],P[j]
    strip=np.array([a-n*g0-d*20,b-n*g0+d*20,b-n*(g0+w)+d*20,a-n*(g0+w)-d*20])
    body=body.cut(B.poly_wp(strip,-dep).extrude(dep+1))
    for mx,my in G['mags']:
        body=body.cut(cq.Workplane('XY',origin=(float(mx),float(my),-T-0.1)).circle(6.2).extrude(1.6))
    print(f'  {nh} Bohrungen, Logo {ang:+.2f}°')
    return body
def to_global(G,shape):
    R,t=G['R'],G['t']; th=math.degrees(math.atan2(R[1,0],R[0,0]))
    return shape.rotate((0,0,0),(0,0,1),th).translate((float(t[0]),float(t[1]),REF['blende_vorderseite_z']))

# ---------------- Ausgaben ----------------
def write_dxf(G,P,path):
    import ezdxf
    doc=ezdxf.new('R2010'); doc.units=ezdxf.units.MM; msp=doc.modelspace()
    for name,col in (('KONTUR',7),('KONTUR_SOLL',8),('TREIBER',5),('MAGNETE',1),('MESSSTELLEN',3)): doc.layers.add(name,color=col)
    R,t=G['R'],G['t']; g=lambda p:tuple(R@np.array(p)+t)
    msp.add_lwpolyline([g(p) for p in P],close=True,dxfattribs={'layer':'KONTUR'})
    msp.add_lwpolyline([g(p) for p in G['poly']],close=True,dxfattribs={'layer':'KONTUR_SOLL','linetype':'DASHED'})
    for k,D in (('sub',D_SUB),('tmt',D_TMT),('ht',D_HT)): msp.add_circle(g(G['drv'][k]),D/2,dxfattribs={'layer':'TREIBER'})
    for m in G['mags']: msp.add_circle(g(m),6.0,dxfattribs={'layer':'MAGNETE'})
    for k,(p1,p2) in stations(G).items():
        for p in (p1,p2): msp.add_point(g(p),dxfattribs={'layer':'MESSSTELLEN'})
    doc.saveas(path)
def plot(G,P,path,title,meas=None,template=False):
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    if template:
        wmm,hmm=540,290; fig=plt.figure(figsize=(wmm/25.4,hmm/25.4)); ax=fig.add_axes([0,0,1,1]); ox,oy=40,45
        ax.set_xlim(-ox,wmm-ox); ax.set_ylim(-oy,hmm-oy)
    else:
        fig,ax=plt.subplots(figsize=(12,6.2),dpi=140); ax.set_xlim(-30,500); ax.set_ylim(-62,250)
    ax.set_aspect('equal'); ax.axis('off')
    ax.fill(*np.vstack([G['poly'],G['poly'][:1]]).T,color='#eef1f4',zorder=0)
    ax.plot(*np.vstack([G['poly'],G['poly'][:1]]).T,color='#111',lw=1.2,zorder=3,label='Soll-Kontur (Schablonenkante)')
    if not template and not np.allclose(P,G['poly']):
        ax.plot(*np.vstack([P,P[:1]]).T,color='#2a78d6',lw=1.8,zorder=4,label='Kontur nach Aufmaß')
    for k,D,lab in (('sub',D_SUB,'Sub W 130 X'),('tmt',D_TMT,'TMT KT 100 V'),('ht',D_HT,'HT BF 32')):
        x,y=G['drv'][k]; ax.add_patch(plt.Circle((x,y),D/2,fill=False,lw=1.0,color='#444'))
        ax.plot([x-4,x+4],[y,y],color='#444',lw=0.6); ax.plot([x,x],[y-4,y+4],color='#444',lw=0.6)
        ax.text(x,y-D/2+6 if k!='ht' else y-D/2-6,lab+f'  Ø{D}',ha='center',va='center',fontsize=7 if template else 8,color='#444')
    for m in G['mags']: ax.add_patch(plt.Circle(m,6,fill=False,lw=0.6,ls='--',color='#999'))
    st=stations(G); names={'oben':('M1','M2'),'unten':('M3','M4'),'schraeg':('M5','M6')}
    for k,(p1,p2) in st.items():
        i,j=G['edges'][k]; d,n=outward(G['poly'],i,j)
        for p,nm,idx in ((p1,names[k][0],0),(p2,names[k][1],1)):
            ax.annotate('',xy=p,xytext=p+n*14,arrowprops=dict(arrowstyle='->',color='#d0342c',lw=1.2))
            val='' if not meas or meas[k][idx] is None else f'\n{meas[k][idx]:.1f} mm'
            ax.text(*(p+n*(21 if not val else 27)),nm+val,ha='center',va='center',fontsize=9,color='#d0342c',fontweight='bold')
    i,j=G['edges']['ueberstand']; mid=(G['poly'][i]+G['poly'][j])/2; d,n=outward(G['poly'],i,j)
    ax.text(*(mid+n*24),'Überstand\n(Korpus + 17,5)',ha='center',va='center',fontsize=7,color='#777',rotation=0)
    if template:
        ax.plot([0,100],[-30,-30],color='k',lw=2); ax.text(50,-26,'Kontrollmaß 100 mm',ha='center',fontsize=8)
        ax.text(-30,232,f'Prüfschablone {G["side"].upper()} – Maßstab 1:1 (ohne Skalierung drucken!) · Soll-Spalt zur Edelstahleinfassung {GAP:.1f} mm · Blick aus dem Cockpit',fontsize=10)
        ax.text(-30,222,'Schablone auf den Deckel legen, Kreise auf die Treiberausschnitte ausrichten; an M1–M6 Spalt Schablonenkante ↔ Innenkante Einfassung messen.',fontsize=8)
    tx,ty=(380,-20) if template else (None,None)
    if template:
        ax.text(tx,ty+8,'Messwerte [mm]:  M1 ____  M2 ____  M3 ____  M4 ____  M5 ____  M6 ____',fontsize=9)
    else:
        if not meas: ax.text(-25,-52,'Messwerte [mm] eintragen:  M1 ____   M2 ____   M3 ____   M4 ____   M5 ____   M6 ____   (Soll 2,0)',fontsize=9,color='#333')
        ax.set_title(title,loc='left',fontsize=12); ax.legend(loc='lower right',frameon=False,fontsize=9,ncol=1 if not meas else 2)
    fig.savefig(path,dpi=None if template else 140); plt.close(fig)

def run(side,step=True):
    print(f'== {side}'); G=side_geometry(side); meas=read_meas(side); P=apply_aufmass(G,meas)
    dev=[np.linalg.norm(P[k]-G['poly'][k]) for k in range(4)]
    print('  Eckverschiebung gegenüber Soll [mm]:',', '.join(f'{v:.2f}' for v in dev))
    json.dump({'seite':side,'kontur_ansicht':P.round(3).tolist(),'kontur_global':[list(np.round(G['R']@p+G['t'],3)) for p in P],
               'aufmass':{k:v for k,v in meas.items()}},open(os.path.join(OUT,f'Kontur_{side}.json'),'w'),indent=1)
    write_dxf(G,P,os.path.join(OUT,f'Kontur_{side}.dxf'))
    plot(G,P,os.path.join(OUT,f'Kontur_{side}.png'),f'Blende {side}: Kontur nach Aufmaß (Ansicht aus dem Cockpit)',meas)
    if not step: return
    solid=build_solid(G,P); g=to_global(G,solid.val())
    sp=os.path.join(OUT3D,f'Blende_{side}.step'); cq.exporters.export(cq.Workplane().add(g),sp)
    import zipfile
    with zipfile.ZipFile(os.path.join(ZIP3D,f'Blende_{side}.step.zip'),'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z: z.write(sp,os.path.basename(sp))
    print(f'  -> step/Blende_{side}.step.zip, zeichnungen/Kontur_{side}.dxf/.png/.json')
def schablone():
    import matplotlib; matplotlib.use('Agg')
    for side in ('links','rechts'):
        G=side_geometry(side); plot(G,G['poly'],os.path.join(OUT,f'Pruefschablone_{side}_1zu1.pdf'),'',template=True)
        plot(G,G['poly'],os.path.join(OUT,f'Aufmassskizze_{side}.png'),f'Aufmaßskizze {side}: Messstellen M1–M6 (Spalt zur Edelstahleinfassung, Soll {GAP} mm)')
        kacheln(os.path.join(OUT,f'Pruefschablone_{side}_1zu1.pdf'),os.path.join(OUT,f'Pruefschablone_{side}_1zu1_A4_Kacheln.pdf'))
    print('Schablonen/Skizzen erzeugt')
def kacheln(src,dst,ov=15.0):
    """1:1-Schablone auf A4-quer-Kacheln (3×2) mit 15 mm Überlappung, Passkreuzen und Kachelnummer aufteilen."""
    try: import pymupdf
    except ImportError: print('  (pymupdf fehlt – keine A4-Kacheln)'); return
    mm=72/25.4; S=pymupdf.open(src); W0,H0=S[0].rect.width,S[0].rect.height; aw,ah=297*mm,210*mm; m=10*mm
    tw,th=aw-2*m,ah-2*m; nx=math.ceil((W0-ov*mm)/(tw-ov*mm)); ny=math.ceil((H0-ov*mm)/(th-ov*mm)); D=pymupdf.open()
    for r in range(ny):
        for c in range(nx):
            x0=c*(tw-ov*mm); y0=r*(th-ov*mm); clip=pymupdf.Rect(x0,y0,min(x0+tw,W0),min(y0+th,H0))
            pg=D.new_page(width=aw,height=ah); pg.show_pdf_page(pymupdf.Rect(m,m,m+clip.width,m+clip.height),S,0,clip=clip)
            pg.draw_rect(pymupdf.Rect(m,m,m+clip.width,m+clip.height),color=(0.6,0.6,0.6),width=0.3)
            for (px,py) in ((m+ov*mm/2,m+ov*mm/2),(m+clip.width-ov*mm/2,m+ov*mm/2),(m+ov*mm/2,m+clip.height-ov*mm/2),(m+clip.width-ov*mm/2,m+clip.height-ov*mm/2)):
                pg.draw_line((px-4*mm,py),(px+4*mm,py),width=0.3); pg.draw_line((px,py-4*mm),(px,py+4*mm),width=0.3)
            pg.insert_text((m,ah-4*mm),f'Kachel Zeile {r+1} / Spalte {c+1}  ({ny}x{nx}) - A4 quer, 100 % / "Tatsächliche Größe" drucken, an den Passkreuzen überlappend (15 mm) kleben',fontsize=7)
    D.save(dst)
if __name__=='__main__':
    arg=sys.argv[1] if len(sys.argv)>1 else 'schablone'
    if arg=='schablone': schablone()
    else:
        for s in (['links','rechts'] if arg=='beide' else [arg]): run(s,step='--ohne-step' not in sys.argv)
