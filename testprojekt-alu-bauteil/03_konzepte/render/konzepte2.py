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
MUSTER={'A':('Sonnenblume',feld_sonnenblume),'B':('Welle',feld_welle),'C':('Strahlenkranz',feld_strahlen)}

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
    items=[V1]+[(f"Variante 2{k} – Alu hochglanzpoliert · Lochmuster „{n}“", (lambda kk: (lambda im: alu_poliert(im,kk)))(k)) for k,(n,_) in MUSTER.items()]
    sheet(items,'Vorschau_flach.jpg',crop)
    sheet_montage(items,'Vorschau_Montage.jpg')
    print('ok')
