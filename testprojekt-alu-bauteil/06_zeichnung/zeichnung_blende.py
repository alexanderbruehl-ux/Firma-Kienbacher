"""Fertigungszeichnung Blende Schwalbennest 2A-35 (A3 quer, PDF + PNG), aus den Modelldaten von 04_cad/blende/blende_2a35.py erzeugt.
    python3 zeichnung_blende.py     ->  Zeichnung_Blende_2A35M.pdf / .png
Inhalt: Ansicht von vorn (1:2), Detail Hochtöner-Feld (3:1), Schnitt durch das Tiefmitteltöner-Feld mit gestufter Haut (2:1), Bohrtabelle, Schriftfeld.
Koordinaten/Maße in mm. Die Bohrungen werden mit Mittelpunkt und Durchmesser aus dem Modell gezeichnet, nicht von Hand."""
import json, math, os, sys, collections, numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.normpath(os.path.join(HERE,'..'))
sys.path.insert(0,os.path.join(ROOT,'04_cad','blende')); import blende_2a35 as B
import signet_m
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon as MPoly
P=json.load(open(os.path.join(ROOT,'parameter.json')))
HT=json.load(open(B.HT_LOECHER))['holes']
fields=[]
for x,y,D in B.HOLES:
    if D<60: pts=[(x+hx,y+hy,hd) for hx,hy,hd in HT]
    else: pts=B.field_2a35(x,y,D)
    fields.append((x,y,D,pts))
cnt=collections.Counter()
for x,y,D,pts in fields:
    for p in pts: cnt[(D,round(p[2],1))]+=1
fig=plt.figure(figsize=(420/25.4,297/25.4)); fig.patch.set_facecolor('white')
INK='#111'; 
def frame(ax_rect,title):
    a=fig.add_axes(ax_rect); a.set_aspect('equal'); a.axis('off'); a.text(0,1.0,title,transform=a.transAxes,fontsize=9,fontweight='bold',va='bottom'); return a
mm=lambda v:v/25.4/ (420/25.4)           # mm auf Blattbreite
# --- Ansicht von vorn 1:2 ---
W0,H0=420.0,297.0; R=lambda x,y,w,h:[x/W0,y/H0,w/W0,h/H0]
a=frame(R(12,150,240,135),'Ansicht von vorn (linke Bootsseite)   M 1:2')
a.add_patch(MPoly(B.BL,fill=False,ec=INK,lw=1.2))
for x,y,D,pts in fields:
    a.add_patch(Circle((x,y),D/2,fill=False,ec=INK,lw=.8)); a.add_patch(Circle((x,y),D/2+B.RING,fill=False,ec=INK,lw=.4,ls='--'))
    for px,py,d in pts: a.add_patch(Circle((px,py),d/2,fill=False,ec=INK,lw=.25))
    a.plot([x-4,x+4],[y,y],color='#c00',lw=.4); a.plot([x,x],[y-4,y+4],color='#c00',lw=.4)
    a.annotate(f'Ø{D}',(x,y-D/2-3),ha='center',va='top',fontsize=7)
for mx,my in B.MAGNETS: a.add_patch(Circle((mx,my),6.0,fill=False,ec='#06c',lw=.6,ls=':'))
import ezdxf
for e in ezdxf.readfile(os.path.join(ROOT,'04_cad','blende','dxf','Logo_Abdeckung_100er.dxf')).modelspace().query('LWPOLYLINE[layer=="LOGO"]'):
    a.add_patch(MPoly([(p[0],p[1]) for p in e.get_points()],fc='#06c',ec='none',alpha=.8))
a.set_xlim(-5,465); a.set_ylim(-5,215)
a.text(0.0,-0.02,'Blendendicke 8,5 · Frontfase 0,5 · Logo 105 mm breit, 0,5 tief gefräst, Schrift 8 mm über Unterkante · Kantennut 1,2 × 0,6 im Abstand 12 zur rechten Kante · 4 Magnettaschen Ø12,4 × 1,6 (hinten)',transform=a.transAxes,fontsize=6,va='top')
# --- Detail Hochtöner 3:1 ---
x,y,D,pts=[f for f in fields if f[2]<60][0]
a=frame(R(258,150,150,135),'Detail Hochtöner-Feld Ø46,2   M 3:1')
a.add_patch(Circle((x,y),D/2,fill=False,ec=INK,lw=.9))
M=signet_m.signet_poly(B.M_WIDTH,x+B.M_DX,y+B.M_DY,ang=math.radians(B.M_ANG)); a.add_patch(MPoly(M,fc='#bbb',ec=INK,lw=.7))
for px,py,d in pts: a.add_patch(Circle((px,py),d/2,fill=False,ec=INK,lw=.5)); 
sz={1.5:'#d6336c',2.0:'#e8890c',2.5:'#222'}
for px,py,d in pts: a.add_patch(Circle((px,py),d/2,fill=True,fc='none',ec=sz.get(round(d,1),'#222'),lw=.7))
a.plot([x-26,x+26],[y,y],color='#c00',lw=.3,ls='-.'); a.plot([x,x],[y-26,y+26],color='#c00',lw=.3,ls='-.')
a.set_xlim(x-26,x+26); a.set_ylim(y-24,y+25)
a.text(0.0,-0.02,'Ø2,5 schwarz · Ø2,0 orange · Ø1,5 rot · Steg ≥ 0,8 · Restwand 1,5 · M 28 mm senkrecht, 1,5 über Mitte',transform=a.transAxes,fontsize=6,va='top')
# --- Schnitt TMT ---
a=frame(R(12,72,170,62),'Schnitt durch Feld Ø118,2 (Haut)   M 2:1')
Rf=59.1; sk=B.SKIN; st=[(0.0,sk)]+[(f*Rf,t) for f,t in B.HAUT_STUFEN]
z=lambda t:-B.RECESS-t
prof=[(0,z(sk)),(st[1][0],z(sk))]; tprev=sk
for k in range(1,len(st)):
    rk,tk=st[k]; prof.append((rk+(tk-tprev),z(tk))); 
    if k+1<len(st): prof.append((st[k+1][0],z(tk)))
    tprev=tk
tm=st[-1][1]; prof+= [(Rf-B.HAUT_RADIUS,z(tm))]
th=np.linspace(0,math.pi/2,12); arc=[(Rf-B.HAUT_RADIUS+B.HAUT_RADIUS*math.sin(t_),z(tm)-B.HAUT_RADIUS+B.HAUT_RADIUS*math.cos(t_)) for t_ in th]
prof+=arc
poly=[(0,-B.RECESS)]+[(Rf,-B.RECESS)]+prof[::-1][:0]
a.add_patch(MPoly([(0,-B.RECESS),(Rf,-B.RECESS),(Rf,z(tm)-B.HAUT_RADIUS)]+[(p[0],p[1]) for p in prof[::-1] if p[0]<Rf-1e-6][:]+[(0,z(sk))],fc='#d7dbe6',ec=INK,lw=.9))
a.plot([-2,Rf+4],[0,0],color=INK,lw=.9)
for (r0,t0),lab in zip(st,('Mitte','Stufe 1','Stufe 2')): pass
a.annotate('2,2',(10,z(2.2)-0.1),fontsize=7,va='top',ha='center'); a.annotate('2,85',(0.57*Rf,z(2.85)-0.1),fontsize=7,va='top',ha='center'); a.annotate('3,5',(0.88*Rf,z(3.5)-0.1),fontsize=7,va='top',ha='center')
a.annotate('45° (V-Fräser)',(0.42*Rf+0.5,z(2.5)),fontsize=6,xytext=(0.42*Rf+8,z(1.0)),arrowprops=dict(arrowstyle='-',lw=.4)); a.annotate('R2,5',(Rf-1,z(tm)-1.2),fontsize=6,xytext=(Rf-8,z(tm)-3.5),arrowprops=dict(arrowstyle='-',lw=.4))
a.set_xlim(-3,Rf+6); a.set_ylim(-8.5,1.5); a.text(0.0,-0.02,'Vorderseite oben (Absenkung 0,6 mm); Haut von hinten gestuft gefräst:\nMitte 2,2 · ab 0,42·R 2,85 · ab 0,72·R 3,5; Flankenversatz = Stufenhöhe (45°).\nFeld Ø156,2 gleich, Radien skaliert.',transform=a.transAxes,fontsize=6,va='top')
# --- Bohrtabelle ---
a=fig.add_axes(R(200,60,208,80)); a.axis('off'); a.text(0,1.02,'Bohrungen',fontsize=9,fontweight='bold',va='bottom')
rows=[('Feld','Bohr-Ø [mm]','Anzahl','Restwand mitte/rand [mm]')]
for x,y,D,pts in fields:
    c=collections.Counter(round(p[2],1) for p in pts); wall='1,5' if D<60 else '2,2 / 3,5'
    for d,n in sorted(c.items()): rows.append((f'Ø{D}',f'{d:.1f}'.replace('.',','),str(n),wall))
rows.append(('gesamt','',str(sum(len(f[3]) for f in fields)),''))
for i,r in enumerate(rows):
    for j,(c,xx) in enumerate(zip(r,(0.0,0.26,0.50,0.66))): a.text(xx,0.97-i*0.085,c,fontsize=7.5,fontweight='bold' if i==0 or i==len(rows)-1 else None,va='top')
a.plot([0,1],[0.9,0.9],color=INK,lw=.5); a.set_xlim(0,1); a.set_ylim(0,1)
# --- Schriftfeld ---
a=fig.add_axes(R(12,8,396,50)); a.axis('off'); a.add_patch(plt.Rectangle((0,0),1,1,fill=False,ec=INK,lw=1.2,transform=a.transAxes))
info=[('Benennung','Blende Schwalbennest links, Variante 2A-35'),('Werkstoff','EN AW-6082 T6 · Platte 8,5 mm'),('Oberfläche','Hochglanzpoliert, Diamantschnitt-Konus 2,0 mm an den Feldkanten'),('Masse (CAD)','1107 g · Volumen 410,1 cm³'),('Allgemeintoleranz','ISO 2768-m'),('Stand','03.10.2026 · Rev. A (Entwurf, nicht freigegeben)'),('Sachnummer','TP-ALU-BLENDE-2A35M-L')]
for i,(k,v) in enumerate(info): a.text(0.01,0.92-i*0.13,k+':',fontsize=7.5,va='top',fontweight='bold'); a.text(0.14,0.92-i*0.13,v,fontsize=7.5,va='top')
a.text(0.99,0.9,'Kienbacher Testprojekt\nMeisterwerke',ha='right',va='top',fontsize=9)
fig.savefig(os.path.join(HERE,'Zeichnung_Blende_2A35M.pdf')); fig.savefig(os.path.join(HERE,'Zeichnung_Blende_2A35M.png'),dpi=110)
print('Zeichnung geschrieben; Bohrungen je Feld/Ø:',dict(cnt))
