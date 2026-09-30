"""Meisterwerke-Logo (nachgezeichnet): Signet 'M' aus zwei verschränkten Spitzen + Wortmarke MEISTERWERKE.
Einheiten: Signethöhe = 153 (gemessen am Referenzbild), Ursprung links oben der Gesamtmarke."""
import numpy as np, os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.recordingPen import DecomposingRecordingPen
HERE=os.path.dirname(os.path.abspath(__file__))  # Cinzel.ttf liegt daneben (SIL Open Font License, siehe Cinzel_OFL.txt)
FONT=os.path.join(HERE,'Cinzel.ttf')
# --- Signet (Koordinaten aus Messung, y nach unten) ---
def _peak(apex_x, left_foot, right_foot, wl, wr, top=37.0, base=190.0):
    ax,ay=apex_x,top
    def xat(p0,p1,y): return p0[0]+(p1[0]-p0[0])*(y-p0[1])/(p1[1]-p0[1])
    oL=(left_foot,base); oR=(right_foot,base)
    iL=(left_foot+wl,base); iR=(right_foot-wr,base)
    # innere Spitze = Schnitt der Innenkanten (parallel zu den Außenkanten)
    dL=np.array([ax-oL[0],ay-oL[1]]); dR=np.array([ax-oR[0],ay-oR[1]])
    A=np.array([dL,-dR]).T; t=np.linalg.solve(A,np.array(iR)-np.array(iL))
    inner=np.array(iL)+t[0]*dL
    return [oL,(ax,ay),oR,iR,tuple(inner),iL]
SIGNET=[ _peak(746.0,680.0,812.0,11.0,14.0), _peak(813.0,747.0,879.0,11.0,14.0) ]
SIG_X0,SIG_Y0,SIG_W,SIG_H=680.0,37.0,199.0,153.0
# Wortmarke: Kapitälchenhöhe 99, Breite 1455, oben bei y=262, links bei x=55
WM_X0,WM_Y0,WM_W,WM_CAP=55.0,262.0,1455.0,99.0
TEXT="MEISTERWERKE"
def _glyphs():
    f=TTFont(FONT); gs=f.getGlyphSet(); cmap=f.getBestCmap(); upm=f['head'].unitsPerEm
    cap=f['OS/2'].sCapHeight or 0.7*upm
    names=[cmap[ord(c)] for c in TEXT]
    adv=[f['hmtx'][n][0] for n in names]
    s=WM_CAP/cap
    natural=sum(adv[:-1])*s+ (gs[names[-1]].width*s)
    # Sperrung so, dass die Gesamtbreite 1455 erreicht wird (Glyphenbreite des letzten Zeichens mitgezählt)
    track=(WM_W-natural)/(len(TEXT)-1)
    return f,gs,names,adv,s,track
def svg(path, color='#1b2a4a', with_signet=True, with_wordmark=True):
    f,gs,names,adv,s,track=_glyphs()
    parts=[]
    if with_signet:
        for poly in SIGNET:
            parts.append('<path d="M'+' L'.join(f'{x:.2f},{y:.2f}' for x,y in poly)+' Z"/>')
    if with_wordmark:
        x=WM_X0
        for n,a in zip(names,adv):
            pen=SVGPathPen(gs)
            tp=TransformPen(pen,(s,0,0,-s,x,WM_Y0+WM_CAP))
            gs[n].draw(tp); parts.append(f'<path d="{pen.getCommands()}"/>')
            x+=a*s+track
    x0=WM_X0 if with_wordmark else SIG_X0; y0=SIG_Y0 if with_signet else WM_Y0
    x1=WM_X0+WM_W if with_wordmark else SIG_X0+SIG_W; y1=WM_Y0+WM_CAP if with_wordmark else SIG_Y0+SIG_H
    pad=10
    open(path,'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0-pad} {y0-pad} {x1-x0+2*pad} {y1-y0+2*pad}"><g fill="{color}">'+''.join(parts)+'</g></svg>')
def draw(draw_polygon, draw_text_glyph_polys, to_px, x_mm, y_mm, width_mm, fill, with_wordmark=True):
    """Zeichnet das Logo mit Zentrum (x_mm,y_mm) und Gesamtbreite width_mm über Callback-Funktionen."""
    f,gs,names,adv,s,track=_glyphs()
    bx0,bx1=(WM_X0,WM_X0+WM_W) if with_wordmark else (SIG_X0,SIG_X0+SIG_W)
    by0,by1=SIG_Y0,(WM_Y0+WM_CAP) if with_wordmark else SIG_Y0+SIG_H
    k=width_mm/(bx1-bx0); cx,cy=(bx0+bx1)/2,(by0+by1)/2
    M=lambda u,v:to_px((x_mm+(u-cx)*k, y_mm-(v-cy)*k))
    for poly in SIGNET: draw_polygon([M(u,v) for u,v in poly])
    if with_wordmark:
        from fontTools.pens.basePen import BasePen
        class Flat(BasePen):
            def __init__(s2,gs): super().__init__(gs); s2.polys=[];s2.cur=[]
            def _moveTo(s2,p): s2.cur=[p]
            def _lineTo(s2,p): s2.cur.append(p)
            def _curveToOne(s2,p1,p2,p3):
                p0=s2.cur[-1]
                for t in np.linspace(0,1,9)[1:]:
                    s2.cur.append(tuple((1-t)**3*np.array(p0)+3*(1-t)**2*t*np.array(p1)+3*(1-t)*t*t*np.array(p2)+t**3*np.array(p3)))
            def _closePath(s2): s2.polys.append(s2.cur); s2.cur=[]
        x=WM_X0
        for n,a in zip(names,adv):
            fp=Flat(gs); tp=TransformPen(fp,(s,0,0,-s,x,WM_Y0+WM_CAP)); gs[n].draw(tp)
            draw_text_glyph_polys([[M(u,v) for u,v in p] for p in fp.polys])
            x+=a*s+track
    return k*(by1-by0)   # Höhe in mm
