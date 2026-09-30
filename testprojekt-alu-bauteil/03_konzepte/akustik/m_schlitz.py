"""Sonnenblume + zusätzlich ausgefrästes M (vier Schenkel als Fräsbahnen, Signet-Proportionen, 3,7° wie das Logo).
Löcher bleiben, außer sie kämen dem M näher als Steg W. Offene Fläche per Rasterung, Stege per Abstandskarte."""
import numpy as np, math
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
import sys, os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','render')); import opt2c
W=0.8; ANG=math.radians(3.711); RES=0.02
# Signet-Geometrie (gemessen, Einheiten der Vorlage): Spitzen A/B, Füße
SIG=dict(top=37.0,base=190.0,A=(680.0,746.0,812.0),B=(747.0,813.0,879.0))
def m_legs(width,cx,cy,slotw,thin=None):
    """Mittellinien der 4 Schenkel (Fräsbahnen) – Außenkontur des M = Signet-Hülle."""
    x0,x1=SIG['A'][0],SIG['B'][2]; h=SIG['base']-SIG['top']; k=(width-slotw)/(x1-x0); mx=(x0+x1)/2; my=(SIG['top']+SIG['base'])/2
    def T(u,v):
        dx,dy=(u-mx)*k,-(v-my)*k*(width/(width))  # gleiche Skalierung
        return (cx+dx*math.cos(ANG)-dy*math.sin(ang0)*0+ -dy*math.sin(ANG), cy+dx*math.sin(ANG)+dy*math.cos(ANG))
    ang0=0
    legs=[]
    tw=thin if thin else slotw
    for L,Ap,Rr in (SIG['A'],SIG['B']):
        legs.append((T(L,SIG['base']),T(Ap,SIG['top']),tw)); legs.append((T(Ap,SIG['top']),T(Rr,SIG['base']),slotw))
    return legs
def field_img(D,mwidth,slotw,law,hole_edge=1.2,thin=None):
    N=int(D/RES)+20; C=N//2; P=lambda x,y:(C+x/RES,C-y/RES)
    im=Image.new('L',(N,N),0); d=ImageDraw.Draw(im)
    def circ(x,y,r): X,Y=P(x,y); rr=r/RES; d.ellipse([X-rr,Y-rr,X+rr,Y+rr],fill=255)
    legs=m_legs(mwidth,0,0,slotw,thin) if mwidth>0 else []
    for a,b,sw in legs:
        a=np.array(a); b=np.array(b); L=np.linalg.norm(b-a)
        for t in np.arange(0,L+1e-9,RES*2): p=a+(b-a)*t/L; circ(p[0],p[1],sw/2)
    mm=np.asarray(im)>0; distM=ndimage.distance_transform_edt(~mm)*RES if legs else None
    opt2c.WMIN=W; kept=0
    for x,y,dd in opt2c.best_phyllo(0,0,D/2-hole_edge,law):
        X,Y=[int(v) for v in P(x,y)]
        if distM is None or distM[Y,X]>=dd/2+W: circ(x,y,dd/2); kept+=1
    yy,xx=np.mgrid[0:N,0:N]; f=((xx-C)**2+(yy-C)**2)<=(D/2/RES)**2; a=np.asarray(im)>0
    mat=(~a)&(((xx-C)**2+(yy-C)**2)<=((D/2-0.3)/RES)**2); dist=ndimage.distance_transform_edt(mat)*RES
    ridge=(dist==ndimage.maximum_filter(dist,size=int(0.3/RES)))&(dist>0.05)
    return im,a[f].mean()*100,np.percentile(2*dist[ridge],0.5),kept,legs
if __name__=='__main__':
    lawHT=lambda t:2.0 if t<0.75 else 2.5
    rows=[]
    for mw in (0,22,28,34):
        im,o,w,n,_=field_img(46.2,mw,2.0,lawHT); rows.append((mw,im,o,w,n))
        print(f"HT M-Breite {mw:2d} mm, Schlitz 2,0: {o:4.1f} % offen, Steg min {w:.2f} mm, {n} Löcher")
    F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',26); Fs=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',20)
    tiles=[]
    for mw,im,o,w,n in rows:
        t=Image.new('RGB',(620,700),(236,238,242)); a=im.resize((560,560),Image.LANCZOS)
        disk=Image.new('RGB',(560,560),(214,217,222)); disk.paste(Image.new('RGB',(560,560),(18,19,23)),(0,0),a)
        m=Image.new('L',(560,560),0); ImageDraw.Draw(m).ellipse([0,0,559,559],fill=255)
        t.paste(disk,(30,20),m); dr=ImageDraw.Draw(t); dr.ellipse([30,20,589,579],outline=(250,250,252),width=5)
        dr.text((20,600),("ohne M" if mw==0 else f"M {mw} mm breit")+f"  ·  {o:.1f} % offen",font=F,fill=(20,20,20))
        dr.text((20,640),f"Steg ≥ {w:.2f} mm · {n} Löcher"+("" if mw==0 else " + 4 Schlitze Ø2,0"),font=Fs,fill=(60,60,60))
        tiles.append(t)
    out=Image.new('RGB',(620*len(tiles),700),'white')
    for i,t in enumerate(tiles): out.paste(t,(620*i,0))
    out.save('HT_M_Schlitz.jpg',quality=90)
