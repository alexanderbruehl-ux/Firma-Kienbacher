"""2C+ 'Strahlenkranz optimiert': maximaler offener Querschnitt bei Mindeststeg WMIN, nur Bohr-Ø aus DIAMS + Langloch-Fräser Ø SLOTW."""
import math, numpy as np
from scipy.spatial import cKDTree
GOLD=math.radians(137.50776); DIAMS=[1.0,1.5,2.0,2.5]; WMIN=0.8; SLOTW=2.0; EDGE=1.2
def qd(d): return min(DIAMS,key=lambda v:abs(v-d))
def phyllo(cx,cy,R,size,c):
    pts=[]; i=1
    while True:
        r=c*math.sqrt(i)
        if r>R: break
        d=size(r/R)
        if r+d/2<=R: a=i*GOLD; pts.append((cx+r*math.cos(a),cy+r*math.sin(a),d))
        i+=1
    return pts
def minweb(pts):
    a=np.array(pts); t=cKDTree(a[:,:2]); dd,ii=t.query(a[:,:2],k=2); return (dd[:,1]-(a[:,2]+a[ii[:,1],2])/2).min()
def best_phyllo(cx,cy,R,size):
    lo,hi=0.5,4.0
    for _ in range(40):
        c=(lo+hi)/2
        if minweb(phyllo(cx,cy,R,size,c))>=WMIN: hi=c
        else: lo=c
    return phyllo(cx,cy,R,size,hi)
def corona(cx,cy,r0,R):
    """Langloch-Kranz: lange Schlitze r0..R, dazwischen kurze Schlitze ab dem Radius, wo der Steg reicht."""
    n=int(2*math.pi*(r0+SLOTW/2)/(SLOTW+WMIN)); slots=[]
    r1=(SLOTW+WMIN)*2*n/(2*math.pi)+SLOTW/2      # ab hier passt ein Zwischenschlitz
    for i in range(n):
        a=2*math.pi*i/n; slots.append((cx,cy,a,r0+SLOTW/2,R-SLOTW/2))
        if r1<R-SLOTW/2-3: slots.append((cx,cy,a+math.pi/n,r1,R-SLOTW/2))
    return slots
def field(cx,cy,D):
    R=D/2-EDGE
    if D<60:   # Hochtöner: Spirale innen Ø2,0 + Strahlenkranz (38 % offen, bester Wert)
        Ri=R*0.45; holes=best_phyllo(cx,cy,Ri,lambda t:2.0); slots=corona(cx,cy,Ri+WMIN,R)
    else:
        Ri=R*0.52
        holes=best_phyllo(cx,cy,Ri,lambda t:qd(1.5+1.0*t)); slots=corona(cx,cy,Ri+WMIN,R)
    return holes,slots
def open_area(holes,slots):
    return sum(math.pi*d*d/4 for *_,d in holes)+sum((r1-r0)*SLOTW+math.pi*SLOTW**2/4 for *_,r0,r1 in slots)
if __name__=='__main__':
    tot=0;A=0
    for (x,y,D),nm in zip([(376.4,151.0,46.2),(286.1,120.7,118.2),(136.5,92.5,156.2)],['Hochtöner','Tiefmitteltöner','Subwoofer']):
        h,s=field(x,y,D); o=open_area(h,s); Af=math.pi*(D/2)**2
        mw=minweb(h) if h else 0
        print(f"{nm:16s} {o/Af*100:5.1f} % offen  ({len(h)} Bohrungen Ø{sorted(set(d for *_,d in h))}, {len(s)} Langlöcher)  Steg min {mw:.2f} mm")
        tot+=o;A+=Af
    print(f"gesamt {tot/A*100:.1f} %")
