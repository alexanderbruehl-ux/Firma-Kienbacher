import numpy as np, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops, ImageEnhance
exec(open('render_v7.py').read().split("FB=ImageFont")[0])   # base (Foto, mm-Raum), toPix, K, W, H, BLD, DK, holes, DX
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FONTR='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
SS=2  # Supersampling
BL=np.array(BLD)            # Blende (mm, verschoben um DX)
LOGO_W=115.0
LOGO_ANG=3.711   # parallel zur Unterkante
import sys as _s; _s.path.insert(0,'../logo'); import mwlogo as _mw
LOGO_H=LOGO_W/_mw.ASPECT
# mittig unter dem 100er (KT 100 V), Unterkante des Logos 5 mm über der Blendenunterkante
LOGO_EDGE=8.0   # Abstand Logounterkante zur Blendenunterkante
# Logo-Mittelachse (senkrecht zur Grundlinie, also um LOGO_ANG gekippt) verlängert durch den 100er-Mittelpunkt
_a=math.radians(LOGO_ANG); _T=np.array([286.1+DX,120.7]); _B0=np.array([0.0+DX,0.0])
_n=np.array([math.sin(_a),-math.cos(_a)])          # Richtung "nach unten" senkrecht zur Unterkante
_dT=np.dot(_T-_B0,-_n)                              # Abstand 100er-Mitte zur Unterkante
LOGO=tuple(_T+(_dT-(LOGO_EDGE+LOGO_H/2))*_n)
import sys; sys.path.insert(0,'../logo'); import mwlogo
HOLES=[(x,y,d) for x,y,d in holes]
def inside_poly(p,poly,margin=0):
    # Punkt in konvexem Polygon mit Randabstand
    n=len(poly)
    for i in range(n):
        a=poly[i];b=poly[(i+1)%n];d=b-a;nn=np.array([d[1],-d[0]])/np.linalg.norm(d)
        if np.dot(p-a,nn)>-margin: return False
    return True
# Orientierung prüfen (UZS/gegen UZS)
if not inside_poly(BL.mean(0),BL): BL=BL[::-1].copy()
ANG=math.atan2(BL[3][1]-BL[0][1],BL[3][0]-BL[0][0]) if False else None
LEFT=np.array(BLD[3])-np.array(BLD[0]); LEFT/=np.linalg.norm(LEFT)   # Richtung linke Kante (65,6°)

def canvas_flat():
    Wf,Hf=W,H
    im=Image.new('RGB',(Wf,Hf),(226,228,231))
    return im
class Pen:
    def __init__(s,img): s.img=img.resize((img.width*SS,img.height*SS)); s.d=ImageDraw.Draw(s.img,'RGBA')
    def P(s,p): x,y=toPix(p); return (x*SS,y*SS)
    def poly(s,pts,**k): s.d.polygon([s.P(p) for p in pts],**k)
    def circ(s,c,r,**k):
        x,y=s.P(c); rr=r*K*SS; s.d.ellipse([x-rr,y-rr,x+rr,y+rr],**k)
    def line(s,a,b,**k): s.d.line([s.P(a),s.P(b)],**k)
    def slot(s,c,u,L,w,fill):
        # Langloch: Mitte c, Richtung u, Länge L (Mitte-Mitte), Breite w
        a=c-u*L/2;b=c+u*L/2
        s.d.line([s.P(a),s.P(b)],fill=fill,width=max(1,int(w*K*SS)))
        s.circ(a,w/2,fill=fill); s.circ(b,w/2,fill=fill)
    def text(s,p,t,size_mm,fill,**k):
        f=ImageFont.truetype(FONT,max(6,int(size_mm*K*SS))); s.d.text(s.P(p),t,font=f,fill=fill,anchor='mm',**k)
    def done(s): return s.img.resize((s.img.width//SS,s.img.height//SS),Image.LANCZOS)

def shadow(img,poly,strength=.55):
    sh=Image.new('L',img.size,0); ImageDraw.Draw(sh).polygon([toPix(p) for p in poly],fill=255)
    sh=ImageChops.offset(sh.filter(ImageFilter.GaussianBlur(10)),-6,10)
    img.paste(Image.new('RGB',img.size,(4,6,12)),(0,0),sh.point(lambda v:int(v*strength)))

def alu_texture(img,poly,tone=(184,188,193),dark=False):
    # gebürstet/gestrahlt: horizontale Feinstruktur + leichter Lichtverlauf
    w,h=img.size; rng=np.random.default_rng(7)
    base=np.ones((h,w,3))*np.array(tone,float)
    base+=rng.normal(0,4.5 if not dark else 3,(h,1,1))
    grad=np.linspace(1.06,0.92,w)[None,:,None]; base*=grad
    tex=Image.fromarray(np.clip(base,0,255).astype('uint8'))
    m=Image.new('L',img.size,0); ImageDraw.Draw(m).polygon([toPix(p) for p in poly],fill=255)
    img.paste(tex,(0,0),m)

def facet(pen,poly,col=(250,251,253),inner=(120,124,130),w=1.2):
    n=len(poly)
    for i in range(n):
        a=np.array(poly[i]);b=np.array(poly[(i+1)%n])
        pen.line(a,b,fill=col,width=int(w*K*SS))
    # innere Schattenkante der Facette
    c=np.mean(poly,0); ip=[c+(np.array(p)-c)*0.994 for p in poly]
    for i in range(n): pen.line(ip[i],ip[(i+1)%n],fill=inner,width=max(1,int(.35*K*SS)))

HOLE=(24,26,32)
def _edge_offset(a,b,g):
    """Linie a-b um g mm nach innen (Richtung Blendenmitte) versetzen, auf Ober-/Unterkante beschneiden."""
    c=BL.mean(0); d=b-a; n=np.array([-d[1],d[0]])/np.linalg.norm(d)
    if np.dot(n,c-a)<0: n=-n
    def cut(p0,dd,q0,qd):
        t=np.linalg.solve(np.array([dd,-qd]).T,q0-p0); return p0+t[0]*dd
    p=a+n*g
    lo=cut(p,d,BL[0],BL[1]-BL[0]); hi=cut(p,d,BL[3],BL[2]-BL[3])
    return lo,hi
def edelstahlleiste(pen,breite=9.0):
    """Polierte Edelstahl-Abschlussleiste an der rechten (überstehenden) Kante, Breite wie die Einfassung des
    Schwalbennests im Rumpf (≈ 9 mm, aus dem Foto gemessen). Spiegelnd: dunkle Reflexkante außen, Glanzstreifen,
    Umgebungsreflex, Schattenfuge innen."""
    a,b=BL[1],BL[2]
    rel=[(0.00,0.07,(90,94,100)),(0.07,0.20,(215,218,223)),(0.20,0.36,(255,255,255)),(0.36,0.50,(196,200,206)),
         (0.50,0.66,(118,124,134)),(0.66,0.82,(176,181,188)),(0.82,0.93,(234,236,240)),(0.93,1.00,(40,42,48))]
    for r0,r1,col in rel:
        l0,h0=_edge_offset(a,b,r0*breite); l1,h1=_edge_offset(a,b,r1*breite)
        pen.poly([l0,h0,h1,l1],fill=col)
def nut(pen,abstand=4.0,breite=1.2):
    """Schlanke gefräste Nut parallel zur rechten Kante (optische Nähe zur Edelstahleinfassung), Glanzflanke."""
    a,b=BL[1],BL[2]
    l0,h0=_edge_offset(a,b,abstand); l1,h1=_edge_offset(a,b,abstand+breite)
    pen.poly([l0,h0,h1,l1],fill=(62,66,72))
    l2,h2=_edge_offset(a,b,abstand+breite*0.7)
    pen.poly([l2,h2,h1,l1],fill=(236,238,242))

# ---------------- Konzepte ----------------
def k1_leder(img,col):
    shadow(img,BL)
    pen=Pen(img)
    pen.poly(BL,fill=col)
    # Lederstruktur
    rng=np.random.default_rng(3)
    for _ in range(9000):
        p=BL[0]+rng.random()*(BL[1]-BL[0])+rng.random()*(BL[3]-BL[0])
        if inside_poly(p,BL,1): pen.circ(p,.25,fill=tuple(int(c*0.88) for c in col)+(120,))
    # Ziernaht umlaufend 4 mm innen
    c=BL.mean(0)
    def insetpoly(poly,g):
        out=[]
        n=len(poly)
        L=[]
        for i in range(n):
            a=poly[i];b=poly[(i+1)%n];d=b-a;nn=np.array([-d[1],d[0]])/np.linalg.norm(d)
            if np.dot(nn,c-a)<0: nn=-nn
            L.append((a+nn*g,d))
        for i in range(n):
            (p1,d1),(p2,d2)=L[i-1],L[i]; t=np.linalg.solve(np.array([d1,-d2]).T,p2-p1); out.append(p1+t[0]*d1)
        return out
    ip=insetpoly(BL,4.5); stitch=tuple(min(255,int(v*1.6+40)) for v in col)
    for i in range(4):
        a=ip[i];b=ip[(i+1)%4];L=np.linalg.norm(b-a);u=(b-a)/L
        for t in np.arange(0,L-3,5): pen.line(a+u*t,a+u*(t+3),fill=stitch,width=int(.6*K*SS))
    # Gitter schwarz mit Metall-Zierring
    for x,y,d in HOLES:
        pen.circ((x,y),d/2+1.2,fill=(40,40,44)); pen.circ((x,y),d/2,fill=(14,14,16))
        for yy in np.arange(y-d/2,y+d/2,2.0):
            hw=math.sqrt(max((d/2-0.8)**2-(yy-y)**2,0)); pen.line((x-hw,yy),(x+hw,yy),fill=(34,34,38),width=max(1,int(.5*K*SS)))
    # geprägtes Logo
    draw_logo(pen,tuple(min(255,int(v*1.35)+14) for v in col)+(255,),offset=(-0.35,0.35))
    draw_logo(pen,tuple(int(v*0.62) for v in col)+(255,))
    # Edelstahl-Abschlussleiste rechts
    edelstahlleiste(pen)
    return pen.done()

def k2_base(img,tone=(184,188,193),dark=False):
    shadow(img,BL); alu_texture(img,BL,tone,dark); return Pen(img)

def k2a_ringe(img,tone=(184,188,193),led=False,dark=False):
    pen=k2_base(img,tone,dark)
    for x,y,d in HOLES:
        R=d/2
        # polierter Diamantschnitt-Ring (Facette) um jedes Feld
        pen.circ((x,y),R+2.2,fill=(236,238,241)); pen.circ((x,y),R+0.9,fill=tone if not dark else tuple(int(v) for v in tone))
        # konzentrische Lochkreise, Lochgröße wächst nach außen
        ring=2.8 if d>60 else 2.2; r=1.4 if d>60 else 1.0
        rr=0.0; pen.circ((x,y),0.9 if d>60 else 0.7,fill=HOLE)
        k=1
        while True:
            rr=k*ring
            if rr>R-1.6: break
            dh=(1.0+1.4*rr/R) if d>60 else (0.8+0.6*rr/R)
            n=int(2*math.pi*rr/(dh+ (1.2 if d>60 else 1.0)))
            for i in range(n):
                a=2*math.pi*i/n+(k%2)*math.pi/n
                pen.circ((x+rr*math.cos(a),y+rr*math.sin(a)),dh/2,fill=HOLE)
            k+=1
    logo(pen,led,dark,tone)
    nut(pen)
    facet(pen,BL)
    return pen.done()

def k2b_diagonal(img,tone=(184,188,193),led=False,dark=False):
    pen=k2_base(img,tone,dark)
    u=LEFT; nrm=np.array([u[1],-u[0]])
    # Langlöcher parallel zur linken Kante (65,6°), nur über den Treibern, Länge = Sehne
    for x,y,d in HOLES:
        R=d/2-1.8; pitch=4.2 if d>60 else 3.0; w=2.2 if d>60 else 1.6
        c=np.array([x,y])
        for o in np.arange(-R+w/2,R,pitch):
            half=math.sqrt(max(R*R-o*o,0))-w/2
            if half<1: continue
            pen.slot(c+nrm*o,u,2*half,w,HOLE)
        pen.circ((x,y),d/2+0.6,outline=(238,240,243),width=int(.7*K*SS))
    logo(pen,led,dark,tone)
    nut(pen)
    facet(pen,BL)
    return pen.done()

def k2c_verlauf(img,tone=(184,188,193),led=False,dark=False):
    pen=k2_base(img,tone,dark)
    # flächiges Lochfeld im 65,6°-Raster, Loch-Ø läuft von links (groß) nach rechts (klein) aus
    u=LEFT; v=np.array([1.0,0.0]); pitch=5.0
    xs=BL[:,0]; x_min,x_max=xs.min(),xs.max()
    for i in range(-10,200):
        for j in range(-5,60):
            p=BL[0]+v*(i*pitch)+u*(j*pitch*0.95)+ (v*pitch/2 if j%2 else 0)
            if not inside_poly(p,BL,6): continue
            # im Logo-Bereich aussparen
            _d=p-np.array(LOGO); _c,_s=math.cos(math.radians(LOGO_ANG)),math.sin(math.radians(LOGO_ANG))
            if abs(_d[0]*_c+_d[1]*_s)<LOGO_W/2+5 and abs(-_d[0]*_s+_d[1]*_c)<LOGO_H/2+4: continue
            t=(p[0]-x_min)/(x_max-x_min)
            over=any(math.hypot(p[0]-x,p[1]-y)<d/2-1 for x,y,d in HOLES)
            dh=(3.2-2.4*t) if over else (1.6-1.5*t)
            if dh<0.5: continue
            pen.circ(p,dh/2,fill=HOLE)
    logo(pen,led,dark,tone)
    nut(pen)
    facet(pen,BL)
    return pen.done()

def draw_logo(pen,fill,with_wordmark=True,width=LOGO_W,center=None,glow=None,offset=(0,0),signet_only=False):
    c=center or LOGO
    to=lambda p:pen.P((p[0]+offset[0],p[1]+offset[1]))
    def poly(pts):
        if glow:
            for w,a in glow: pen.d.polygon(pts,fill=None,outline=fill[:3]+(a,),width=w)
        pen.d.polygon(pts,fill=fill)
    def glyph(ps):
        # Außenkontur füllen, Innenkonturen (Punzen) mit Hintergrund ausschneiden -> gerade/ungerade über Maske
        m=Image.new('L',pen.img.size,0); md=ImageDraw.Draw(m)
        for p in ps:
            tmp=Image.new('L',pen.img.size,0); ImageDraw.Draw(tmp).polygon(p,fill=255); m=ImageChops.logical_xor(m.convert('1'),tmp.convert('1')).convert('L')
        pen.img.paste(Image.new('RGB',pen.img.size,fill[:3]),(0,0),m)
    return mwlogo.draw(poly,glyph,to,c[0],c[1],width,fill,with_wordmark,angle_deg=LOGO_ANG,signet_only=signet_only)
def logo(pen,led,dark,tone=(184,188,193)):
    """Logo eingefräst (keine Farbe, keine LED): flache Frästasche mit Licht-/Schattenkante.
    Natur/hell: Taschengrund etwas dunkler als die gestrahlte Fläche; dunkles Eloxal: blank gefräst (hell)."""
    if dark:
        base=(196,199,204,255)                        # blankes Alu im Fräsgrund
    else:
        base=tuple(int(v*0.80) for v in tone)+(255,)  # Fräsgrund matter/dunkler
    sh=tuple(max(0,int(v*0.55)) for v in tone)+(255,) # Schattenkante (Licht von links oben)
    hl=(245,247,250,255)                              # Lichtkante
    draw_logo(pen,hl,offset=(0.18,-0.18))
    draw_logo(pen,sh,offset=(-0.18,0.18))
    draw_logo(pen,base)
# ---------------- Ausgabe ----------------
def label(im,title,sub=None):
    d=ImageDraw.Draw(im); f=ImageFont.truetype(FONT,30); fs=ImageFont.truetype(FONTR,22)
    d.rectangle([0,0,im.width,46],fill=(0,0,0)); d.text((14,8),title,font=f,fill='white')
    if sub: d.text((14,im.height-34),sub,font=fs,fill=(40,40,40))
    return im
def crop(im): return im.crop((0,int(0.02*im.height),int(im.width*0.64),int(im.height*0.98)))
K_LIST=[
 ("K1 Leder – dunkelblau · LS-Gitter · geprägtes Logo · polierte Edelstahl-Abschlussleiste", lambda im:k1_leder(im,(30,42,78))),
 ("K2a Alu „Ringe“ – konzentrische Lochkreise, Diamantschnitt-Ringe, Logo eingefräst, Kantennut", lambda im:k2a_ringe(im)),
 ("K2b Alu „Diagonale“ – Langlöcher im 65,6°-Winkel, Logo eingefräst, Kantennut", lambda im:k2b_diagonal(im)),
 ("K2c Alu „Verlauf“ – Lochfeld flächig, Loch-Ø läuft aus, Logo eingefräst, Kantennut", lambda im:k2c_verlauf(im)),
]
import sys
flat=[];mont=[]
for title,fn in K_LIST:
    f=fn(canvas_flat()); flat.append(label(crop(f),title))
    m=fn(base.copy()); mont.append(label(m,title))
def stack(ims,path,q=88):
    Wm=max(i.width for i in ims); out=Image.new('RGB',(Wm,sum(i.height for i in ims)+8*(len(ims)-1)),'white'); y=0
    for i in ims: out.paste(i,(0,y)); y+=i.height+8
    out.save(path,quality=q)
stack(flat,'Konzepte_flach.jpg'); stack(mont,'Konzepte_Montage.jpg')
# Lederfarben
cols=[("dunkelblau",(30,42,78)),("hellgrau",(176,178,180)),("schwarz",(26,26,28)),("sattelbraun",(128,74,38))]
sw=[label(crop(k1_leder(canvas_flat(),c)),"K1 Leder – "+n) for n,c in cols]
stack(sw,'K1_Lederfarben_flach.jpg')
swm=[label(k1_leder(base.copy(),c),"K1 Leder – "+n) for n,c in cols]
stack(swm,'K1_Lederfarben_Montage.jpg')
# K2 Farbvarianten Eloxal
el=[("natur (C-0), gestrahlt",(184,188,193),False),("titan/sektfarben",(170,160,142),False),("dunkelblau eloxiert",(40,52,86),True),("schwarz eloxiert",(38,39,42),True)]
ev=[label(crop(k2b_diagonal(canvas_flat(),t,False,dk)),"K2b Eloxal – "+n) for n,t,dk in el]
stack(ev,'K2_Eloxalfarben_flach.jpg')
print('ok')
