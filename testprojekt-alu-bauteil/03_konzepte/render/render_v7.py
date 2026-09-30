import numpy as np, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
DX=11.4; G=2.0; OV=17.5
C=np.array([(0,0),(369.1,23.9),(438.7,209.4),(93.8,207.0)])+[DX,0]          # Blende CAD Vorderseite
DK=np.array([(-17.8,2.4),(373.8,27.7),(440.6,205.9),(-17.4,202.7)])+[DX,0]  # Korpus
holes=[(376.4+DX,151.0,46.2),(286.1+DX,120.7,118.2),(136.5+DX,92.5,156.2)]
def off(a,b,g,ref):
    d=b-a; n=np.array([-d[1],d[0]]); n/=np.linalg.norm(n)
    if np.dot(n,ref-a)>0: n=-n
    return a+n*g,d
def X(l1,l2):
    (p1,d1),(p2,d2)=l1,l2; t=np.linalg.solve(np.array([d1,-d2]).T,p2-p1); return p1+t[0]*d1
ctr=C.mean(0)
Lb=off(C[0],C[1],G,ctr); Lt=off(C[3],C[2],G,ctr); Ll=off(C[0],C[3],G,ctr)
# rechte Blendenkante: Korpus rechts + 17,5
dr=DK[2]-DK[1]; n=np.array([dr[1],-dr[0]]); n/=np.linalg.norm(n); Rr=(DK[1]+n*OV,dr)
BLD=[X(Lb and (C[0],C[1]-C[0]),(C[0],C[3]-C[0])), X((C[0],C[1]-C[0]),Rr), X((C[3],C[2]-C[3]),Rr), C[3]]
# Foto: Innenkante Einfassung (BL,BR,TR,TL); Maßstab der bestätigten Montage für die rechte Seite
s1=165/215; x0=(237.5+3*s1)-93.8*s1; y0=421.5-3*s1
inv=lambda p:np.array([(p[0]-x0)/s1,(y0-p[1])/s1])
PBL,PBR,PTR,PTL=[np.array(p,float) for p in [(182.3,421.5),(740.5,404),(832,253.5),(232.9,256.5)]]
tBL=X(Lb,Ll); tTL=X(Lt,Ll)
def onto(line,p):   # Punkt p (mm) senkrecht auf Linie projizieren
    a,d=line; d=d/np.linalg.norm(d); return a+d*np.dot(p-a,d)
tBR=onto(Lb,inv(PBR)); tTR=onto(Lt,inv(PTR))
def homog(s,d):
    A=[];b=[]
    for (x,y),(u,v) in zip(s,d): A+=[[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]]; b+=[u,v]
    return np.append(np.linalg.solve(np.array(A,float),np.array(b,float)),1).reshape(3,3)
K=2.4; ox,oy=-60,-40   # Ausgabe: K px/mm, Ursprung
W,H=int((910-ox)*K),int((255-oy)*K)
toPix=lambda p:((p[0]-ox)*K, H-(p[1]-oy)*K)
Hd=homog([toPix(p) for p in (tBL,tBR,tTR,tTL)],[PBL,PBR,PTR,PTL])   # Ausgabepixel -> Fotopixel
photo=Image.open('/home/user/privat-meisterwerke/Projekte/Schwalbennester Alassio/Referenzbilder/03-Schwalbennest.jpeg').convert('RGB')
base=photo.transform((W,H),Image.PERSPECTIVE,tuple(Hd.flatten()[:8]),Image.BICUBIC)
from PIL import ImageEnhance
_a=np.asarray(base).astype(float)/255.0
_a=np.clip(_a**0.55*1.08,0,1)                       # Gamma aufhellen (Schatten stärker als Lichter)
base=Image.fromarray((_a*255).astype('uint8'))
base=ImageEnhance.Contrast(base).enhance(1.12); base=ImageEnhance.Color(base).enhance(1.15)
FB=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',int(8*K))
F2=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',30)
Fs=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',24)
def dashed(d,pts,col,w=3,step=18):
    for i in range(len(pts)):
        a=np.array(pts[i]);b=np.array(pts[(i+1)%len(pts)]);L=np.linalg.norm(b-a);u=(b-a)/L
        for t in np.arange(0,L,step): d.line([tuple(a+u*t),tuple(a+u*min(t+step/2,L))],fill=col,width=w)
def render(var):
    im=base.copy(); poly=[toPix(p) for p in BLD]
    sh=Image.new('L',im.size,0); ImageDraw.Draw(sh).polygon(poly,fill=255)
    sh=ImageChops.offset(sh.filter(ImageFilter.GaussianBlur(10)),-7,10); im.paste(Image.new('RGB',im.size,(4,6,12)),(0,0),sh.point(lambda v:int(v*.6)))
    d=ImageDraw.Draw(im,'RGBA')
    circ=lambda cx,cy,r:[toPix((cx-r,cy+r)),toPix((cx+r,cy-r))]
    if var==1:
        d.polygon(poly,fill=(26,36,66))
        for cx,cy,D in holes: d.ellipse(circ(cx,cy,D/2),fill=(10,10,12),outline=(70,72,80),width=2)
        d.text(toPix((215+DX,24)),"MEISTERWERKE",font=FB,fill=(44,56,92),anchor='ms')
        d.line([poly[1],poly[2]],fill=(228,230,234),width=int(3*K)); d.line([poly[1],poly[2]],fill=(255,255,255),width=2)
    else:
        d.polygon(poly,fill=(176,180,185))
        for cx,cy,D in holes:
            R=D/2; pitch=5.2 if D>60 else 3.6
            for j,yy in enumerate(np.arange(cy-R,cy+R,pitch*.866)):
                for xx in np.arange(cx-R+(pitch/2 if j%2 else 0),cx+R,pitch):
                    r=math.hypot(xx-cx,yy-cy)
                    if r<R-2:
                        dh=((1.4+1.4*r/R) if D>60 else 1.3)/2; d.ellipse(circ(xx,yy,dh),fill=(20,22,28))
            d.ellipse(circ(cx,cy,R+1.5),outline=(240,242,245),width=2)
        d.text(toPix((215+DX,24)),"MEISTERWERKE",font=FB,fill=(110,225,240),anchor='ms')
        d.polygon(poly,outline=(248,249,251),width=3)
    dashed(d,[toPix(p) for p in DK],(255,210,0))
    a=toPix(DK[0]*0+[DK[0][0],60]); d.line([a,(a[0]+40,a[1]+170)],fill=(255,210,0),width=2); d.text((a[0]-60,a[1]+174),"Korpus (gelb gestrichelt), links im Hinterschnitt",font=Fs,fill=(255,230,120),stroke_width=3,stroke_fill=(0,0,0))
    b=np.mean([poly[1],poly[2]],axis=0); d.line([tuple(b),(b[0]+80,b[1]+215)],fill=(255,210,0),width=2); d.text((b[0]+20,b[1]+220),"Überstand 17,5 mm → „fliegende“ Kante",font=Fs,fill=(255,230,120),stroke_width=3,stroke_fill=(0,0,0))
    d.text(toPix((560+DX,110)),"offenes Staufach",font=Fs,fill=(255,230,120),stroke_width=3,stroke_fill=(0,0,0))
    return im
outs=[render(1),render(2)]
titles=["Variante 1 – Leder, LS-Gitter, geprägtes Logo, Edelstahl-Abschlussleiste","Variante 2 – Alu gefräst, Perforation, eingefrästes Logo (LED)"]
o=Image.new('RGB',(W,H*2+8),'white')
for i,im in enumerate(outs):
    d=ImageDraw.Draw(im); d.rectangle([0,0,W,46],fill=(0,0,0)); d.text((14,8),titles[i]+"  ·  CAD-Kontur, Foto entzerrt, Spalt 2 mm",font=F2,fill='white'); o.paste(im,(0,i*(H+8)))
o.save('Einbau_Schwalbennest_Varianten_v7.jpg',quality=88)
print('Blende (mm):',np.round(np.array(BLD)-[DX,0],1).tolist())
