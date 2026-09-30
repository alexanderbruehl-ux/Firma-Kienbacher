"""Schematischer Frequenzgang: idealer (linearer) Lautsprecher + Einfügedämpfung der Lochblende.
Lochplatte als akustische Masse: TL = 10·log10(1 + (X/2)²), X = ω·t_eff/(σ·c), t_eff = t + 0,85·d·(1 − 0,7·√σ).
Hochtöner: σ frequenzabhängig gewichtet mit dem radialen Offen-Profil des Feldes (Rasterung) und einer
Bündelungsgewichtung w_f(r) = exp(−(r/r_f)²), r_f = R·(0,2 + 0,8/√(1+(f/f_ka)²)), f_ka = c/(2π·16 mm) ≈ 3,4 kHz:
je höher die Frequenz, desto stärker zählt die Feldmitte.
Weichen schematisch (leistungskomplementär, 4. Ordnung): Sub/TMT 100 Hz, TMT/HT 2,5 kHz."""
import json, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
c=343.0; f=np.logspace(np.log10(20),np.log10(20000),600)
J=json.load(open('ht_profile.json')); r=np.array(J['r']); dA=2*np.pi*r*(r[1]-r[0])
def sigma_eff(prof):
    prof=np.array(prof); fka=c/(2*np.pi*0.016); out=[]
    for fi in f:
        rf=23.1*(0.2+0.8/np.sqrt(1+(fi/fka)**2)); w=np.exp(-(r/rf)**2)*dA
        out.append(np.sum(prof*w)/np.sum(w))
    return np.array(out)
def tl(sigma,t_mm,d_mm):
    teff=(t_mm+0.85*d_mm*(1-0.7*np.sqrt(sigma)))/1000
    return 10*np.log10(1+((2*np.pi*f*teff/(sigma*c))/2)**2)
def system(ht,tmt,sub,f1=100,f2=2500):
    ws=1/(1+(f/f1)**4); wh=1/(1+(f2/f)**4); wt=np.clip(1-ws-wh,0,1)
    return 10*np.log10(ws*10**(-sub/10)+wt*10**(-tmt/10)+wh*10**(-ht/10))
tmt_old,sub_old=tl(0.274,2.2,1.9),tl(0.283,2.2,2.0)
tmt_new,sub_new=tl(0.351,2.2,3.0),tl(0.357,2.2,3.0)
curves=[
 ('Sonnenblume bisher (Ø 0,7–1,6 im HT, Haut 2,2 mm)', system(tl(sigma_eff(J['bisher']),2.2,1.2),tmt_old,sub_old), '#eb6834'),
 ('2A-35 optimiert (Haut 2,2 mm)',                    system(tl(sigma_eff(J['ohneM']),2.2,2.25),tmt_new,sub_new), '#2a78d6'),
 ('2A-35, Hochtöner-Haut 1,5 mm',                     system(tl(sigma_eff(J['ohneM']),1.5,2.25),tmt_new,sub_new), '#1baf7a'),
 ('2A-35, HT-Haut 1,5 mm + ausgefrästes Signet-M',   system(tl(sigma_eff(J['mitM']),1.5,2.2),tmt_new,sub_new),  '#4a3aa7'),
]
INK='#0b0b0b'; INK2='#52514e'; GRID='#e4e3df'; SURF='#fcfcfb'
fig,ax=plt.subplots(figsize=(12,6.6),dpi=150); fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
for x0,x1,lab in ((20,100,'Subwoofer W 130 X'),(100,2500,'Tiefmitteltöner KT 100 V'),(2500,20000,'Hochtöner BF 32')):
    ax.text(np.sqrt(x0*x1),1.35,lab,ha='center',va='center',fontsize=10,color=INK2)
for x in (100,2500): ax.axvline(x,color=GRID,lw=1,zorder=0)
ax.plot(f,np.zeros_like(f),color=INK2,lw=2,ls=(0,(5,3)),label='idealer Lautsprecher ohne Blende (linear)')
ends=[]
for lab,y,col in curves:
    ax.plot(f,y,color=col,lw=2.6 if 'Signet' in lab else 2,label=lab); ends.append((y[-1],col))
# Endwerte mit Mindestabstand beschriften
ends=sorted(ends); yl=[]
for y,col in ends:
    yy=y if not yl or y-yl[-1]>=0.32 else yl[-1]+0.32; yl.append(yy)
    ax.plot([20000],[y],'o',ms=5,color=col,mec=SURF,mew=1.5,zorder=5)
    ax.annotate(f"{y:.1f} dB",(20000,y),xytext=(22500,yy),textcoords='data',va='center',fontsize=10,color=INK,annotation_clip=False)
i10=np.argmin(abs(f-10000)); yM=curves[3][1]; y15=curves[2][1]
ax.annotate(f"10 kHz: Signet-M {yM[i10]:.1f} dB\nohne M {y15[i10]:.1f} dB",(10000,yM[i10]),xytext=(-190,-44),textcoords='offset points',fontsize=10,color=INK,arrowprops=dict(arrowstyle='-',color=INK2,lw=0.8))
ax.set_xscale('log'); ax.set_xlim(20,20000); ax.set_ylim(-14,2)
ax.set_xticks([20,50,100,200,500,1000,2000,5000,10000,20000]); ax.set_xticklabels(['20','50','100','200','500','1k','2k','5k','10k','20k'])
ax.set_xlabel('Frequenz [Hz]',color=INK2); ax.set_ylabel('Pegel relativ zum idealen Lautsprecher [dB]',color=INK2)
ax.grid(True,which='major',color=GRID,lw=0.8); ax.grid(True,which='minor',axis='x',color=GRID,lw=0.4,alpha=0.6)
for s in ax.spines.values(): s.set_color(GRID)
ax.tick_params(colors=INK2)
ax.set_title('Schematischer Frequenzgang: idealer Lautsprecher mit Alu-Lochblende „Sonnenblume“ – Optimierungsstufen',color=INK,fontsize=13,loc='left',pad=14)
ax.legend(loc='lower left',frameon=False,fontsize=10,labelcolor=INK)
fig.text(0.01,0.012,'Modell: Lochplatte als akustische Masse (Massengesetz, Mündungskorrektur); Hochtöner mit radialem Offen-Profil und Bündelungsgewichtung (Mitte zählt bei hohen Frequenzen mehr).\nWeichen schematisch 100 Hz / 2,5 kHz. Ohne Raum-, Kammer- und Beugungseffekte – nur zum Vergleich der Blenden, keine Messung.',fontsize=8.5,color=INK2)
fig.tight_layout(rect=(0,0.05,0.97,1)); fig.savefig('Frequenzplot_Sonnenblume.png',facecolor=SURF)
for lab,y,_ in curves: print(f"{lab:50s} "+'  '.join(f"{fq//1000}k:{y[np.argmin(abs(f-fq))]:.2f}" for fq in (5000,10000,15000,20000)))
