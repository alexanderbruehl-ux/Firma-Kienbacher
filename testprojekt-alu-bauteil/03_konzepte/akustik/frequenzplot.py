"""Schematischer Frequenzgang: idealer (linearer) Lautsprecher + Einfügedämpfung der Lochblende.
Modell: Lochplatte als akustische Masse (Massengesetz), TL = 10·log10(1 + (ω·m/(2ρc))²),
m = ρ·t_eff/σ, t_eff = t + 0,85·d·(1 − 0,7·√σ) (Mündungskorrektur mit Wechselwirkung benachbarter Löcher).
Weichen schematisch (leistungskomplementär, 4. Ordnung): Sub/TMT 100 Hz, TMT/HT 2,5 kHz."""
import numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
c=343.0
f=np.logspace(np.log10(20),np.log10(20000),600)
def tl(sigma,t_mm,d_mm):
    teff=(t_mm+0.85*d_mm*(1-0.7*np.sqrt(sigma)))/1000
    X=2*np.pi*f*teff/(sigma*c)
    return 10*np.log10(1+(X/2)**2)
def system(hts,tmt,sub,f1=100,f2=2500):
    w_sub=1/(1+(f/f1)**4); w_ht=1/(1+(f2/f)**4); w_tmt=np.clip(1-w_sub-w_ht,0,1)
    p=w_sub*10**(-sub/10)+w_tmt*10**(-tmt/10)+w_ht*10**(-hts/10)
    return 10*np.log10(p)
# Kennwerte (offen σ, Restwand t, mittlerer Loch-Ø d)
old =system(tl(0.238,2.2,1.30),tl(0.274,2.2,1.9),tl(0.283,2.2,2.0))
new =system(tl(0.288,2.2,2.25),tl(0.351,2.2,3.0),tl(0.357,2.2,3.0))
new15=system(tl(0.288,1.5,2.25),tl(0.351,2.2,3.0),tl(0.357,2.2,3.0))
S1,S2,S3='#2a78d6','#eb6834','#1baf7a'; INK='#0b0b0b'; INK2='#52514e'; GRID='#e4e3df'; SURF='#fcfcfb'
fig,ax=plt.subplots(figsize=(12,6.2),dpi=150); fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
for x0,x1,lab in ((20,100,'Subwoofer W 130 X'),(100,2500,'Tiefmitteltöner KT 100 V'),(2500,20000,'Hochtöner BF 32')):
    ax.text(np.sqrt(x0*x1),1.35,lab,ha='center',va='center',fontsize=10,color=INK2)
for x in (100,2500): ax.axvline(x,color=GRID,lw=1,zorder=0)
ax.plot(f,np.zeros_like(f),color=INK2,lw=2,ls=(0,(5,3)),label='idealer Lautsprecher ohne Blende (linear)')
ax.plot(f,old,color=S2,lw=2,label='Sonnenblume bisher (27,8 % offen, Ø 1,0–2,5, Haut 2,2 mm)')
ax.plot(f,new,color=S1,lw=2,label='Sonnenblume optimiert 2A-35 (35,1 % offen, Ø 2,0–3,5, Haut 2,2 mm)')
ax.plot(f,new15,color=S3,lw=2,label='2A-35 mit Hochtöner-Haut 1,5 mm')
for y,col,txt in ((old[-1],S2,f"{old[-1]:.1f} dB"),(new[-1],S1,f"{new[-1]:.1f} dB"),(new15[-1],S3,f"{new15[-1]:.1f} dB")):
    ax.annotate(txt,(20000,y),xytext=(6,0),textcoords='offset points',va='center',fontsize=10,color=INK)
    ax.plot([20000],[y],'o',ms=5,color=col,mec=SURF,mew=1.5,zorder=5)
i10=np.argmin(abs(f-10000))
ax.annotate(f"10 kHz: {new[i10]:.1f} dB (2A-35)\n{new15[i10]:.1f} dB (HT-Haut 1,5 mm)",(10000,new[i10]),xytext=(-170,-40),textcoords='offset points',fontsize=10,color=INK,arrowprops=dict(arrowstyle='-',color=INK2,lw=0.8))
ax.set_xscale('log'); ax.set_xlim(20,20000); ax.set_ylim(-8,2)
ax.set_xticks([20,50,100,200,500,1000,2000,5000,10000,20000]); ax.set_xticklabels(['20','50','100','200','500','1k','2k','5k','10k','20k'])
ax.set_xlabel('Frequenz [Hz]',color=INK2); ax.set_ylabel('Pegel relativ zum idealen Lautsprecher [dB]',color=INK2)
ax.grid(True,which='major',color=GRID,lw=0.8); ax.grid(True,which='minor',axis='x',color=GRID,lw=0.4,alpha=0.6)
for s in ax.spines.values(): s.set_color(GRID)
ax.tick_params(colors=INK2)
ax.set_title('Schematischer Frequenzgang: idealer Lautsprecher mit Alu-Lochblende „Sonnenblume“',color=INK,fontsize=13,loc='left',pad=14)
ax.legend(loc='lower left',frameon=False,fontsize=10,labelcolor=INK)
fig.text(0.01,0.012,'Modell: Lochplatte als akustische Masse (Massengesetz, Mündungskorrektur), Weichen schematisch 100 Hz / 2,5 kHz (leistungskomplementär).\nOhne Raum-, Kammer- und Beugungseffekte – nur zum Vergleich der Blenden, keine Messung.',fontsize=8.5,color=INK2)
fig.tight_layout(rect=(0,0.05,1,1)); fig.savefig('Frequenzplot_Sonnenblume.png',facecolor=SURF)
for nm,v in (('bisher',old),('2A-35',new),('2A-35 HT 1,5',new15)):
    print(nm,' '.join(f"{fq}Hz:{v[np.argmin(abs(f-fq))]:.2f}" for fq in (1000,5000,10000,15000,20000)))
