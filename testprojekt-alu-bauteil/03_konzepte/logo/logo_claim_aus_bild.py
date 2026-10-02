"""Claim „MAGNA OPERA OF INTERIOR & SOUND“ als Vektor: Buchstaben aus der Rasterdatei rekonstruiert, M aus dem Meisterwerke-Schriftzug, Neusatz.
    pip install pillow numpy scipy scikit-image matplotlib
    python3 logo_claim_aus_bild.py
Quelle: original/meisterwerke_logo_mit_claim_RASTER.gif (1733 x 864 px, nur Tinte/transparent, Claim-Höhe 42 px) mit dem ALTEN Claim
„OPUS MAGNA OF INTERIOR & SOUND“. Richtig ist „MAGNA OPERA …“ (Plural von „magnum opus“; „opus magna“ ist grammatisch falsch).
Alle Buchstaben des neuen Claims kommen im alten vor. Pro Buchstabe: mehrfach vorkommende Exemplare werden auf Teilpixel genau übereinandergelegt und
gemittelt, die Kontur wird geglättet, Ecken werden aus den Schnittpunkten der angrenzenden Kanten bestimmt, dazwischen wenige kubische Béziers (curvefit.py).
Das M stammt direkt aus dem Vektor-Schriftzug (mw_trace.json, Original-DWG), auf Claim-Höhe skaliert.
Neusatz: Buchstabenabstand des GIF (Modell Lücke(i,j)=a_i+b_j, Wortabstand = Mittel der Wortlücken), mittig zum Schriftzug.
ACHTUNG: Rekonstruktion aus einem 42-px-Raster (außer M) - nur Näherung, nicht für Fertigungsdaten. Dafür die Original-Vektordatei MIT richtigem Claim beschaffen.
mw_trace.json: nur 'claim', 'bbox_claim', 'claim_text' kommen hinzu; Signet und Schriftzug bleiben unverändert."""
import json, os, sys, numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, shift as nd_shift
from scipy.signal import fftconvolve
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import curvefit, mwlogo
HERE=os.path.dirname(os.path.abspath(__file__)); SRC=os.path.join(HERE,'original','meisterwerke_logo_mit_claim_RASTER.gif')
ALT='OPUS MAGNA OF INTERIOR & SOUND'; NEU='MAGNA OPERA OF INTERIOR & SOUND'
FIELD_SIGMA=0.7; FIT=dict(sig=1.3,err=0.03)                                      # Glättung der Rasterkante / der Kontur (px), Anpassungsfehler (px^2)
T=json.load(open(os.path.join(HERE,'mw_trace.json')))
ink=np.asarray(Image.open(SRC).convert('RGBA'))[...,3]>128
rows=np.where(ink.any(1))[0]; blocks=np.split(rows,np.where(np.diff(rows)>20)[0]+1); assert len(blocks)==3
wm_r,cl_r=blocks[1],blocks[2]; wx=np.where(ink[wm_r[0]:wm_r[-1]+1].any(0))[0]
wm_x0=wx[0]; wm_w=wx[-1]-wx[0]+1; wm_bottom=wm_r[-1]+1; wm_cx=wm_x0+wm_w/2                      # Pixelkanten
bw=T['bbox_wordmark']; s=(bw[2]-bw[0])/wm_w                                                      # Einheiten je GIF-Pixel
y0,y1=cl_r[0],cl_r[-1]+1; xs=np.where(ink[y0:y1].any(0))[0]
seg=[(r[0],r[-1]+1) for r in np.split(xs,np.where(np.diff(xs)>1)[0]+1)]
letters=[c for c in ALT if c!=' ']; assert len(seg)==len(letters), (len(seg),len(letters))
UP=8; M=4
def inst_field(a,b,W,H):
    m=np.zeros((H,W),bool); sub=ink[y0-M:y1+M,a-M:b+M]; m[:sub.shape[0],:sub.shape[1]]=sub
    m[:,:M]=False; m[:,M+(b-a):]=False                                           # Nachbarbuchstaben ausblenden
    big=np.asarray(Image.fromarray(m.astype('uint8')*255).resize((W*UP,H*UP),Image.BICUBIC)).astype(float)/255
    return gaussian_filter(big,FIELD_SIGMA*UP)
def avg_field(segs):
    Wc=max(b-a for a,b in segs)+2*M+2; Hc=(y1-y0)+2*M
    fields=[inst_field(a,b,Wc,Hc) for a,b in segs]; ref=fields[0]; acc=[ref]
    for f in fields[1:]:                                                          # Teilpixel-Ausrichtung per Kreuzkorrelation
        c=fftconvolve(ref-ref.mean(),(f-f.mean())[::-1,::-1],mode='same'); yy,xx=np.indices(c.shape); yy-=c.shape[0]//2; xx-=c.shape[1]//2
        c=np.where((abs(yy)<=0.5*UP)&(abs(xx)<=2.5*UP),c,-np.inf)                # gleiche Grundlinie: senkrecht +-0,5 px, waagerecht +-2,5 px
        cy,cx=np.unravel_index(np.argmax(c),c.shape); acc.append(nd_shift(f,(cy-c.shape[0]//2,cx-c.shape[1]//2),order=1,mode='constant'))
    return np.mean(acc,axis=0)
def trace_char(segs):
    out=[]
    for cont in curvefit.field_to_beziers(avg_field(segs),UP,**FIT):
        P=lambda p:(p[0]-M,p[1]-M+y0)                                             # x relativ zur linken Glyphenkante (px), y absolut
        d=[('M',P(cont[0][0]))]+[('C',P(c[1]),P(c[2]),P(c[3])) for c in cont]; out.append(d)
    return out
def wordmark_M():
    """M aus dem Vektor-Schriftzug (linkeste Außenkontur), auf Claim-Kapitalhöhe skaliert (Höhe/Lage wie das M im GIF)."""
    polys=mwlogo._subpaths(T['wordmark']); polys=[np.array(p) for p in polys]; poly=min(polys,key=lambda p:p[:,0].min())
    mi=letters.index('M'); a,b=seg[mi]; ys=np.where(ink[y0:y1,a:b].any(1))[0]; top,bot=y0+ys.min(),y0+ys.max()+1       # Höhe des M im GIF
    k=(bot-top)/(poly[:,1].max()-poly[:,1].min()); pts=[((u-poly[:,0].min())*k,top+(v-poly[:,1].min())*k) for u,v in poly]
    w=(poly[:,0].max()-poly[:,0].min())*k; return w,[[('M',pts[0])]+[('L',p) for p in pts[1:]]]
glyph={}
for ch in dict.fromkeys(letters):
    segs=[sg for c,sg in zip(letters,seg) if c==ch]; glyph[ch]=(segs[0][1]-segs[0][0],trace_char(segs)); print(f'{ch}:{len(segs)}x',end=' ')
print()
rw={ch:g[0] for ch,g in glyph.items()}                                            # Rasterbreiten (für Abstandsmodell)
glyph['M']=wordmark_M(); print('M aus dem Schriftzug: Breite %.1f px (Claim-M im GIF: %d px)'%(glyph['M'][0],rw['M']))
# Buchstaben nach Regeln (claim_regeln.py) ersetzen die Pixel-Nachzeichnung; nicht fertige Buchstaben bleiben Pixel-Nachzeichnung
import claim_regeln as RG
RULE={'I':RG.letter_I,'E':RG.letter_E,'F':RG.letter_F,'T':RG.letter_T,'R':RG.letter_R,'P':RG.letter_P,'D':RG.letter_D,'N':RG.letter_N,'A':RG.letter_A,'U':RG.letter_U,'O':RG.letter_O,'S':RG.letter_S}
for _n in ('G','AMP'):
    if hasattr(RG,'letter_'+_n): RULE['&' if _n=='AMP' else _n]=getattr(RG,'letter_'+_n)
URU=1000/41                                                                       # Einheiten je GIF-Pixel (Kappenhöhe 41 px = 1000)
def rule_glyph(fn):
    res=fn(); cont,dy=res if isinstance(res,tuple) else (res,0.0)
    P=np.vstack([RG.sample(c,12) for c in cont]); xmin,xmax=P[:,0].min(),P[:,0].max()
    f=lambda p:((p[0]-xmin)/URU,y0+(p[1]+dy)/URU)                                 # x ab linker Tintenkante (px), y absolut (px)
    paths=[]
    for c in cont:
        d=[('M',f(c[0][0]))]+[('C',f(b[1]),f(b[2]),f(b[3])) for b in c]; paths.append(d)
    return (xmax-xmin)/URU,paths
for _ch,_fn in RULE.items():
    if _ch in glyph: glyph[_ch]=rule_glyph(_fn)
print('Nach Regeln: '+' '.join(RULE.keys()))
# Abstandsmodell: Lücke(i,j)=a_i+b_j, Wortlücke = Mittel
pairs=[];wg=[];prev=None;li=0
for c in ALT:
    if c==' ': prev='SPACE'; continue
    if li>0:
        gap=seg[li][0]-seg[li-1][1]
        if prev=='SPACE': wg.append(gap)
        else: pairs.append((letters[li-1],c,gap))
    prev=c; li+=1
chars=sorted(set(letters)); ci={c:i for i,c in enumerate(chars)}; n=len(chars); mean_g=np.mean([p[2] for p in pairs])
A=np.zeros((len(pairs)+2*n,2*n)); y=np.zeros(len(pairs)+2*n)
for r,(a_,b_,g_) in enumerate(pairs): A[r,ci[a_]]=1; A[r,n+ci[b_]]=1; y[r]=g_
for i in range(2*n): A[len(pairs)+i,i]=1.0; y[len(pairs)+i]=mean_g/2                # Ridge: unbeobachtete Werte -> Mittel/2
sol=np.linalg.lstsq(A,y,rcond=None)[0]; gap_of=lambda a_,b_:float(sol[ci[a_]]+sol[n+ci[b_]]); WG=float(np.mean(wg))
def layout(text,widths):
    x=0.0; res=[]; prev=None; sp=False
    for c in text:
        if c==' ': sp=True; continue
        if prev is not None: x+= WG if sp else gap_of(prev,c)
        res.append((c,x)); x+=widths[c]; prev=c; sp=False
    return res,x
res,W=layout(ALT,rw); err=[abs((x+seg[0][0])-a) for (c,x),(a,b) in zip(res,seg)]
print('Kontrolle am alten Text: Abweichung der Buchstabenpositionen zum GIF: mittel %.2f px, max %.2f px (Buchstabenhöhe 42 px)'%(np.mean(err),np.max(err)))
res,W=layout(NEU,{c:g[0] for c,g in glyph.items()}); left=wm_cx-W/2
Xu=lambda px:bw[0]+(px-wm_x0)*s; Yu=lambda py:bw[3]+(py-wm_bottom)*s
f=lambda p,ox:f'{Xu(ox+p[0]):.3f},{Yu(p[1]):.3f}'; parts=[]
for c,x in res:
    for d in glyph[c][1]:
        t=[]
        for cmd in d:
            if cmd[0] in 'ML': t.append(cmd[0]+f(cmd[1],left+x))
            else: t.append('C'+' '.join(f(p,left+x) for p in cmd[1:]))
        parts.append(' '.join(t)+' Z')
claim=' '.join(parts); nums=np.array([pt for q in mwlogo._subpaths(claim) for pt in q])      # Ausdehnung aus der gezeichneten Kontur
bc=[nums[:,0].min(),nums[:,1].min(),nums[:,0].max(),nums[:,1].max()]
T['claim']=claim; T['bbox_claim']=bc; T['claim_text']=NEU; json.dump(T,open(os.path.join(HERE,'mw_trace.json'),'w'))
print('Neuer Claim "%s": Breite %.2f = %.1f %% der Schriftzugbreite (GIF-Claim alt: 84.8 %%), Höhe %.2f, Abstand zur Schrift %.2f (GIF 17.9), mittig: Versatz %.2f'%(NEU,bc[2]-bc[0],100*(bc[2]-bc[0])/(bw[2]-bw[0]),bc[3]-bc[1],bc[1]-bw[3],(bc[0]+bc[2])/2-(bw[0]+bw[2])/2))
# ---- Ausgaben: SVG / PDF / PNG (Signet + Schriftzug wie in mw_trace.json, darunter der Claim) ----
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch
SIG=mwlogo._subpaths(T['signet']); WM=mwlogo._subpaths(T['wordmark']); CL=mwlogo._subpaths(claim)
ba=[min(T['bbox_all'][0],bc[0]),T['bbox_all'][1],max(T['bbox_all'][2],bc[2]),bc[3]]
p=4; open(os.path.join(HERE,'Meisterwerke_Logo_mit_Claim.svg'),'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{ba[0]-p:.2f} {ba[1]-p:.2f} {ba[2]-ba[0]+2*p:.2f} {ba[3]-ba[1]+2*p:.2f}"><g fill="#1b2a4a" fill-rule="evenodd">'+''.join(f'<path d="{d}"/>' for d in (T['signet'],T['wordmark'],claim))+'</g></svg>')
v=[];c=[]
for q in SIG+WM+CL: v+=list(map(tuple,q))+[tuple(q[0])]; c+=[Path.MOVETO]+[Path.LINETO]*(len(q)-1)+[Path.CLOSEPOLY]
for name,bg,fg in (('Logo_mit_Claim_hell.png','#ffffff','#1b2a4a'),('Logo_mit_Claim_dunkel.png','#0e1422','#f2f2f2')):
    fig=plt.figure(figsize=(20,20*(ba[3]-ba[1]+60)/(ba[2]-ba[0]+60))); ax=fig.add_axes([0,0,1,1]); fig.patch.set_facecolor(bg)
    ax.add_patch(PathPatch(Path(v,c),facecolor=fg,edgecolor='none')); ax.set_xlim(ba[0]-30,ba[2]+30); ax.set_ylim(ba[3]+30,ba[1]-30); ax.set_aspect('equal'); ax.axis('off')
    fig.savefig(os.path.join(HERE,name),dpi=300,facecolor=bg)
    if name.endswith('hell.png'): fig.savefig(os.path.join(HERE,'Meisterwerke_Logo_mit_Claim.pdf'),facecolor=bg)
    plt.close(fig)
print('Dateien geschrieben')
