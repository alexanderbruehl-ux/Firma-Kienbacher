import numpy as np, math
exec(open('konzepte.py').read().split("K_LIST=[")[0])
GOLD=math.radians(137.50776)
DIAMS=[1.0,1.5,2.0,2.5]   # nur 4 Bohrdurchmesser (Werkzeugkosten)
def qd(d): return min(DIAMS,key=lambda v:abs(v-d))
SADDLE=(128,74,38)

def polished(img,poly):
    """Hochglanzpoliertes Alu: Spiegelreflexe (weiche Studio-Lichtbänder), leicht kühl."""
    w,h=img.size; yy,xx=np.mgrid[0:h,0:w].astype(float)
    u=(xx*0.8+yy*0.35)/w
    v=0.50+0.30*np.sin(u*9.0+0.6)+0.16*np.sin(u*23.0+1.7)          # diagonale Lichtbänder
    v+=0.18*(1-yy/h)                                                 # Himmel oben heller
    v=np.clip(v,0,1)
    base=np.stack([70+175*v, 74+176*v, 82+178*v],-1)
    tex=Image.fromarray(np.clip(base,0,255).astype('uint8')).filter(ImageFilter.GaussianBlur(3))
    m=Image.new('L',img.size,0); ImageDraw.Draw(m).polygon([toPix(p) for p in poly],fill=255)
    img.paste(tex,(0,0),m)

def hole(pen,p,d):
    """Bohrung im polierten Alu: dunkel mit feiner Glanzfase oben links."""
    pen.circ(p,d/2+0.18,fill=(250,251,253)); pen.circ(p,d/2,fill=(16,17,21))

def diamond_ring(pen,c,R,w=2.4):
    """Diamantschnitt-Ring (Glanzfacette) um ein Lochfeld – nur als Ring, Feld bleibt poliert."""
    for rr,ww,col in ((R+w*0.80,w*0.40,(252,253,255)),(R+w*0.45,w*0.30,(140,146,156)),(R+w*0.15,w*0.30,(236,238,242))):
        x,y=pen.P(c); r=rr*K*SS; pen.d.ellipse([x-r,y-r,x+r,y+r],outline=col,width=max(1,int(ww*K*SS)))

# ---------- Muster ----------
def feld_sonnenblume(pen,cx,cy,D):
    """A: Phyllotaxis (Sonnenblumen-Spirale), Loch-Ø wächst nach außen – organisch, schimmert je nach Blickwinkel."""
    R=D/2-1.8; big=D>60
    pitch=3.1 if big else 2.2
    n=int((R/pitch)**2*math.pi*0.92)
    c=R/math.sqrt(n)
    for i in range(1,n):
        r=c*math.sqrt(i); a=i*GOLD
        t=r/R; d=qd((1.0+1.6*t**1.25) if big else (1.0+0.6*t))
        if r+d/2>R: continue
        hole(pen,(cx+r*math.cos(a),cy+r*math.sin(a)),d)

def feld_welle(pen,cx,cy,D):
    """B: konzentrische Lochkreise, Loch-Ø wellenförmig moduliert – Ringe scheinen zu 'schwingen' (Schallwelle)."""
    R=D/2-1.8; big=D>60; ring=2.9 if big else 2.1
    k=1; hole(pen,(cx,cy),1.5 if big else 1.0)
    while k*ring<R-1.2:
        r=k*ring; t=r/R
        d=((1.2+1.3*t)*(0.62+0.38*math.cos(2*math.pi*r/(R/2.6)))) if big else (0.8+0.6*t)*(0.7+0.3*math.cos(2*math.pi*r/(R/2)))
        d=qd(max(d,1.0)); n=int(2*math.pi*r/max(d+1.0,1.9))
        for i in range(n):
            a=2*math.pi*i/n+k*0.21
            hole(pen,(cx+r*math.cos(a),cy+r*math.sin(a)),d)
        k+=1

def feld_strahlen(pen,cx,cy,D):
    """C: Zentrum als Sonnenblumen-Feld, außen Strahlenkranz aus Langlöchern, die zum Rand länger werden."""
    R=D/2-1.8; big=D>60
    Ri=R*0.55
    feld_sonnenblume(pen,cx,cy,2*(Ri+1.8)) if big else feld_sonnenblume(pen,cx,cy,D*0.7)
    if not big:
        return
    n=int(2*math.pi*R/4.6)
    for i in range(n):
        a=2*math.pi*i/n
        r0=Ri+2.2; r1=R-1.2 - (0 if i%2 else 3.5)       # abwechselnd lang/kurz -> Strahlenkranz
        u=np.array([math.cos(a),math.sin(a)]); w=1.5
        pen.slot(np.array([cx,cy])+u*(r0+r1)/2,u,r1-r0,w,(16,17,21))

def stack(ims,path,q=88):
    Wm=max(i.width for i in ims); out=Image.new('RGB',(Wm,sum(i.height for i in ims)+8*(len(ims)-1)),'white'); y=0
    for i in ims: out.paste(i,(0,y)); y+=i.height+8
    out.save(path,quality=q)
import opt2c
def feld_strahlen_plus(pen,cx,cy,D):
    """C+: Strahlenkranz optimiert – max. offener Querschnitt bei Steg ≥ 0,8 mm, nur Ø1,5/2,0/2,5 + Fräser Ø2,0."""
    h,s=opt2c.field(cx,cy,D)
    for x,y,d in h: hole(pen,(x,y),d)
    for x0,y0,a,r0,r1 in s:
        u=np.array([math.cos(a),math.sin(a)]); pen.slot(np.array([x0,y0])+u*(r0+r1)/2,u,r1-r0,opt2c.SLOTW,(16,17,21))
def feld_sonnenblume35(pen,cx,cy,D):
    """A35: Sonnenblume querschnittsoptimiert – Sub/TMT Ø2,5→3,5, HT Ø2,0→2,5, Steg ≥ 0,8 mm (≈ 35 % offen)."""
    opt2c.WMIN=0.8
    q=lambda v,ds:min(ds,key=lambda x:abs(x-v))
    law=(lambda t:q(2.5+1.0*t,[2.5,3.0,3.5])) if D>60 else (lambda t:q(2.0+0.5*t,[2.0,2.5]))
    for x,y,d in opt2c.best_phyllo(cx,cy,D/2-1.2,law): hole(pen,(x,y),d)
def _stamp(pen,pts,w):
    pts=np.array(pts); seg=np.linalg.norm(np.diff(pts,axis=0),axis=1); L=np.concatenate([[0],np.cumsum(seg)])
    for s_ in np.arange(0,L[-1]+1e-9,0.08):
        pen.circ((np.interp(s_,L,pts[:,0]),np.interp(s_,L,pts[:,1])),w/2,fill=(16,17,21))
def ht_spirale(pen,cx,cy,D):
    """HT-V2: Spiralschlitze (13 Haupt- + 13 Zwischenarme, aus den Sonnenblumen-Spiralen) + Zentralloch Ø8."""
    R=D/2-1.2; rc=4.0; n=13; w=1.6; W=0.8; PITCH=0.9; COSA=math.cos(math.atan(PITCH))
    hole(pen,(cx,cy),2*rc)
    r0=max(rc+W+w/2,(n*(w+W))/(2*math.pi*COSA)*1.12); r1=(2*n*(w+W))/(2*math.pi*COSA)*1.12
    arm=lambda th0,rs:[(cx+r*math.cos(th0+PITCH*math.log(r/r0)),cy+r*math.sin(th0+PITCH*math.log(r/r0))) for r in np.linspace(rs,R-w/2,60)]
    for i in range(n):
        th=2*math.pi*i/n; _stamp(pen,arm(th,r0),w); _stamp(pen,arm(th+math.pi/n,r1),w)
def ht_ringe(pen,cx,cy,D):
    """HT-V3: konzentrische Ringschlitze (3 versetzte Stege je Ring) + Zentralloch Ø6."""
    R=D/2-1.2; w=1.6; W=0.8; hole(pen,(cx,cy),6.0); r=3.0+W+w/2; ring=0
    while r+w/2<=R:
        for s in range(3):
            a0=2*math.pi*s/3+ring*0.6; a1=a0+2*math.pi/3-(W+w)/r
            _stamp(pen,[(cx+r*math.cos(a),cy+r*math.sin(a)) for a in np.linspace(a0,a1,80)],w)
        r+=w+W; ring+=1
def sonnenblume_mit_ht(ht):
    def f(pen,cx,cy,D):
        if D<60: ht(pen,cx,cy,D)
        else: feld_sonnenblume35(pen,cx,cy,D)
    return f
import ht_m as _htm
def _signet(pen,cx,cy,width,fill):
    pts=_htm.signet_poly(width,cx,cy); pen.poly(pts,fill=fill)
def _radius(pts,cx,cy): return max(math.hypot(x-cx,y-cy) for x,y in pts)
def ht_m_medaillon(pen,cx,cy,D):
    """A: Signet-M als Durchbruch in einem Medaillon (Glanzring), Sonnenblumen-Löcher nur außen."""
    mw=20.0; rm=_radius(_htm.signet_poly(mw,cx,cy),cx,cy)+1.2
    diamond_ring(pen,(cx,cy),rm,w=1.2)
    _signet(pen,cx,cy,mw,(16,17,21))
    opt2c.WMIN=0.8
    for x,y,d in opt2c.best_phyllo(cx,cy,D/2-1.2,lambda t:2.0 if t<0.75 else 2.5):
        if math.hypot(x-cx,y-cy)-d/2>=rm+1.2+0.8: hole(pen,(x,y),d)
def tmt_emblem(pen,cx,cy,D):
    """B: massives, poliertes Medaillon mit eingefrästem M in der 100er-Mitte (Burmester-Prinzip), Löcher außen."""
    rm=10.0
    q=lambda v,ds:min(ds,key=lambda x:abs(x-v)); opt2c.WMIN=0.8
    for x,y,d in opt2c.best_phyllo(cx,cy,D/2-1.2,lambda t:q(2.5+1.0*t,[2.5,3.0,3.5])):
        if math.hypot(x-cx,y-cy)-d/2>=rm+2.0: hole(pen,(x,y),d)
    pen.circ((cx,cy),rm,fill=(246,247,250)); diamond_ring(pen,(cx,cy),rm,w=1.4)
    _signet(pen,cx+0.12,cy-0.12,13.0,(250,251,253)); _signet(pen,cx-0.12,cy+0.12,13.0,(120,126,136)); _signet(pen,cx,cy,13.0,(196,200,207))
def ht_offen_mitte(pen,cx,cy,D):
    """HT mit offener Mitte: Zentralloch Ø7, Sonnenblume umgekehrt (große Löcher innen)."""
    hole(pen,(cx,cy),7.0); opt2c.WMIN=0.8
    for x,y,d in opt2c.best_phyllo(cx,cy,D/2-1.2,lambda t:2.5 if t<0.6 else 2.0):
        if math.hypot(x-cx,y-cy)-d/2>=3.5+0.8: hole(pen,(x,y),d)
def kombi(ht,tmt):
    def f(pen,cx,cy,D):
        if D<60: ht(pen,cx,cy,D)
        elif D<130: tmt(pen,cx,cy,D)
        else: feld_sonnenblume35(pen,cx,cy,D)
    return f
import m_schlitz as _ms
def _segdist(p,a,b):
    p,a,b=map(np.array,(p,a,b)); t=np.clip(np.dot(p-a,b-a)/np.dot(b-a,b-a),0,1); return np.linalg.norm(p-(a+t*(b-a)))
def sonnenblume_mit_M(mfac,law_fn,edge=1.2):
    def f(pen,cx,cy,D):
        mw=mfac*D; legs=[((a[0]+cx,a[1]+cy),(b[0]+cx,b[1]+cy),sw) for a,b,sw in _ms.m_legs(mw,0,0,2.5,1.6)]
        opt2c.WMIN=0.8
        for x,y,d in opt2c.best_phyllo(cx,cy,D/2-edge,law_fn(D)):
            if all(_segdist((x,y),a,b)-sw/2-d/2>=0.8 for a,b,sw in legs): hole(pen,(x,y),d)
        for a,b,sw in legs: _stamp(pen,[a,b],sw)
    return f
def _law(D):
    q=lambda v,ds:min(ds,key=lambda x:abs(x-v))
    return (lambda t:q(2.5+1.0*t,[2.5,3.0,3.5])) if D>60 else (lambda t:2.0 if t<0.75 else 2.5)
def nur_ht_M(pen,cx,cy,D):
    if D<60: sonnenblume_mit_M(28/46.2,_law)(pen,cx,cy,D)
    else: feld_sonnenblume35(pen,cx,cy,D)
def alle_M(pen,cx,cy,D):
    sonnenblume_mit_M(0.6,_law)(pen,cx,cy,D)
MUSTER={'MH':('M-Schlitze im Hochtöner',nur_ht_M),'MALL':('M-Schlitze in allen Feldern',alle_M),'MA':('HT mit M-Medaillon',kombi(ht_m_medaillon,feld_sonnenblume35)),'MB':('100er mit M-Emblem',kombi(ht_offen_mitte,tmt_emblem)),'A35S':('Sonnenblume + HT Spiralschlitze',sonnenblume_mit_ht(ht_spirale)),'A35R':('Sonnenblume + HT Ringschlitze',sonnenblume_mit_ht(ht_ringe)),'A35':('Sonnenblume querschnittsoptimiert',feld_sonnenblume35),'C+':('Strahlenkranz optimiert',feld_strahlen_plus),'A':('Sonnenblume',feld_sonnenblume),'B':('Welle',feld_welle),'C':('Strahlenkranz',feld_strahlen)}

def alu_poliert(img,muster='A'):
    shadow(img,BL); polished(img,BL); pen=Pen(img)
    for x,y,d in HOLES:
        diamond_ring(pen,(x,y),d/2)
        # Feldgrund minimal dunkler (Spiegel innen ruhiger)
        MUSTER[muster][1](pen,x,y,d)
    logo(pen,False,False,(205,208,214))
    nut(pen)
    facet(pen,BL,col=(255,255,255),inner=(110,116,126),w=1.4)
    return pen.done()

def leder(img): return k1_leder(img,SADDLE)

def sheet(items,path,crop_fn=None):
    ims=[label(crop_fn(fn(canvas_flat())) if crop_fn else fn(canvas_flat()),t) for t,fn in items]
    stack(ims,path)
def sheet_montage(items,path):
    ims=[label(fn(base.copy()),t) for t,fn in items]; stack(ims,path)

if __name__=='__main__':
    V1=("Variante 1 – Leder sattelbraun · Logo geprägt · Edelstahlleiste 12 mm", leder)
    import sys
    if 'mschlitz' in sys.argv:
        items=[("Sonnenblume + ausgefrästes M im Hochtöner (HT 27,3 % statt 25,1 % offen)", lambda im: alu_poliert(im,'MH')),
               ("Sonnenblume + ausgefrästes M in allen drei Feldern", lambda im: alu_poliert(im,'MALL'))]
        sheet(items,'M_Schlitz_Blende.jpg',crop); print('ok'); raise SystemExit
    if 'mlogo' in sys.argv:
        items=[("A · Hochtöner: M als Durchbruch im Medaillon, Löcher außen", lambda im: alu_poliert(im,'MA')),
               ("B · Burmester-Prinzip: M-Emblem massiv in der 100er-Mitte, HT mit offener Mitte", lambda im: alu_poliert(im,'MB'))]
        sheet(items,'M_Varianten_Blende.jpg',crop); print('ok'); raise SystemExit
    if 'ht' in sys.argv:
        items=[("Hochtöner V2 Spiralschlitze · HT 39,7 % offen · Mitte offen Ø8", lambda im: alu_poliert(im,'A35S')),
               ("Hochtöner V3 Ringschlitze · HT 49,8 % offen · Mitte offen Ø6", lambda im: alu_poliert(im,'A35R'))]
        sheet(items,'HT_Varianten_Blende.jpg',crop); print('ok'); raise SystemExit
    if 'vergleich' in sys.argv:
        items=[("2A Sonnenblume bisher · 27,8 % offen · Steg 0,56 mm (zu dünn)", lambda im: alu_poliert(im,'A')),
               ("2A-35 Sonnenblume querschnittsoptimiert · 35,1 % offen · Steg ≥ 0,8 mm", lambda im: alu_poliert(im,'A35'))]
        sheet(items,'Sonnenblume_Vergleich.jpg',crop); print('ok'); raise SystemExit
    V2=("Variante 2 – Alu hochglanzpoliert · Sonnenblume querschnittsoptimiert · 35 % offen", lambda im: alu_poliert(im,'A35'))
    items=[V1,V2]
    sheet(items,'Vorschau_flach.jpg',crop)
    sheet_montage(items,'Vorschau_Montage.jpg')
    print('ok')
