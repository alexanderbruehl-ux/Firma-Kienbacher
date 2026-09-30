"""Hochtöner-Feld mit Signet-M als zentralem Durchbruch + Sonnenblumen-Löcher außen.
Offene Fläche per Rasterung, Stege per Abstandskarte."""
import numpy as np, math, sys
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
import os; _H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.join(_H,'..','..','03_konzepte','logo')); sys.path.insert(0,_H); import mwlogo; import lochmuster_opt as opt2c
D=46.2; R=D/2-1.2; RES=0.02; N=int(D/RES)+20; C=N//2; W=0.8; ANG=math.radians(3.711)
def signet_poly(width,cx=0.0,cy=0.0,ang=ANG):
    bx0,by0,bx1,by1=mwlogo.BBOX_SIG; k=width/(bx1-bx0); mx,my=(bx0+bx1)/2,(by0+by1)/2
    out=[]
    for u,v in mwlogo.SIGNET[0]:
        dx,dy=(u-mx)*k,-(v-my)*k
        out.append((cx+dx*math.cos(ang)-dy*math.sin(ang), cy+dx*math.sin(ang)+dy*math.cos(ang)))
    return out
def P(x,y): return (C+x/RES, C-y/RES)
def build(mw):
    im=Image.new('L',(N,N),0); d=ImageDraw.Draw(im)
    M=signet_poly(mw); d.polygon([P(*p) for p in M],fill=255)
    # Abstand jedes Punkts zum M (für Lochfreistellung)
    mm=np.asarray(im)>0; distM=ndimage.distance_transform_edt(~mm)*RES
    opt2c.WMIN=W
    pts=opt2c.best_phyllo(0,0,R,lambda t:2.0 if t<0.75 else 2.5)
    kept=[]
    for x,y,dd in pts:
        X,Y=P(x,y); X,Y=int(X),int(Y)
        if distM[Y,X] >= dd/2+W: kept.append((x,y,dd))
    for x,y,dd in kept:
        X,Y=P(x,y); r=dd/2/RES; d.ellipse([X-r,Y-r,X+r,Y+r],fill=255)
    yy,xx=np.mgrid[0:N,0:N]; field=((xx-C)**2+(yy-C)**2)<=(D/2/RES)**2
    a=np.asarray(im)>0; openp=a[field].mean()*100
    mat=(~a)&(((xx-C)**2+(yy-C)**2)<=((D/2-0.3)/RES)**2); dist=ndimage.distance_transform_edt(mat)*RES
    ridge=(dist==ndimage.maximum_filter(dist,size=int(0.3/RES)))&(dist>0.05)
    web=np.percentile(2*dist[ridge],0.5)
    # schmalste Stelle im M (Strichstärke)
    dM=ndimage.distance_transform_edt(mm)*RES; rM=(dM==ndimage.maximum_filter(dM,size=int(0.3/RES)))&(dM>0.05)
    stroke=np.percentile(2*dM[rM],2)
    return im,openp,web,stroke,len(kept),M
if __name__=='__main__':
    res=[]
    for mw in (16.0,20.0,24.0):
        im,o,w,s,n,M=build(mw); res.append((mw,im,o,w,s,n))
        print(f"M-Breite {mw:4.1f} mm (Höhe {mw*(mwlogo.BBOX_SIG[3]-mwlogo.BBOX_SIG[1])/(mwlogo.BBOX_SIG[2]-mwlogo.BBOX_SIG[0]):.1f}): {o:4.1f} % offen, Steg min {w:.2f} mm, M-Strich min {s:.2f} mm, {n} Löcher")
    F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',26); Fs=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',20)
    tiles=[]
    for mw,im,o,w,s,n in res:
        t=Image.new('RGB',(620,700),(236,238,242)); a=im.resize((560,560),Image.LANCZOS)
        disk=Image.new('RGB',(560,560),(214,217,222)); disk.paste(Image.new('RGB',(560,560),(18,19,23)),(0,0),a)
        mask=Image.new('L',(560,560),0); ImageDraw.Draw(mask).ellipse([0,0,559,559],fill=255)
        t.paste(disk,(30,20),mask); dr=ImageDraw.Draw(t); dr.ellipse([30,20,589,579],outline=(250,250,252),width=5)
        dr.text((20,600),f"M {mw:.0f} mm breit  ·  {o:.1f} % offen",font=F,fill=(20,20,20))
        dr.text((20,640),f"Steg ≥ {w:.2f} mm · M-Strich ≥ {s:.2f} mm · {n} Löcher",font=Fs,fill=(60,60,60))
        tiles.append(t)
    out=Image.new('RGB',(620*len(tiles),700),'white')
    for i,t in enumerate(tiles): out.paste(t,(620*i,0))
    out.save('HT_M_Varianten.jpg',quality=90)
