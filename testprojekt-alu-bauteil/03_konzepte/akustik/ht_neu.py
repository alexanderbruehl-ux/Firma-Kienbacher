"""Frequenzgang mit dem neuen Hochtöner-Feld (101 Bohrungen, M +1,5 mm): Offen-Profil aus ht_neu_loecher.json, sonst Modell wie frequenzplot.py"""
import json, sys, math, numpy as np
sys.path.insert(0,'../../04_cad/blende')
src=open('frequenzplot.py').read().split("tmt_old,sub_old")[0]      # Funktionen/Daten aus frequenzplot.py
exec(src)
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import signet_m
H=json.load(open('ht_neu_loecher.json')); DYM=H['dy']
D=46.2; RES=0.02; N=int(D/RES)+20; C=N//2; P=lambda x,y:(C+x/RES,C-y/RES)
im=Image.new('L',(N,N),0); d=ImageDraw.Draw(im)
# M im Achsensystem: wie im Bauteil (um 3,5° geneigt) – für das Profil zählt nur die Fläche; M wird um DYM nach oben geschoben, Mitte 0/0
M=signet_m.signet_poly(28.0,0,0); 
d.polygon([P(x,y+DYM) for x,y in M],fill=255)
for x,y,dd in H['holes']:
    X,Y=P(x,y); r=dd/2/RES; d.ellipse([X-r,Y-r,X+r,Y+r],fill=255)
a=np.asarray(im)>0; yy,xx=np.mgrid[0:N,0:N]; rr=np.hypot(xx-C,yy-C)*RES
field=rr<=D/2; open_pct=a[field].mean()*100
prof=[]; rr_=np.array(J['r']); dr_=rr_[1]-rr_[0]; edges=np.append(rr_-dr_/2,rr_[-1]+dr_/2)
for i in range(len(J['r'])):
    m=(rr>=edges[i])&(rr<edges[i+1]); prof.append(a[m].mean())
dmean=np.average([h[2] for h in H['holes']])
tmt_new,sub_new=tl(0.351,2.2,3.0),tl(0.357,2.2,3.0)
cur=[('2A-35, HT-Haut 1,5 mm + Signet-M (bisheriges Feld, 69 Bohrungen)',system(tl(sigma_eff(J['mitM']),1.5,2.2),tmt_new,sub_new),'#4a3aa7'),
     ('NEU: 101 Bohrungen, M 1,5 mm höher, %.0f %% offen'%open_pct,system(tl(sigma_eff(prof),1.5,2.45),tmt_new,sub_new),'#d6336c')]
ideal=np.zeros_like(f)
fig,ax=plt.subplots(figsize=(12,6.4),dpi=130)
ax.plot(f,ideal,color='#52514e',lw=2,ls=(0,(5,3)),label='idealer Lautsprecher ohne Blende')
for lab,y,col in cur: ax.plot(f,y,color=col,lw=2.4,label=lab)
for x in (100,2500): ax.axvline(x,color='#e4e3df',lw=1)
ax.set_xscale('log'); ax.set_xlim(20,20000); ax.set_ylim(-6,1.5); ax.set_xticks([20,50,100,200,500,1000,2000,5000,10000,20000]); ax.set_xticklabels(['20','50','100','200','500','1k','2k','5k','10k','20k'])
ax.set_xlabel('Frequenz [Hz]'); ax.set_ylabel('Pegel relativ zum idealen Lautsprecher [dB]'); ax.grid(True,which='major',color='#e4e3df'); ax.legend(loc='lower left',frameon=False,fontsize=10)
ax.set_title('Schematischer Frequenzgang mit dem neuen Hochtöner-Feld',loc='left')
for lab,y,col in cur: print(lab, '  '.join('%dk: %.2f dB'%(fq//1000,y[np.argmin(abs(f-fq))]) for fq in (5000,10000,15000,20000)))
fig.tight_layout(); fig.savefig('Frequenzplot_Hochtoener_neu.png',facecolor='white'); print('offen gesamt %.1f %%'%open_pct,'mittlerer Lochdurchmesser %.2f'%dmean)
