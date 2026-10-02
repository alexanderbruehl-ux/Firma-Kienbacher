"""Konturen aus einem Rasterfeld: Ecken erkennen, dazwischen glätten und mit wenigen kubischen Béziers anpassen (Schneider-Verfahren)."""
import numpy as np
from skimage import measure
from scipy.ndimage import gaussian_filter1d

def _resample(P,ds):
    d=np.r_[0,np.cumsum(np.hypot(*np.diff(P,axis=0).T))]; L=d[-1]; n=max(int(L/ds),8); t=np.linspace(0,L,n,endpoint=False)
    return np.c_[np.interp(t,d,P[:,0]),np.interp(t,d,P[:,1])],L
def _smooth_closed(P,sig_px,ds): s=sig_px/ds; return np.c_[gaussian_filter1d(P[:,0],s,mode='wrap'),gaussian_filter1d(P[:,1],s,mode='wrap')]
def find_corners(P,ds,sig=0.35,win=1.1,thr=38,minsep=1.6):
    S=_smooth_closed(P,sig,ds); T=np.gradient(S,axis=0); ang=np.unwrap(np.arctan2(T[:,1],T[:,0])); n=len(P); w=max(int(win/ds),1)
    ang_c=np.r_[ang,ang+ (ang[-1]-ang[0]) if False else ang]
    # Richtungsänderung über Fenster (zyklisch)
    a=np.arctan2(T[:,1],T[:,0]); turn=np.zeros(n)
    for i in range(n):
        a0=a[(i-w)%n]; a1=a[(i+w)%n]; d=(a1-a0+np.pi)%(2*np.pi)-np.pi; turn[i]=np.degrees(d)
    corners=[]; absT=np.abs(turn)
    cand=[i for i in range(n) if absT[i]>=thr and absT[i]>=absT[(i-1)%n] and absT[i]>=absT[(i+1)%n]]
    cand.sort(key=lambda i:-absT[i]); sep=int(minsep/ds)
    for i in cand:
        if all(min(abs(i-j),n-abs(i-j))>=sep for j in corners): corners.append(i)
    return sorted(corners)
# ---- Schneider (Graphics Gems) ----
def _bez(c,t):
    mt=1-t; return (mt**3)[:,None]*c[0]+(3*mt*mt*t)[:,None]*c[1]+(3*mt*t*t)[:,None]*c[2]+(t**3)[:,None]*c[3]
def _bez1(c,t): return 3*((1-t)**2)[:,None]*(c[1]-c[0])+6*((1-t)*t)[:,None]*(c[2]-c[1])+3*(t*t)[:,None]*(c[3]-c[2])
def _bez2(c,t): return 6*(1-t)[:,None]*(c[2]-2*c[1]+c[0])+6*t[:,None]*(c[3]-2*c[2]+c[1])
def _chord(P): d=np.r_[0,np.cumsum(np.hypot(*np.diff(P,axis=0).T))]; return d/d[-1]
def _gen(P,u,t1,t2):
    c=np.array([P[0],None,None,P[-1]],dtype=object); b0=(1-u)**3;b1=3*u*(1-u)**2;b2=3*u*u*(1-u);b3=u**3
    A1=b1[:,None]*t1; A2=b2[:,None]*t2; C=np.array([[ (A1*A1).sum(),(A1*A2).sum()],[(A1*A2).sum(),(A2*A2).sum()]])
    tmp=P-(b0+b1)[:,None]*P[0]-(b2+b3)[:,None]*P[-1]; X=np.array([(A1*tmp).sum(),(A2*tmp).sum()])
    det=C[0,0]*C[1,1]-C[0,1]*C[1,0]; seg=np.hypot(*(P[-1]-P[0]))
    if abs(det)>1e-12: al=(X[0]*C[1,1]-X[1]*C[0,1])/det; ar=(C[0,0]*X[1]-C[1,0]*X[0])/det
    else: al=ar=0
    eps=1e-6*seg
    if al<eps or ar<eps: al=ar=seg/3
    return np.array([P[0],P[0]+t1*al,P[-1]+t2*ar,P[-1]])
def _reparam(c,P,u):
    d=_bez(c,u)-P; d1=_bez1(c,u); d2=_bez2(c,u); num=(d*d1).sum(1); den=(d1*d1).sum(1)+(d*d2).sum(1)
    return np.clip(np.where(abs(den)>1e-12,u-num/den,u),0,1)
def _fit(P,t1,t2,err):
    if len(P)==2: d=np.hypot(*(P[1]-P[0]))/3; return [np.array([P[0],P[0]+t1*d,P[1]+t2*d,P[1]])]
    u=_chord(P); c=_gen(P,u,t1,t2)
    for _ in range(6):
        e=((_bez(c,u)-P)**2).sum(1); m=e.max()
        if m<err: return [c]
        u=_reparam(c,P,u); c=_gen(P,u,t1,t2)
    e=((_bez(c,u)-P)**2).sum(1); m=e.max(); i=int(np.argmax(e)); i=min(max(i,1),len(P)-2)
    if m<err*4 and False: return [c]
    tc=P[i-1]-P[i+1]; tc=tc/np.hypot(*tc)
    return _fit(P[:i+1],t1,tc,err)+_fit(P[i:],-tc,t2,err)
def _unit(v): n=np.hypot(*v); return v/n if n>0 else v
def fit_open(P,err,k=3):
    t1=_unit(P[min(k,len(P)-1)]-P[0]); t2=_unit(P[max(len(P)-1-k,0)]-P[-1]); return _fit(P,t1,t2,err)
def _line(pts):
    c=pts.mean(0); u,sv,vt=np.linalg.svd(pts-c); return c,vt[0]
def contour_to_beziers(P,ds=0.1,sig=0.8,err=0.012,corner_kw={},edge=0.9,span=(0.7,2.2),line_tol=0.6):
    """P: geschlossene Kontur (N,2) in px. Ecken = Schnittpunkt der Geraden der beiden angrenzenden Kanten; dazwischen geglättete Kontur,
    angepasst mit wenigen Béziers. Rückgabe: Liste kubischer Béziers (4x2), Eckpunkte."""
    R,L=_resample(P,ds); n=len(R); cor=find_corners(R,ds,**corner_kw); S=_smooth_closed(R,sig,ds)
    sharp=bool(cor)
    if not cor: cor=[0,n//4,n//2,3*n//4]
    o1,o2,eg=int(span[0]/ds),int(span[1]/ds),int(edge/ds)
    pin={};tin={};tout={}
    for i in cor:
        if sharp:
            li=S[[(i-k)%n for k in range(o1,o2+1)]]; ri=S[[(i+k)%n for k in range(o1,o2+1)]]
            c1,d1=_line(li); c2,d2=_line(ri)
            if np.dot(d1,S[i]-S[(i-o2)%n])<0: d1=-d1            # Laufrichtung in die Ecke hinein
            if np.dot(d2,S[(i+o2)%n]-S[i])<0: d2=-d2            # Laufrichtung aus der Ecke heraus
            A=np.array([d1,-d2]).T; p=R[i]
            if abs(np.linalg.det(A))>0.15:
                st=np.linalg.solve(A,c2-c1); q=c1+st[0]*d1
                if np.hypot(*(q-R[i]))<1.5: p=q
            pin[i]=p; tin[i]=d1; tout[i]=d2
        else:
            pin[i]=S[i]; tout[i]=_unit(S[(i+3)%n]-S[(i-3)%n]); tin[i]=tout[i]
    out=[]
    for a,b in zip(cor,cor[1:]+[cor[0]+n]):
        ea=eg if sharp else 0; idx=np.arange(a+ea,b-ea+1)%n if b-ea>a+ea else np.array([],int)
        seg=np.vstack([pin[a],S[idx],pin[b%n]]) if len(idx) else np.vstack([pin[a],pin[b%n]])
        p0,p1=seg[0],seg[-1]; ch=p1-p0; Lc=np.hypot(*ch)
        if sharp and Lc>2.0 and len(seg)>3 and np.abs(np.cross(ch/Lc,seg-p0)).max()<=line_tol:       # nahezu gerade Kante -> echte Gerade
            out.append(np.array([p0,p0+ch/3,p0+2*ch/3,p1])); continue
        out+=_fit(seg,tout[a],-tin[b%n],err)
    return out,[pin[i] for i in cor]
def field_to_beziers(av,UP,level=0.5,**kw):
    res=[]
    for c in measure.find_contours(np.pad(av,2),level):
        c=c-2; 
        if np.hypot(*(c[0]-c[-1]))>1e-6: continue
        P=np.c_[c[:,1],c[:,0]]/UP
        if len(P)<12*UP//8: continue
        res.append(contour_to_beziers(P[:-1],**kw)[0])
    return res
