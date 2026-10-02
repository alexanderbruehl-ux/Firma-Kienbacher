"""Meisterwerke-Logo aus der Original-Reinzeichnung (Vektor, DWG) -> mw_trace.json + SVGs + Vorschau.
    pip install ezdwg ezdxf matplotlib
    python3 logo_aus_dwg.py [original/meisterwerke_logo_RZ_ohne_claim_pfad.dwg]
Die DWG (AutoCAD R14) enthält Signet + Wortmarke als gefüllte Flächen (HATCH, 16 Konturen) und dieselben Umrisse noch einmal
als Splines. Die Splines werden von ezdwg beim Lesen teils falsch dekodiert (feine Striche) -> es werden nur die HATCH-Konturen
verwendet. Einheit: Zeichnungseinheiten der DWG (Gesamtbreite 453,46), y nach unten (wie bisher in mw_trace.json)."""
import ezdwg, ezdxf, json, os, sys, tempfile, numpy as np
from ezdxf.math import bulge_to_arc
HERE=os.path.dirname(os.path.abspath(__file__))
SRC=sys.argv[1] if len(sys.argv)>1 else os.path.join(HERE,'original','meisterwerke_logo_RZ_ohne_claim_pfad.dwg')
tmp=os.path.join(tempfile.mkdtemp(),'logo.dxf'); ezdwg.to_dxf(SRC,tmp); doc=ezdxf.readfile(tmp)
ins=[e for e in doc.modelspace() if e.dxftype()=='INSERT'][0]
assert tuple(ins.dxf.insert)==(0,0,0) and ins.dxf.xscale==ins.dxf.yscale==1 and ins.dxf.rotation==0, 'INSERT mit Transformation - nicht unterstützt'
def pts(p):
    v=list(p.vertices); n=len(v); out=[]
    for i in range(n):
        x,y,b=(v[i][0],v[i][1],(v[i][2] if len(v[i])>2 else 0))
        out.append((x,y))
        if b and (i<n-1 or p.is_closed):
            x2,y2=v[(i+1)%n][:2]; c,sa,ea,r=bulge_to_arc((x,y),(x2,y2),b)
            if b<0: sa,ea=ea,sa
            if ea<sa: ea+=2*np.pi
            seg=[(c[0]+r*np.cos(a),c[1]+r*np.sin(a)) for a in np.linspace(sa,ea,24)[1:-1]]; out+=seg if b>0 else seg[::-1]
    out=[q for i,q in enumerate(out) if i==0 or np.hypot(q[0]-out[i-1][0],q[1]-out[i-1][1])>1e-6]   # doppelte Punkte entfernen
    if np.hypot(out[0][0]-out[-1][0],out[0][1]-out[-1][1])<=1e-6: out.pop()                       # Schlusspunkt = Startpunkt
    return np.array(out)
paths=[pts(p) for h in doc.blocks[ins.dxf.name] if h.dxftype()=='HATCH' for p in h.paths]
paths=[np.c_[p[:,0],-p[:,1]] for p in paths]                       # y nach unten
bb=lambda P:[min(p[:,0].min() for p in P),min(p[:,1].min() for p in P),max(p[:,0].max() for p in P),max(p[:,1].max() for p in P)]
ymid=(bb(paths)[1]+bb(paths)[3])/2                                            # Signet liegt oberhalb der Bildmitte, Wortmarke darunter
sig=[p for p in paths if p[:,1].max()<ymid]; wm=[p for p in paths if p[:,1].max()>=ymid]
assert len(sig)==1 and len(wm)==len(paths)-1, (len(sig),len(wm))
d=lambda P:' '.join('M'+' L'.join(f'{x:.3f},{y:.3f}' for x,y in p)+' Z' for p in P)
dsig,dwm=d(sig),d(wm); bs,bw,ba=bb(sig),bb(wm),bb(paths)
json.dump({'signet':dsig,'wordmark':dwm,'bbox_all':ba,'bbox_signet':bs,'bbox_wordmark':bw},open(os.path.join(HERE,'mw_trace.json'),'w'))
import mwlogo
for name,kw in (('Meisterwerke_Logo.svg',{}),('Meisterwerke_Signet.svg',{'with_wordmark':False}),('Meisterwerke_Wortmarke.svg',{'with_signet':False})):
    mwlogo.svg(os.path.join(HERE,name),**kw)
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch
v=[];c=[]
for p in sig+wm: v+=list(map(tuple,p))+[tuple(p[0])]; c+=[Path.MOVETO]+[Path.LINETO]*(len(p)-1)+[Path.CLOSEPOLY]
for name,bg,fg in (('Logo_hell.png','#ffffff','#1b2a4a'),('Logo_dunkel.png','#0e1422','#f2f2f2')):
    fig=plt.figure(figsize=(20,20*(ba[3]-ba[1]+60)/(ba[2]-ba[0]+60))); ax=fig.add_axes([0,0,1,1]); fig.patch.set_facecolor(bg)
    ax.add_patch(PathPatch(Path(v,c),facecolor=fg,edgecolor='none')); ax.set_xlim(ba[0]-30,ba[2]+30); ax.set_ylim(ba[3]+30,ba[1]-30); ax.set_aspect('equal'); ax.axis('off')
    fig.savefig(os.path.join(HERE,name),dpi=100,facecolor=bg); plt.close(fig)
print('Signet-BBox',[round(x,2) for x in bs],'Wortmarke-BBox',[round(x,2) for x in bw],'Gesamt',[round(x,2) for x in ba])
