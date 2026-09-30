"""Meisterwerke-Logo – aus der Original-Bilddatei vektorisiert (trace_logo.py, Potrace), keine Fremdschrift.
Pfade in mw_trace.json (Einheit: Pixel der Vorlage 1024x266, y nach unten)."""
import json, os, re, numpy as np
HERE=os.path.dirname(os.path.abspath(__file__))
_T=json.load(open(os.path.join(HERE,'mw_trace.json')))
BBOX_ALL=_T['bbox_all']; BBOX_SIG=_T['bbox_signet']; BBOX_WM=_T['bbox_wordmark']
ASPECT=(BBOX_ALL[2]-BBOX_ALL[0])/(BBOX_ALL[3]-BBOX_ALL[1])     # Breite/Höhe Gesamtmarke
def _subpaths(d, steps=10):
    """SVG-Pfad (M/L/C/Z, absolut) -> Liste geschlossener Polygone."""
    toks=re.findall(r'[MLCZ]|-?\d+\.?\d*',d); i=0; polys=[]; cur=[]; cmd=None
    def num():
        nonlocal i; v=float(toks[i]); i+=1; return v
    while i<len(toks):
        t=toks[i]
        if t in 'MLCZ': cmd=t; i+=1
        if cmd=='M': cur=[(num(),num())]
        elif cmd=='L': cur.append((num(),num()))
        elif cmd=='C':
            p0=np.array(cur[-1]); p1=np.array((num(),num())); p2=np.array((num(),num())); p3=np.array((num(),num()))
            for t_ in np.linspace(0,1,steps+1)[1:]:
                cur.append(tuple((1-t_)**3*p0+3*(1-t_)**2*t_*p1+3*(1-t_)*t_*t_*p2+t_**3*p3))
        elif cmd=='Z':
            polys.append(cur); cur=[]
    return polys
SIGNET=_subpaths(_T['signet']); WORDMARK=_subpaths(_T['wordmark'])
def svg(path,color='#1b2a4a',with_signet=True,with_wordmark=True):
    parts=([_T['signet']] if with_signet else [])+([_T['wordmark']] if with_wordmark else [])
    bb=BBOX_ALL if (with_signet and with_wordmark) else (BBOX_SIG if with_signet else BBOX_WM); p=4
    open(path,'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{bb[0]-p:.2f} {bb[1]-p:.2f} {bb[2]-bb[0]+2*p:.2f} {bb[3]-bb[1]+2*p:.2f}"><g fill="{color}" fill-rule="evenodd">'+''.join(f'<path d="{d}"/>' for d in parts)+'</g></svg>')
def draw(draw_polygon, draw_text_glyph_polys, to_px, x_mm, y_mm, width_mm, fill, with_wordmark=True, angle_deg=0.0, signet_only=False):
    """Zeichnet das Logo: Zentrum (x_mm,y_mm) der Gesamtmarke, Gesamtbreite width_mm, Drehung angle_deg (gegen UZS).
    draw_polygon(pts) für das Signet, draw_text_glyph_polys(list_of_polys) für die Wortmarke (gerade/ungerade füllen).
    Gibt die Höhe der Gesamtmarke in mm zurück."""
    bx0,by0,bx1,by1=BBOX_ALL
    k=width_mm/(bx1-bx0); cx,cy=(bx0+bx1)/2,(by0+by1)/2
    ca,sa=np.cos(np.radians(angle_deg)),np.sin(np.radians(angle_deg))
    def M(u,v):
        dx,dy=(u-cx)*k,-(v-cy)*k
        return to_px((x_mm+dx*ca-dy*sa, y_mm+dx*sa+dy*ca))
    draw_text_glyph_polys([[M(u,v) for u,v in p] for p in SIGNET]) if len(SIGNET)>1 else draw_polygon([M(u,v) for u,v in SIGNET[0]])
    if with_wordmark and not signet_only:
        draw_text_glyph_polys([[M(u,v) for u,v in p] for p in WORDMARK])
    return k*(by1-by0)
