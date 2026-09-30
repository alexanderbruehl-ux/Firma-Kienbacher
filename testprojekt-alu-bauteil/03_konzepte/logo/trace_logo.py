"""Vektorisiert das Meisterwerke-Logo aus der Bilddatei (keine Fremdschrift).
Ablauf: 8x hochskalieren (bikubisch) -> leicht glätten -> Schwelle auf halber Kantenhöhe ->
Sterne/Kleinstflecken entfernen -> Potrace (Bezierkurven) -> SVG (Signet und Wortmarke getrennt)."""
import numpy as np, sys
from PIL import Image, ImageFilter
from skimage import measure
import potrace
SRC=sys.argv[1] if len(sys.argv)>1 else 'LOGO MW.jpg'
UP=8
g=Image.open(SRC).convert('L')
W0,H0=g.size
big=g.resize((W0*UP,H0*UP),Image.BICUBIC).filter(ImageFilter.GaussianBlur(UP*0.5))
a=np.asarray(big).astype(float)
mask=a>100                                     # ~ halbe Kantenhöhe zwischen Hintergrund (10) und Metall (≈220)
lab=measure.label(mask,connectivity=2)
props=measure.regionprops(lab)
keep=np.zeros(lab.max()+1,bool)
for p in props:
    if p.area>=(3*UP)**2*6: keep[p.label]=True  # Sterne sind winzig
mask=keep[lab]
ys,xs=np.where(mask); print('Logo-BBox (Originalpixel):',xs.min()/UP,xs.max()/UP,ys.min()/UP,ys.max()/UP)
# Trennung Signet/Wortmarke über Zeilenlücke
rows=mask.any(1); gaps=np.where(~rows[ys.min():ys.max()])[0]+ys.min()
# größte Lücke
split=None;best=0;start=None
for y in range(ys.min(),ys.max()):
    if not rows[y]:
        if start is None: start=y
    else:
        if start is not None and y-start>best: best=y-start; split=(start+y)//2
        start=None
print('Trennlinie Signet/Wortmarke bei y=',split/UP)
def trace(m):
    bm=potrace.Bitmap(m)
    path=bm.trace(turdsize=20*UP, turnpolicy=potrace.POTRACE_TURNPOLICY_MINORITY, alphamax=1.1, opticurve=True, opttolerance=0.6)
    d=[]
    H,W=m.shape
    for curve in path:
        pts=[curve.start_point]+[sg.end_point for sg in curve.segments]
        xs=[p.x for p in pts]; ys=[p.y for p in pts]
        if max(xs)-min(xs)>0.95*W and max(ys)-min(ys)>0.95*H: continue   # Bildrahmen-Artefakt
        s=curve.start_point; d.append(f'M{s.x/UP:.3f},{s.y/UP:.3f}')
        for seg in curve.segments:
            if seg.is_corner:
                d.append(f'L{seg.c.x/UP:.3f},{seg.c.y/UP:.3f} L{seg.end_point.x/UP:.3f},{seg.end_point.y/UP:.3f}')
            else:
                d.append(f'C{seg.c1.x/UP:.3f},{seg.c1.y/UP:.3f} {seg.c2.x/UP:.3f},{seg.c2.y/UP:.3f} {seg.end_point.x/UP:.3f},{seg.end_point.y/UP:.3f}')
        d.append('Z')
    return ' '.join(d)
sig=mask.copy(); sig[split:]=False
wm=mask.copy(); wm[:split]=False
def polytrace(m,tol):
    cs=measure.find_contours(m.astype(float),0.5)
    d=[]
    for c in cs:
        if len(c)<50: continue
        ap=measure.approximate_polygon(c,tolerance=tol)
        d.append('M'+' L'.join(f'{p[1]/UP:.3f},{p[0]/UP:.3f}' for p in ap[:-1])+' Z')
        print('  Signet-Kontur: %d Ecken'%(len(ap)-1))
    return ' '.join(d)
dsig=polytrace(sig,0.9*UP); dwm=trace(wm)
def bbox(m):
    ys,xs=np.where(m); return xs.min()/UP,ys.min()/UP,(xs.max()+1)/UP,(ys.max()+1)/UP
bs,bw=bbox(sig),bbox(wm)
x0,y0=min(bs[0],bw[0]),bs[1]; x1,y1=max(bs[2],bw[2]),bw[3]
import json
json.dump({'signet':dsig,'wordmark':dwm,'bbox_all':[x0,y0,x1,y1],'bbox_signet':bs,'bbox_wordmark':bw},open('mw_trace.json','w'))
for name,parts,bb in (('Meisterwerke_Logo.svg',[dsig,dwm],(x0,y0,x1,y1)),('Meisterwerke_Signet.svg',[dsig],bs),('Meisterwerke_Wortmarke.svg',[dwm],bw)):
    p=4
    open(name,'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{bb[0]-p:.2f} {bb[1]-p:.2f} {bb[2]-bb[0]+2*p:.2f} {bb[3]-bb[1]+2*p:.2f}"><g fill="#1b2a4a" fill-rule="evenodd">'+''.join(f'<path d="{d}"/>' for d in parts)+'</g></svg>')
print('Signet-BBox',bs,'Wortmarke-BBox',bw)
