"""Regelwerk für den Claim: Buchstaben aus Regeln konstruiert (abgeleitet vom Meisterwerke-Schriftzug), Einheiten: Kapitalhöhe = 1000, x=0 linke Kante.
Jeder Buchstabe: Liste geschlossener Konturen aus kubischen Béziers (je 4 Punkte (x,y)), y nach unten (oben = 0). Regeln & Freigaben: siehe REGELN_CLAIM.md."""
import numpy as np, os, sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import curvefit
CAP=1000.0
# --- Regeln (Stand: Vorschlag, vom Nutzer pro Buchstabe freizugeben) ---
STAMM=113.8           # Stammstärke in der Mitte
AUSSTELLUNG=20.5      # Zusatzbreite an den Enden (Ende = STAMM+AUSSTELLUNG)
AUSLAUF=390.0         # Länge des Auslaufs (kubisch) von den Enden zur Mitte
LINKS_ANTEIL=0.57     # Anteil der Ausstellung links am OBEREN Ende; am unteren Ende 1-LINKS_ANTEIL (Punktsymmetrie: oben mehr nach links, unten mehr nach rechts)
def breite(y,cap=CAP):
    d=np.minimum(y,cap-y); t=np.clip(1-d/AUSLAUF,0,1); return STAMM+AUSSTELLUNG*t**3
def _edge_curve(pts,err=0.02):
    """glatte Kante (Punktfolge) -> kubische Béziers"""
    pts=np.asarray(pts,float); return curvefit._fit(pts,curvefit._unit(pts[3]-pts[0]),curvefit._unit(pts[-4]-pts[-1]),err)
# Einbuchtung der geraden Enden (Schriftzug-I): Oberkante y(x) als Kubik, x ab linker Spitze; Unterkante = Oberkante um 180° gedreht (Punktsymmetrie).
DELLE_OBEN=np.array([-9.5e-07,-0.00031543,0.03883999,2.90811263])
def _poly_bezier(c,x0,x1):
    p=np.poly1d(c); d=p.deriv(); h=x1-x0
    return np.array([[x0,p(x0)],[x0+h/3,p(x0)+d(x0)*h/3],[x1-h/3,p(x1)-d(x1)*h/3],[x1,p(x1)]])
def letter_I(delle=True):
    p=np.poly1d(DELLE_OBEN); xm=LINKS_ANTEIL*AUSSTELLUNG                                 # x der linken Kante in der Stammmitte
    anteil=lambda y: np.where(np.asarray(y)<CAP/2,LINKS_ANTEIL,1-LINKS_ANTEIL)
    xl_f=lambda y: xm-anteil(y)*(breite(y)-STAMM); xr_f=lambda y: xl_f(y)+breite(y)
    W=float(xr_f(0.0)-xl_f(0.0))
    ytl=float(p(xl_f(0.0))) if delle else 0.0; ytr=float(p(W)) if delle else 0.0        # obere Ecken (links tiefer als rechts)
    ybl,ybr=CAP-ytr,CAP-ytl                                                              # untere Ecken (180°-Drehung)
    yl=np.linspace(ytl,ybl,201); yr=np.linspace(ytr,ybr,201)
    left=np.c_[xl_f(yl),yl]; right=np.c_[xr_f(yr),yr]
    if delle: top=_poly_bezier(DELLE_OBEN,left[0,0],right[0,0])
    else: top=np.array([left[0],left[0]+(right[0]-left[0])/3,left[0]+2*(right[0]-left[0])/3,right[0]])
    xs=left[0,0]+right[-1,0]                                                             # Drehmitte x = (linke obere + rechte untere Spitze)/2
    bot=np.c_[xs-top[:,0],CAP-top[:,1]]                                                  # 180° um (xs/2, 500) -> läuft von unten rechts nach unten links
    out=[top]+curvefit._fit(right,curvefit._unit(right[3]-right[0]),curvefit._unit(right[-4]-right[-1]),0.02)+[bot]+curvefit._fit(left[::-1],curvefit._unit(left[::-1][3]-left[::-1][0]),curvefit._unit(left[::-1][-4]-left[::-1][-1]),0.02)
    return [out]
def sample(contour,n=24):
    pts=[]
    for c in contour:
        t=np.linspace(0,1,n,endpoint=False); mt=1-t; pts+=list((mt**3)[:,None]*c[0]+(3*mt*mt*t)[:,None]*c[1]+(3*mt*t*t)[:,None]*c[2]+(t**3)[:,None]*c[3])
    return np.array(pts)

# ---------------------------------------------------------------------------------------------------------------------------
# Buchstaben, die im Meisterwerke-Schriftzug (Vektor) vorkommen und im Claim dieselbe Breite/Strichstärke haben: direkt aus dem Schriftzug
# übernommen und zu wenigen sauberen Béziers zusammengefasst (kein Pixel-Rauschen). Einheiten: I-Höhe = 1000, x=0 linke Spitze, y=0 Oberkante des I.
# ---------------------------------------------------------------------------------------------------------------------------
def _wordmark_glyphs():
    import mwlogo
    polys=[np.array(p) for p in mwlogo._subpaths(mwlogo._T['wordmark'])]
    from shapely.geometry import Polygon
    P=[Polygon(p) for p in polys]
    outer=[i for i,p in enumerate(P) if not any(j!=i and P[j].contains(p) for j in range(len(P)))]; outer.sort(key=lambda i:P[i].bounds[0])
    names=['M','E','I','S','T','E','R','W','E','R','K1','K2','E']; idx={}
    for n,i in zip(names,outer): idx.setdefault(n,[]).append(i)
    return polys,idx
def _fit_polygon(poly_norm,k=0.041):
    """geschlossenes Polygon (Einheiten, I-Höhe=1000) -> Béziers: Ecken erkennen, dazwischen anpassen (Parameter für px-Maß mit Kapitalhöhe 41 px)"""
    cont,cor=curvefit.contour_to_beziers(poly_norm*k,ds=0.08,sig=0.12,err=0.0015,corner_kw=dict(thr=35,minsep=0.5,win=0.5,sig=0.15),edge=0.25,span=(0.2,0.7),line_tol=0.03)
    return [c/k for c in cont]
ARM_FAKTOR_E=1.10    # Armlänge des E im Claim gegenüber dem Schriftzug-E (gemessen am GIF: Armspitzen 512/488/537 statt 475/449/509 -> 1,07..1,12)
STAMM_RAND_E=125.0   # rechte Kante des Stamms im E: Arme werden nur rechts davon gestreckt
def letter_E(arm_faktor=None):
    """E aus dem Schriftzug (alle vier E im Schriftzug sind identisch), Arme um ARM_FAKTOR_E gestreckt. Rückgabe: (Konturen, y_offset gegenüber der I-Oberkante)"""
    polys,idx=_wordmark_glyphs(); I=polys[idx['I'][0]]; F=1000/(I[:,1].max()-I[:,1].min()); E=polys[idx['E'][0]]
    En=(E-[E[:,0].min(),E[:,1].min()])*F; dy=(E[:,1].min()-I[:,1].min())*F
    f=ARM_FAKTOR_E if arm_faktor is None else arm_faktor
    En[:,0]=np.where(En[:,0]<=STAMM_RAND_E,En[:,0],STAMM_RAND_E+(En[:,0]-STAMM_RAND_E)*f)       # nur die Arme strecken, Stamm bleibt
    return [_fit_polygon(En)],float(dy)

# --- F: abgeleitet vom E (gleicher Stamm und gleicher oberer Arm), ohne unteren Arm; Stammfuß wie beim I; mittlerer Arm kürzer (GIF: 19 statt 20 px) ---
F_MITTELARM_KUERZER=24.0   # Einheiten (1 px im Claim)
def _stem_foot_cut():       # y, ab dem der Stamm vom I übernommen wird (dort sind Stamm-Kanten von E und I praktisch gleich)
    return 700.0
def letter_F():
    from shapely.geometry import Polygon, box
    polys,idx=_wordmark_glyphs(); I=polys[idx['I'][0]]; F=1000/(I[:,1].max()-I[:,1].min()); E=polys[idx['E'][0]]
    En=(E-[E[:,0].min(),E[:,1].min()])*F; dy=float((E[:,1].min()-I[:,1].min())*F)
    En[:,0]=np.where(En[:,0]<=STAMM_RAND_E,En[:,0],STAMM_RAND_E+(En[:,0]-STAMM_RAND_E)*ARM_FAKTOR_E)
    # mittleren Arm kürzen (Schrumpfung der Armlänge um F_MITTELARM_KUERZER, nur Punkte des mittleren Arms)
    L=(449.0-STAMM_RAND_E)*ARM_FAKTOR_E; s=1-F_MITTELARM_KUERZER/L
    m=(En[:,1]>400)&(En[:,1]<560)&(En[:,0]>STAMM_RAND_E+0.5); En[m,0]=STAMM_RAND_E+(En[m,0]-STAMM_RAND_E)*s
    top=Polygon(En).buffer(0).intersection(box(-50,-50,1000,_stem_foot_cut()))
    Ipoly=Polygon(sample(letter_I()[0],60)).buffer(0); Ipoly=Polygon(np.c_[Ipoly.exterior.coords][:,0],np.c_[Ipoly.exterior.coords][:,1]+(-dy)) if False else Ipoly
    from shapely import affinity
    Ishift=affinity.translate(Ipoly,0,-dy)                                        # I-Koordinaten (Oberkante 0) -> E-Koordinaten (Oberkante des E = 0)
    foot=Ishift.intersection(box(-50,_stem_foot_cut()-10,1000,1100))
    poly=top.union(foot).buffer(0.0); poly=poly.simplify(0.05)
    pts=np.array(poly.exterior.coords)[:-1]
    return [_fit_polygon(pts)],dy

# --- T: Schriftzug-T, Balkenhälften auf die Claim-Breite gestaucht (GIF: 31 px = 756 Einheiten, Schriftzug 843); Stamm, Fuß, Balkendicke und Spitzen bleiben ---
T_BREITE=756.0
T_STAMM=(360.0,474.0)      # linke/rechte Stammkante im Schriftzug-T (I-Höhe = 1000)
def letter_T(breite=None):
    polys,idx=_wordmark_glyphs(); I=polys[idx['I'][0]]; F=1000/(I[:,1].max()-I[:,1].min()); T=polys[idx['T'][0]]
    Tn=(T-[T[:,0].min(),T[:,1].min()])*F; dy=float((T[:,1].min()-I[:,1].min())*F)
    xl,xr=T_STAMM; w=Tn[:,0].max(); b=T_BREITE if breite is None else breite
    s=(b-(xr-xl))/(w-(xr-xl))                                                       # Stauchung der beiden Balkenhälften
    x=Tn[:,0]; Tn[:,0]=np.where(x<xl,xl-(xl-x)*s,np.where(x>xr,xr+(x-xr)*s,x)); Tn[:,0]-=Tn[:,0].min()
    return [_fit_polygon(Tn)],dy

# --- R: Stamm, Steg und Bogen aus dem Schriftzug-R (an das Claim-R angepasst), das Bein als saubere Form mit geraden Kanten (aus den GIF-Pixeln beider R) ---
R_BOGEN=1.086       # x-Faktor für den Bogen (ab Stammkante 125)
R_STEG_Y=483.0      # Höhe der Mittelsteg-Mitte (Schriftzug-R: 546)
R_BEIN_STEIGUNG=0.7819         # gemeinsame Steigung der Beinkanten (38,0° von der Senkrechten; GIF: 37,3° links / 38,8° rechts = Auslauf-Aufweitung)
R_BEIN_LINKS_700=334.1         # linke Beinkante bei y=700
R_BEIN_BREITE=150.5            # waagrechte Beinbreite in der Mitte (y=700)
R_BEIN_OBEN=480.0              # Oberkante des Bein-Polygons (liegt im Steg, wird mit ihm vereinigt)
def _fuss_delle_unten(x0,x1,n=30):
    """untere Endkante (von x0 nach x1, x0<x1) mit der Delle des I (um 180° gedreht), x auf die I-Breite (134) normiert; liefert (x,y)"""
    xs=np.linspace(x0,x1,n); u=(xs-x0)/(x1-x0)*134.0; return np.c_[xs,CAP-np.poly1d(DELLE_OBEN)(134.0-u)]
def _bein_aufgeweitet(al,bl,ar,br,yt,n=60):
    ys=np.linspace(yt,CAP,n); tf=np.clip(1-(CAP-ys)/AUSLAUF,0,1)**3
    xl=al+bl*ys-(1-LINKS_ANTEIL)*AUSSTELLUNG*tf; xr=ar+br*ys+LINKS_ANTEIL*AUSSTELLUNG*tf          # unten mehr nach rechts (Punktsymmetrie zum Kopf)
    fuss=_fuss_delle_unten(xl[-1],xr[-1])
    return list(zip(xl,ys))[:-1]+list(map(tuple,fuss))+list(zip(xr,ys))[::-1][1:]
def letter_R(unten_runter=18.0,innen_hoch=18.0,glatt=True):   # Variante D (Engstelle am Bogen: Wand 75 statt 37)
    from shapely.geometry import Polygon as Pg
    polys,idx=_wordmark_glyphs(); I=polys[idx['I'][0]]; F=1000/(I[:,1].max()-I[:,1].min()); Rp=polys[idx['R'][0]]
    Ro=Pg(Rp); inner=[p for p in polys if Pg(p).within(Ro) and not np.array_equal(p,Rp)][0]
    o=[Rp[:,0].min(),Rp[:,1].min()]; Rn=(Rp-o)*F; Cn=(inner-o)*F; dy=float((Rp[:,1].min()-I[:,1].min())*F)
    STEM,YB=125.0,546.0
    def warp(P):                                                                     # Steghöhe verschieben, Bogen weiten (Bein wird unten ersetzt)
        P=np.asarray(P,float); x=P[:,0]; y=P[:,1]
        yn=np.where(y<=YB,y*(R_STEG_Y/YB),R_STEG_Y+(y-YB)*(1000-R_STEG_Y)/(1000-YB)); xn=np.where(x>STEM,STEM+(x-STEM)*R_BOGEN,x)
        return np.c_[xn,yn]
    base=Pg(warp(Rn)).buffer(0)
    # Bogenunterseite im Claim (aus den GIF-Pixeln, Zeilen 652-660): glatte Kurve x(y) vom Bogen bis zur rechten Beinkante (Kerbe)
    bl=br=R_BEIN_STEIGUNG; al=R_BEIN_LINKS_700-bl*700.0; ar=al+R_BEIN_BREITE; yt=R_BEIN_OBEN
    if glatt:      # Unterseite = eine kubische Bézierkurve, tangentenstetig aus der Bogenaußenkante bis zur Kerbe an der rechten Beinkante
        yk=512.0+unten_runter; P0=np.array([613.0,300.0]); P3=np.array([ar+br*yk,yk])
        t0=np.array([-0.3,1.0]); t0/=np.linalg.norm(t0); t3=np.array([1.0,-0.443]); t3/=np.linalg.norm(t3)
        P1=P0+t0*76.0; P2=P3+t3*(151.7+1.5*unten_runter); tt=np.linspace(0,1,80)[:,None]
        path=(1-tt)**3*P0+3*(1-tt)**2*tt*P1+3*(1-tt)*tt**2*P2+tt**3*P3
        pts=path
    else:
        pts=np.array([(610,317),(585,341),(561,366),(561,390),(512,415),(488,439),(439,463),(341,488),(ar+br*512.0,512.0)],float)
        cx=np.polyfit(pts[:,1],pts[:,0],3); yy=np.linspace(pts[0,1],512.0,40); path=np.c_[np.polyval(cx,yy),yy]
    yt=min(yt,path[-1,1]-20.0); xk=path[-1,0]
    region=Pg([(-100,-100),(1200,-100),(1200,pts[0,1])]+list(map(tuple,path))+[(xk,1100),(-100,1100)])   # alles oberhalb der Kurve und links von der Beinkante bleibt
    base=base.intersection(region)
    leg=Pg(_bein_aufgeweitet(al,bl,ar,br,yt))      # Beinkanten laufen am Fuß wie beim I kubisch aus, Fußkante mit der Delle des I
    poly=base.union(leg).buffer(0).buffer(-1.0,join_style=2).buffer(1.0,join_style=2).simplify(0.05)
    outer=np.array(poly.exterior.coords)[:-1]
    Cw=warp(Cn)
    if innen_hoch:     # unteren Rand des Bogeninnenraums anheben (Wandstärke ↑), Stammkante bleibt senkrecht
        t=np.clip((Cw[:,1]-250.0)/205.0,0,None); Cw[:,1]-=innen_hoch*t**2
    return [_fit_polygon(outer),_fit_polygon(Cw)],dy


# --- P: Stamm und Bogen wie beim R (gleiche Bogenwand-Regel), ohne Bein; der Mittelsteg endet unten waagrecht am Stamm ---
P_BOGEN=1.133       # x-Faktor Bogen ab Stammkante 125 (Bogen rechts bei 634 = 26 px im GIF)
P_INNEN_X=0.946     # Innenraum-Faktor x ab Stammkante
P_STEG_Y=498.0      # Mittelsteg im Claim-P ca. 1 px (24) tiefer als im R
P_STEG_UNTEN=539.0  # Unterkante des Mittelstegs (GIF: Zeile 22)
P_UNTERSEITE=[(610,354),(585,402),(561,427),(537,451),(512,476)]    # Mittellinie der GIF-Treppe (Bogenunterseite)
def letter_P(innen_hoch=18.0):
    from shapely.geometry import Polygon as Pg
    from scipy.optimize import least_squares
    polys,idx=_wordmark_glyphs(); I=polys[idx['I'][0]]; F=1000/(I[:,1].max()-I[:,1].min()); Rp=polys[idx['R'][0]]
    Ro=Pg(Rp); inner=[p for p in polys if Pg(p).within(Ro) and not np.array_equal(p,Rp)][0]
    o=[Rp[:,0].min(),Rp[:,1].min()]; Rn=(Rp-o)*F; Cn=(inner-o)*F; dy=-1.4
    STEM,YB=125.0,546.0
    def warp(P):
        P=np.asarray(P,float); x=P[:,0]; y=P[:,1]
        yn=np.where(y<=YB,y*(P_STEG_Y/YB),P_STEG_Y+(y-YB)*(1000-P_STEG_Y)/(1000-YB)); xn=np.where(x>STEM,STEM+(x-STEM)*P_BOGEN,x)
        return np.c_[xn,yn]
    base=Pg(warp(Rn)).buffer(0)
    # Außenkante des Bogens bei y=300 und ihre Richtung
    from shapely.geometry import LineString
    xo=lambda y: LineString([(0,y),(3000,y)]).intersection(base).bounds[2]
    P0=np.array([xo(300.0),300.0]); sl=(xo(310.0)-xo(290.0))/20.0; t0=np.array([sl,1.0]); t0/=np.linalg.norm(t0)
    yb=P_STEG_UNTEN; G=np.array(P_UNTERSEITE,float); tt=np.linspace(0,1,120)[:,None]
    def bez(p):
        a,b,x3=p; P3=np.array([x3,yb]); P1=P0+t0*a; P2=P3+np.array([1.0,0.0])*b
        return (1-tt)**3*P0+3*(1-tt)**2*tt*P1+3*(1-tt)*tt**2*P2+tt**3*P3
    res=lambda p:[np.min(np.linalg.norm(bez(p)-g,axis=1)) for g in G]+[0.02*(p[2]-380.0)]
    p=least_squares(res,[80,150,380.0],bounds=([10,10,200],[300,400,500])).x; path=bez(p)
    box=lambda x0,y0,x1,y1: Pg([(x0,y0),(x1,y0),(x1,y1),(x0,y1)])
    unten=Pg([(100.0,290.0),tuple(P0)]+list(map(tuple,path))+[(100.0,yb)])        # Bogenunterseite + waagrechter Stegboden (immer glatt, unabhängig von der Schriftzug-Kontur)
    poly=base.intersection(box(-100,-100,1500,300.0)).union(base.intersection(box(-100,-100,135.0,yb))).union(base.intersection(box(-100,-100,135.0,1100))).union(unten.intersection(base.buffer(60))).buffer(0)
    poly=poly.buffer(-1.0,join_style=2).buffer(1.0,join_style=2).simplify(0.05)
    outer=np.array(poly.exterior.coords)[:-1]
    Cw=warp(Cn)
    t=np.clip((Cw[:,1]-250.0)/205.0,0,None); Cw[:,1]-=innen_hoch*t**2
    Cw[:,0]=np.where(Cw[:,0]>STEM,STEM+(Cw[:,0]-STEM)*P_INNEN_X,Cw[:,0])     # Innenraum rechts an die GIF-Pixel (Bogenwand 6 px)
    return [_fit_polygon(outer),_fit_polygon(Cw)],dy


# --- D: linke Hälfte (Stamm, oberer und unterer Arm samt Einzug) aus dem Schriftzug-E, rechts ein Bogen aus je zwei Bézierkurven (außen/innen), angepasst an die GIF-Pixel ---
D_XC=300.0          # ab hier beginnt der Bogen (Arme laufen bis dahin wie beim E)
# Bogenparameter: je (Anlauf oben, Ausrundung oben, Anlauf unten, Ausrundung unten, Außenrand x, Beginn/Ende des senkrechten Rands oben/unten);
# per Flächenabgleich (symmetrische Differenz) mit den GIF-Pixeln angepasst
D_BOGEN_AUSSEN=(233.5,308.4,210.2,299.8,900.4,342.6,568.9)
D_BOGEN_INNEN=(302.4,155.0,313.8,147.2,753.0,340.1,636.9)
def letter_D():
    from shapely.geometry import Polygon as Pg, LineString, box
    polys,idx=_wordmark_glyphs(); I=polys[idx['I'][0]]; F=1000/(I[:,1].max()-I[:,1].min()); E=polys[idx['E'][0]]
    En=(E-[E[:,0].min(),E[:,1].min()])*F; dy=-1.8
    Ep=Pg(En).buffer(0)
    def span(x):                      # (Oberkante, Unterkante der Arme, Innenkanten) bei x
        L=LineString([(x,-10),(x,1030)]).intersection(Ep); g=sorted([b.bounds[1::2] for b in (L.geoms if hasattr(L,'geoms') else [L])])
        return g[0],g[-1]
    top0,bot0=span(D_XC); yt,yi_t=top0[0],top0[1]; yi_b,yb=bot0[0],bot0[1]
    tt=np.linspace(0,1,150)[:,None]
    def bz(P0,P1,P2,P3): return (1-tt)**3*P0+3*(1-tt)**2*tt*P1+3*(1-tt)*tt**2*P2+tt**3*P3
    def kurve(par,ytop,ybot):
        au,bu,ad,bd,xm,ya,yv=par
        P0=np.array([D_XC,ytop]); P3=np.array([xm,ya]); u=bz(P0,P0+np.array([au,0.0]),P3-np.array([0.0,bu]),P3)
        Q0=np.array([xm,yv]); Q3=np.array([D_XC,ybot]); d=bz(Q0,Q0+np.array([0.0,bd]),Q3+np.array([ad,0.0]),Q3)
        return np.vstack([u,d])
    out=kurve(D_BOGEN_AUSSEN,yt,yb); inn=kurve(D_BOGEN_INNEN,yi_t,yi_b)
    xs=np.linspace(125.0,D_XC,12); topk=[(x,span(x)[0][1]) for x in xs]; botk=[(x,span(x)[1][0]) for x in xs]
    Cc=Pg([(125.0,topk[0][1])]+topk[1:]+list(map(tuple,inn[1:-1]))+botk[::-1]).buffer(0)
    xs2=np.linspace(100.0,D_XC,30); fill=Pg([(x,span(x)[0][0]) for x in xs2]+[(x,span(x)[1][1]) for x in xs2[::-1]]).buffer(0)       # Arme samt Stamm exakt nach der E-Kontur
    Fo=Ep.intersection(box(-10,-10,D_XC,1030)).union(fill).union(Pg(np.vstack([[(D_XC,yt)],out[1:-1],[(D_XC,yb)]])).buffer(0))
    G=Fo.difference(Cc).buffer(0).buffer(-0.8,join_style=2).buffer(0.8,join_style=2).simplify(0.05)
    assert G.geom_type=='Polygon' and len(G.interiors)==1, (G.geom_type,len(getattr(G,'interiors',[])))
    return [_fit_polygon(np.array(G.exterior.coords)[:-1]),_fit_polygon(np.array(G.interiors[0].coords)[:-1])],dy


def _dent_kante(xl,xr,oben=True):
    """gerade Endkante zwischen x=xl und xr (xl<xr) mit der Delle des I (Regel für ALLE flachen Stammenden); Rückgabe: 4 Béziers-Punkte von xl nach xr.
    oben: Delle des I-Kopfs, unten: um 180° gedreht (Punktsymmetrie); die Dellenform wird auf die Kantenbreite normiert (I-Stamm = 134)"""
    w=xr-xl; sc=np.poly1d([134.0/w,0.0]); p=np.poly1d(DELLE_OBEN)
    q=p(sc) if oben else -p(np.poly1d([-134.0/w,134.0]))
    B=_poly_bezier(q.coeffs,0.0,w); B=B.copy(); B[:,0]+=xl
    if not oben: B[:,1]+=CAP
    return B

# --- N: Stämme mit den geschwungenen Auslauf-Kanten des I (kubisch t³ über AUSLAUF, exakt als Bézier), Diagonale gerade unter ~42,8° (Regel aus allen drei N im GIF),
#     die Diagonale läuft an beiden Enden spitz in die Stämme; Punktsymmetrie bei Diagonale und Auslaufrichtung ---
N_BREITE=854.0                       # Gesamtbreite (inkl. Ausstellung rechts oben)
N_L=(24.4,97.6)                      # linker Stamm (Haarlinie 73) in der Mitte: x-Bereich
N_R=(768.0,829.4)                    # rechter Stamm (im GIF schmaler: 61) in der Mitte
N_AUSSTELLUNG_L_UNTEN=24.4           # linker Stamm: Fuß weitet sich nach links (GIF: 4 statt 3 px)
N_AUSSTELLUNG_R_OBEN=(12.2,24.4)     # rechter Stamm: Kopf weitet sich links/rechts (GIF: 4 statt 2 px)
N_DIAG_A,N_DIAG_B=62.0,0.927         # obere Diagonalkante x = a + b*y ; untere punktsymmetrisch: a_u = W - a - 1000*b
def letter_N():
    W=N_BREITE; a=N_DIAG_A; b=N_DIAG_B; al=W-a-1000*b; xl0,xl1=N_L; xr0,xr1=N_R
    ya=(xr0-a)/b; yb=(xl1-al)/b                                    # Schnittpunkte Diagonale/Stamm (rechts bzw. links)
    L=lambda p,q:np.array([p,np.add(p,np.subtract(q,p)/3.0),np.add(p,2*np.subtract(q,p)/3.0),q],float)
    def flare(x_mid,A,y_end,y_mid,sgn):             # Auslaufkante x = x_mid + sgn*A*(1-u)³, u=0 am Ende (y_end) … 1 an der Stelle y_mid; exakt kubisch
        ys=[y_end+(y_mid-y_end)*k/3.0 for k in range(4)]; off=[A,0.0,0.0,0.0]
        return np.array([[x_mid+sgn*o,y] for o,y in zip(off,ys)],float)
    AU=AUSLAUF
    out=[]
    out.append(_dent_kante(xl0,a,True))                                            # Kopf links (Spitze), Delle wie beim I
    out.append(L((a,0.0),(xr0,ya)))                                                # obere Diagonalkante
    out.append(L((xr0,ya),(xr0,AU)))                                               # rechter Stamm, linke Kante (gerade)
    out.append(flare(xr0,N_AUSSTELLUNG_R_OBEN[0],0.0,AU,-1)[::-1])                 # … Auslauf nach oben (nach links ausgestellt)
    out.append(_dent_kante(xr0-N_AUSSTELLUNG_R_OBEN[0],xr1+N_AUSSTELLUNG_R_OBEN[1],True))   # Kopf rechts, Delle wie beim I
    out.append(flare(xr1,N_AUSSTELLUNG_R_OBEN[1],0.0,AU,+1))                       # rechte Kante: Auslauf oben …
    out.append(L((xr1,AU),(xr1,1000.0)))                                           # … gerade bis unten
    out.append(_dent_kante(al+b*1000.0,xr1,False)[::-1])                           # Fuß rechts (Spitze), Delle gedreht
    out.append(L((al+b*1000.0,1000.0),(xl1,yb)))                                   # untere Diagonalkante
    out.append(L((xl1,yb),(xl1,1000.0)))                                           # linker Stamm, rechte Kante
    out.append(_dent_kante(xl0-N_AUSSTELLUNG_L_UNTEN,xl1,False)[::-1])             # Fuß links, Delle gedreht
    out.append(flare(xl0,N_AUSSTELLUNG_L_UNTEN,1000.0,1000.0-AU,-1))               # linke Kante: Auslauf unten …
    out.append(L((xl0,1000.0-AU),(xl0,0.0)))                                       # … gerade bis oben
    # Delle-Kanten behalten ihre Endpunkte (Ecke links tiefer als rechts, wie beim I); die angrenzenden Kanten rücken dorthin
    dent=[bool(len(o)==4 and o[0][1] not in (0.0,1000.0) or False) for o in out]
    dent=[k in (0,4,7,10) for k in range(len(out))]
    gerade=[k not in (3,5,11) and k not in (0,4,7,10) for k in range(len(out))]       # Linienstücke (Auslaufkurven sind 3,5,11 → nur Endpunkt verschieben)
    n=len(out)
    for k in range(n):
        a,b=out[k],out[(k+1)%n]; d=a[3]-b[0]
        if np.linalg.norm(d)<1e-9: continue
        if dent[k]: b[0]=a[3]; b[1]=b[1]+(-d)
        else:       a[3]=b[0]; a[2]=a[2]+d
    for k in range(n):
        if gerade[k]: p,q=out[k][0],out[k][3]; out[k]=np.array([p,p+(q-p)/3,p+2*(q-p)/3,q])
    return [out],-1.8
