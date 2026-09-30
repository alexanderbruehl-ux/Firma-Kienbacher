"""Hochtöner-Feld (Ø46,2): Alternativen mit offener Mitte. Offene Fläche per Rasterung (0,02 mm), Steg ≥ 0,8 mm."""
import numpy as np, math
from PIL import Image, ImageDraw
import opt2c
D=46.2; R=D/2-1.2; RES=0.02; N=int(D/RES)+20; C=N//2
GOLD=math.radians(137.50776); W=0.8
def canvas(): im=Image.new('L',(N,N),0); return im,ImageDraw.Draw(im)
def P(x,y): return (C+x/RES, C-y/RES)
def circ(d,x,y,r): X,Y=P(x,y); rr=r/RES; d.ellipse([X-rr,Y-rr,X+rr,Y+rr],fill=255)
def slot_arc(d,pts,w):
    """Fräserbahn exakt: Kreise (Ø = Schlitzbreite) dicht entlang der Bahn stempeln."""
    pts=np.array(pts); seg=np.linalg.norm(np.diff(pts,axis=0),axis=1); L=np.concatenate([[0],np.cumsum(seg)])
    for s_ in np.arange(0,L[-1]+1e-9,RES*2):
        x=np.interp(s_,L,pts[:,0]); y=np.interp(s_,L,pts[:,1]); circ(d,x,y,w/2)
def open_frac(im):
    a=np.asarray(im)>0; yy,xx=np.mgrid[0:N,0:N]; m=((xx-C)**2+(yy-C)**2)<=(D/2/RES)**2
    return a[m].mean()*100
res={}
# V0: Sonnenblume 2A-35 (Referenz)
im,d=canvas(); opt2c.WMIN=W
for x,y,dd in opt2c.best_phyllo(0,0,R,lambda t:2.0 if t<0.75 else 2.5): circ(d,x,y,dd/2)
res['V0 Sonnenblume 2A-35 (kleine Löcher innen)']=(im,open_frac(im))
# V1: Sonnenblume umgekehrt + Zentralloch Ø7: große Löcher innen, außen kleiner
im,d=canvas(); circ(d,0,0,3.5)
pts=opt2c.best_phyllo(0,0,R,lambda t:2.5 if t<0.6 else 2.0)
for x,y,dd in pts:
    if math.hypot(x,y)-dd/2 >= 3.5+W: circ(d,x,y,dd/2)
res['V1 Sonnenblume umgekehrt + Zentralloch Ø7']=(im,open_frac(im))
# V2: Spiralschlitze aus den Sonnenblumen-Parastichen: 13 Hauptarme + 13 Zwischenarme außen + Zentralloch Ø8
im,d=canvas(); rc=4.0; circ(d,0,0,rc); n=13; w=1.6; PITCH=0.9
COSA=math.cos(math.atan(PITCH))                   # Arme laufen schräg: senkrechter Abstand = Bogenabstand·cos α
r_start=max(rc+W+w/2,(n*(w+W))/(2*math.pi*COSA)*1.12)
r_mid=(2*n*(w+W))/(2*math.pi*COSA)*1.12            # ab hier passen 26 Arme mit Steg ≥ 0,8
def arm(th0,r0):
    return [(r*math.cos(th0+PITCH*math.log(r/r_start)),r*math.sin(th0+PITCH*math.log(r/r_start))) for r in np.linspace(r0,R-w/2,60)]
for k in range(n):
    th0=2*math.pi*k/n
    slot_arc(d,arm(th0,r_start),w)
    slot_arc(d,arm(th0+math.pi/n,r_mid),w)
res['V2 Spiralschlitze 13+13 Arme + Zentralloch Ø8']=(im,open_frac(im))
# V3: konzentrische Ringschlitze mit 3 versetzten Stegen + Zentralloch Ø6
im,d=canvas(); circ(d,0,0,3.0); w=1.6; r=3.0+W+w/2; ring=0
while r+w/2<=R:
    gap=W+w                                  # Steg zwischen Segmenten (Bogenlänge)
    for s in range(3):
        a0=2*math.pi*s/3+ring*0.6; a1=a0+2*math.pi/3-gap/r
        arc=[(r*math.cos(a),r*math.sin(a)) for a in np.linspace(a0,a1,80)]
        slot_arc(d,arc,w)
    r+=w+W; ring+=1
res['V3 Ringschlitze + Zentralloch Ø6']=(im,open_frac(im))
for k,(im,o) in res.items(): print(f"{k:48s} {o:5.1f} % offen")
# Übersichtsbild
tiles=[]
from PIL import ImageFont
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',26)
for k,(im,o) in res.items():
    t=Image.new('RGB',(620,700),(236,238,242)); a=im.resize((560,560),Image.LANCZOS)
    disk=Image.new('RGB',(560,560),(214,217,222)); dd=ImageDraw.Draw(disk); dd.ellipse([0,0,559,559],fill=(214,217,222))
    holes=Image.new('RGB',(560,560),(18,19,23)); disk.paste(holes,(0,0),a)
    mask=Image.new('L',(560,560),0); ImageDraw.Draw(mask).ellipse([0,0,559,559],fill=255)
    t.paste(disk,(30,20),mask); ImageDraw.Draw(t).ellipse([30,20,589,579],outline=(250,250,252),width=5)
    ImageDraw.Draw(t).text((20,600),k.split(' ',1)[0]+f"  {o:.1f} % offen",font=F,fill=(20,20,20))
    ImageDraw.Draw(t).text((20,640),k.split(' ',1)[1][:44],font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',20),fill=(60,60,60))
    tiles.append(t)
out=Image.new('RGB',(620*len(tiles),700),'white')
for i,t in enumerate(tiles): out.paste(t,(620*i,0))
out.save('HT_Varianten.jpg',quality=90)
