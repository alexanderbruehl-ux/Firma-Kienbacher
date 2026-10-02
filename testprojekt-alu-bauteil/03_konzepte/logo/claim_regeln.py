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
