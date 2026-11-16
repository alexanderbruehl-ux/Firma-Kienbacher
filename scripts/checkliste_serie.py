import sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule
OUT=sys.argv[1]
F='Arial'
def font(**k): return Font(name=F, size=k.pop('size',10), **k)
dünn=Side(style='thin', color='9FB3BF'); RAND=Border(left=dünn,right=dünn,top=dünn,bottom=dünn)
GELB=PatternFill('solid', fgColor='FFF4C2'); KOPF=PatternFill('solid', fgColor='D9E6EE'); ABS=PatternFill('solid', fgColor='EEF3F6')
WRAP=Alignment(wrap_text=True, vertical='top'); MITTE=Alignment(horizontal='center', vertical='top', wrap_text=True)
wb=Workbook(); ws=wb.active; ws.title='Checkliste'
for col,w in zip('ABCDEFG',[5,52,26,20,17,33,12]): ws.column_dimensions[col].width=w
ws['A1']='Checkliste Übernahme in die Serie'; ws['A1'].font=font(size=16,bold=True,color='00435C')
ws['F1']='Produktion · intern'; ws['F1'].font=font(size=9,color='666666'); ws['F1'].alignment=Alignment(horizontal='right')
ws.merge_cells('F1:G1')
ws['A2']='Grundlage: 7V-3-1 Vers. N, 7.3.4.8 Entwicklungsausgaben und 7.3.4.10 Serienfreigabe. Das Ergebnis geht in das Prozessreview 7F-34-1 ein, das die Produktion mitzeichnet.'
ws['A2'].font=font(size=9,color='555555'); ws.merge_cells('A2:G2')
felder=[('Projekt / Artikelbezeichnung','Kunde'),('Artikel-Nr.','Werkzeug-Nr.'),('Maschine (Haupt / Ausweich)','Serienstart geplant'),('Prozessreview am','Ausgefüllt von')]
for i,(l1,l2) in enumerate(felder):
    r=4+i
    ws.cell(r,1,l1).font=font(bold=True); ws.merge_cells(start_row=r,start_column=1,end_row=r,end_column=2)
    ws.cell(r,1).alignment=Alignment(horizontal='right',vertical='center')
    ws.cell(r,3).fill=GELB; ws.merge_cells(start_row=r,start_column=3,end_row=r,end_column=4)
    ws.cell(r,5,l2).font=font(bold=True); ws.cell(r,5).alignment=Alignment(horizontal='right',vertical='center',wrap_text=True)
    ws.cell(r,6).fill=GELB; ws.merge_cells(start_row=r,start_column=6,end_row=r,end_column=7)
    for c in range(3,8):
        if c!=5: ws.cell(r,c).border=RAND
    ws.row_dimensions[r].height=20
ws['A9']=('Ausfüllen: gelbe Felder. Status je Punkt aus der Liste wählen: erfüllt / offen / n. z. (nicht zutreffend). '
          'Bei „offen“ Maßnahme und Termin eintragen. „Verantwortlich“ = Bereich, der den Punkt prüft und bestätigt (Vorschlag, siehe Blatt Hinweise).')
ws['A9'].font=font(size=9,italic=True,color='555555'); ws['A9'].alignment=WRAP; ws.merge_cells('A9:G9'); ws.row_dimensions[9].height=26
KOPFZ=11
for c,t in enumerate(['Nr','Kriterium','Nachweis','Verantwortlich','Status','Bemerkung / Maßnahme','Termin'],1):
    x=ws.cell(KOPFZ,c,t); x.font=font(bold=True); x.fill=KOPF; x.border=RAND; x.alignment=MITTE if c in (1,5,7) else WRAP
P=[('A','Unterlagen und Freigaben',[
 ('Zeichnung, Stückliste und Materialspezifikation liegen freigegeben vor','Zeichnungsindex, Stückliste (liefert PT)','Prozesstechnik'),
 ('Produktfreigabe des Kunden liegt vor (Erstbemusterung)','Erstmusterprüfbericht / PPAP','PT / QM'),
 ('Besondere Merkmale sind bekannt und in Lenkungsplan und artikelbezogener Arbeitsanweisung gekennzeichnet','FMEA, Lenkungsplan, Arbeitsanweisung','PT / RPP'),
 ('Artikelstamm und Arbeitsplan sind im ERP-System (FOSS) angelegt (Kavitäten, Material, Trocknung, Verpackung)','Arbeitsplan im ERP-System (FOSS, ARPL)','Produktionsplanung')]),
 ('B','Werkzeug',[
 ('Werkzeug ist abgenommen, Mängel aus der Bemusterung sind behoben','Werkzeugabnahmeprotokoll, Musterbericht','Prozesstechnik / Werkzeugbau'),
 ('Werkzeug ist als Objekt im ERP-System (FOSS) bzw. MES angelegt (Werkzeug-Nr., Kavitäten, Einbaumaße, Heißkanal, Kühlplan)','Objektstammdaten ERP-System (FOSS) / MES','Digitale Prozessentwicklung / Werkzeugbau'),
 ('Wartungsplan für das Werkzeug ist angelegt (Intervall in Schuss)','Wartungsplan','Werkzeugbau'),
 ('Kritische Verschleiß- und Ersatzteile sind festgelegt und verfügbar','Ersatzteilliste','Werkzeugbau')]),
 ('C','Maschine, Peripherie und Prozess',[
 ('Haupt- und Ausweichmaschine sind festgelegt, die Ausweichmaschine ist mitbemustert','Musterbericht, Arbeitsplan im ERP-System (FOSS)','Prozesstechnik / Produktionsplanung'),
 ('Prozessparameter sind freigegeben und in der Maschine gespeichert','Einstelldatenblatt','Prozesstechnik'),
 ('Rüstanleitung liegt vor','Rüstanleitung','Prozesstechnik'),
 ('Peripherie und Automatisierung sind abgenommen; bei integrierten Gesamtanlagen liegt die CE-Konformität vor','Inbetriebnahme, CE-Dokumentation','Automatisierung'),
 ('Neue Anlagen und Betriebsmittel sind als Objekt im ERP-System (FOSS) angelegt, Wartung und kritische Ersatzteile festgelegt','Objektstammdaten ERP-System (FOSS), Wartungsplan','Instandhaltung')]),
 ('D','Leistung und Fähigkeit',[
 ('Run@Rate unter Serienbedingungen bestanden: Zykluszeit und Ausbringung erreicht','Run@Rate-Protokoll','Prozesstechnik'),
 ('Maschinenzeit ist festgelegt: Rüstzeit und Zykluszeit aus dem Run@Rate, im Arbeitsplan im ERP-System (FOSS) hinterlegt','Arbeitsplan im ERP-System (FOSS, ARPL), Run@Rate-Protokoll','Prozesstechnik / Produktionsplanung'),
 ('Ausschuss im Run@Rate innerhalb der Vorgabe','Run@Rate-Protokoll','Prozesstechnik'),
 ('Vorläufige Prozessfähigkeit für besondere Merkmale nachgewiesen (laut Kundenvorgabe, sonst Ppk ≥ 1,67)','Fähigkeitsnachweis','QM / RPP'),
 ('Kapazität für den Serienstart ist eingeplant und in der Kapazitäts- und Planungsabstimmung (aktuell KPLI) abgestimmt','Maschinenbelegung','Produktionsplanung'),
 ('Falls vor Abschluss des Run@Rate vorproduziert wird: Risiko bewusst entschieden und festgehalten (vergleichbar Interim Approval)','Prozessreview / Aktennotiz','Produktionsleitung')]),
 ('E','Qualität am Arbeitsplatz',[
 ('Lenkungsplan für Vorserie bzw. Serie ist freigegeben','Lenkungsplan','PT / RPP'),
 ('Prüfungen sind in der artikelbezogenen Arbeitsanweisung festgelegt (Merkmale, Häufigkeit, Prüfmittel); Prüfmittel sind freigegeben (Messsystemanalyse)','Arbeitsanweisung (artikelbezogen), MSA','Prozesstechnik / QS'),
 ('Produktionsfreigabemuster liegt am Arbeitsplatz; ab der ersten Serienproduktion zusätzlich das Rückstellmuster der letzten Produktion','Produktionsfreigabemuster, Rückstellmuster','QS'),
 ('Reaktionsplan bei Fehlern ist festgelegt und den Schichtführern bekannt','Reaktionsplan','QS / Teamleitung'),
 ('Poka-Yoke-Verifizierung (Dummy-Prüfung) ist eingerichtet: Referenzteile und Intervall festgelegt, falls vorgesehen','Referenzteile, Prüfintervall','Prozesstechnik / QS')]),
 ('F','Mitarbeitende, Arbeitssicherheit und Umwelt',[
 ('Artikelbezogene Arbeitsanweisung liegt aktuell und verständlich am Arbeitsplatz','Arbeitsanweisung (artikelbezogen)','Prozesstechnik'),
 ('Mitarbeitende sind geschult, der Nachweis ist in DocuWare abgelegt','6F-22-6','Teamleitung'),
 ('Neue Arbeitsstoffe: Sicherheitsdatenblatt im Gefahrstoffkataster, Betriebsanweisung ausgehängt, Unterweisung dokumentiert','SDB, Betriebsanweisung, 6F-22-6','Produktionsleitung'),
 ('PSA ist festgelegt und verfügbar, Arbeitsplatzevaluierung bei neuer Tätigkeit aktualisiert','Evaluierung, PSA-Ausgabeliste','Produktionsleitung'),
 ('Entsorgung bzw. Rückführung von Ausschuss, Angüssen und Mahlgut ist geklärt','Abfall- bzw. Mahlgutregelung','Produktionsleitung')]),
 ('G','Logistik und Verpackung',[
 ('Verpackungsvorschrift liegt vor, Verpackung ist verfügbar','Verpackungsvorschrift','Logistik'),
 ('Material für den Serienstart ist gesichert (Rohmaterial, Farbe, Zukaufteile)','Bestellung / Bestand','Logistik / Einkauf'),
 ('Kennzeichnung und Etiketten (Kundenlabel) sind eingerichtet','Etikettenmuster','Logistik')]),
 ('H','Anlauf',[
 ('Anlaufbetreuung ist festgelegt: verantwortliche Person, Dauer, erhöhte Prüfumfänge','Anlaufplan','Prozesstechnik / QS'),
 ('Prüfbegleitkarte für den Artikel ist angelegt (Erststück-/Letztstückfreigabe)','Prüfbegleitkarte','Teamleitung / PQB'),
 ('Offene Punkte aus Bemusterung und Prozessreview sind mit Maßnahme, Verantwortlichem und Termin erfasst','Prozessreview-Workflow (7F-34-1)','PT')])]
r=KOPFZ+1; nr=0; erste=r
from openpyxl.worksheet.pagebreak import Break
for buchst,titel,punkte in P:
    if buchst in ('D','G'): ws.row_breaks.append(Break(id=r-1))
    ws.cell(r,1,f'{buchst}  {titel}').font=font(bold=True,color='00435C'); ws.cell(r,1).fill=ABS
    ws.merge_cells(start_row=r,start_column=1,end_row=r,end_column=7)
    for c in range(1,8): ws.cell(r,c).border=RAND
    r+=1
    for krit,nachweis,verantw in punkte:
        nr+=1
        werte=[nr,krit,nachweis,verantw,None,None,None]
        for c,v in enumerate(werte,1):
            x=ws.cell(r,c,v); x.font=font(); x.border=RAND; x.alignment=MITTE if c in (1,5,7) else WRAP
            if c in (5,6,7): x.fill=GELB
        ws.cell(r,7).number_format='DD.MM.YYYY'
        zl=max(-(-len(krit)//54), -(-len(nachweis)//27), -(-len(verantw)//19), 1)
        ws.row_dimensions[r].height=max(15.5, 12.8*zl+2)
        r+=1
letzte=r-1
dv=DataValidation(type='list', formula1='"erfüllt,offen,n. z."', allow_blank=True, showErrorMessage=True,
                  errorTitle='Status', error='Bitte erfüllt, offen oder n. z. wählen.')
ws.add_data_validation(dv); dv.add(f'E{erste}:E{letzte}')
rng=f'E{erste}:E{letzte}'
ws.conditional_formatting.add(rng, FormulaRule(formula=[f'E{erste}="erfüllt"'], fill=PatternFill('solid',fgColor='C6EFCE'), font=Font(name=F,color='006100')))
ws.conditional_formatting.add(rng, FormulaRule(formula=[f'E{erste}="offen"'], fill=PatternFill('solid',fgColor='FFC7CE'), font=Font(name=F,color='9C0006',bold=True)))
ws.conditional_formatting.add(rng, FormulaRule(formula=[f'E{erste}="n. z."'], fill=PatternFill('solid',fgColor='E7E6E6'), font=Font(name=F,color='595959')))
# Auswertung
r=letzte+2
ws.cell(r,2,'Auswertung').font=font(bold=True,size=11,color='00435C'); r+=1
aus=[('Punkte gesamt',f'=COUNT(A{erste}:A{letzte})'),('erfüllt',f'=COUNTIF(E{erste}:E{letzte},"erfüllt")'),
     ('offen',f'=COUNTIF(E{erste}:E{letzte},"offen")'),('n. z.',f'=COUNTIF(E{erste}:E{letzte},"n. z.")')]
zeilen={}
for lab,f in aus:
    ws.cell(r,2,lab).font=font(); ws.cell(r,2).alignment=Alignment(horizontal='right')
    x=ws.cell(r,3,f); x.font=font(bold=True); x.alignment=Alignment(horizontal='left'); zeilen[lab]=r; r+=1
ws.cell(r,2,'noch nicht bewertet').font=font(); ws.cell(r,2).alignment=Alignment(horizontal='right')
ws.cell(r,3,f'=C{zeilen["Punkte gesamt"]}-C{zeilen["erfüllt"]}-C{zeilen["offen"]}-C{zeilen["n. z."]}').font=font(bold=True)
ws.cell(r,3).alignment=Alignment(horizontal='left'); zeilen['nb']=r; r+=1
ws.cell(r,2,'Ergebnis').font=font(bold=True); ws.cell(r,2).alignment=Alignment(horizontal='right')
ws.cell(r,3,f'=IF(C{zeilen["offen"]}+C{zeilen["nb"]}=0,"Alle Punkte erfüllt oder nicht zutreffend",C{zeilen["offen"]}+C{zeilen["nb"]}&" Punkte offen oder nicht bewertet")').font=font(bold=True,color='00435C')
ws.merge_cells(start_row=r,start_column=3,end_row=r,end_column=6); r+=2
ws.cell(r,2,'Entscheidung der Produktion').font=font(bold=True,size=11,color='00435C'); r+=1
for t in ['☐  Übernahme in die Serie','☐  Übernahme mit Auflagen: offene Punkte siehe oben, Termine verbindlich','☐  keine Übernahme, erneutes Prozessreview am: ______________']:
    ws.cell(r,2,t).font=font(); ws.merge_cells(start_row=r,start_column=2,end_row=r,end_column=6); r+=1
r+=1
for c,t in enumerate(['Funktion','Name','Datum','Unterschrift'],2):
    x=ws.cell(r,c,t); x.font=font(bold=True); x.fill=KOPF; x.border=RAND
ws.merge_cells(start_row=r,start_column=5,end_row=r,end_column=6); r+=1
for fkt in ['Produktionsleitung','Prozesstechnik und Bemusterung','Werkzeugbau','Produktionsplanung','Instandhaltung / Automatisierung']:
    ws.cell(r,2,fkt).font=font()
    for c in range(2,7): ws.cell(r,c).border=RAND
    for c in (3,4,5): ws.cell(r,c).fill=GELB
    ws.merge_cells(start_row=r,start_column=5,end_row=r,end_column=6); ws.row_dimensions[r].height=24; r+=1
ws.freeze_panes=f'A{KOPFZ+1}'
ws.print_title_rows=f'{KOPFZ}:{KOPFZ}'
ws.page_setup.orientation='landscape'; ws.page_setup.paperSize=ws.PAPERSIZE_A4
ws.page_setup.fitToWidth=1; ws.page_setup.fitToHeight=0; ws.sheet_properties.pageSetUpPr.fitToPage=True
ws.page_margins.left=ws.page_margins.right=0.4; ws.page_margins.top=0.5; ws.page_margins.bottom=0.6
ws.oddFooter.left.text='Checkliste Übernahme in die Serie · Produktion · Stand 12.11.2026'; ws.oddFooter.left.size=8
ws.oddFooter.right.text='Seite &P von &N'; ws.oddFooter.right.size=8
# Hinweise
h=wb.create_sheet('Hinweise')
h.column_dimensions['A'].width=24; h.column_dimensions['B'].width=95
zeilen_h=[('Zweck','Die Produktion prüft vor der Serienfreigabe, ob ein Produkt serienreif ist, und bestätigt das im Prozessreview 7F-34-1 (7V-3-1 Vers. N, 7.3.4.10). Die Checkliste macht die Kriterien dafür einheitlich und nachvollziehbar.'),
 ('Wann','Spätestens zum Prozessreview vor der Serienfreigabe; bei Bedarf schon nach dem ersten Lauf mit dem Serienwerkzeug als Zwischenstand.'),
 ('Ausfüllen','Gelbe Felder ausfüllen. Status je Punkt: erfüllt / offen / n. z. Bei „offen“ Maßnahme und Termin eintragen. Die Auswertung rechnet selbst.'),
 ('Verantwortlich','Bereich, der den Punkt prüft und bestätigt. Festgelegt: Werkzeugabnahme gemeinsam Prozesstechnik und Werkzeugbau; Maschinenzeit (Rüst- und Zykluszeit) gemeinsam Prozesstechnik und Produktionsplanung. Die übrigen Zuordnungen folgen den Rollen der 7V-5-1 (Entwurf) und sind noch mit den Bereichen abzustimmen.'),
 ('Ablage','Ausgefüllte Checkliste als Anlage zum Prozessreview-Workflow (7F-34-1) in DocuWare ablegen.'),
 ('Bezug zu Vorgaben','7V-3-1 Vers. N: 7.3.4.8 Entwicklungsausgaben, 7.3.4.10 Serienfreigabe. 7V-5-1 (Entwurf, Stand 23.10.2026): Produktionsleiter Themenblock 11 – Kontrolle des Bemusterungsprozesses aus Produktionssicht, Run@Rate, Vorproduktion; Rollen 7.5.3.12–7.5.3.19. 6V-1-1 / 6F-22-6: Schulung und Unterweisung.'),
 ('Bezug zu den Normen','IATF 16949: 8.3.4.4 Produktfreigabe, 8.3.5.2 Ergebnisse der Fertigungsprozessentwicklung, 8.5.1.1 Produktionslenkungsplan, 8.5.1.5 TPM, 8.5.1.6 Produktionswerkzeuge, 7.2.2 Schulung am Arbeitsplatz. ISO 14001: 8.1 Betriebliche Planung und Steuerung. ASchG § 14: Unterweisung.'),
 ('Stand','12.11.2026, Produktionsleitung. Interne Arbeitshilfe, kein gelenktes Formblatt.'),
 ('Begriff: Run@Rate','Produktionslauf unter Serienbedingungen (Serienwerkzeug, Serienmaschine, Serienpersonal, Serienmaterial, Serientakt) über eine festgelegte Dauer bzw. Stückzahl. Er weist nach, dass Zykluszeit, Ausbringung und Ausschussquote erreicht werden. Dauer und Stückzahl laut Kundenvorgabe, sonst intern festlegen. Begriff wie in 7V-5-1 (Entwurf), Produktionsleiter Themenblock 11; in der 7V-3-1 Vers. N nicht beschrieben.'),
 ('Begriff: vorläufige Prozessfähigkeit','Fähigkeitskennwert (Ppk) aus dem Bemusterungs- bzw. Run@Rate-Lauf für besondere Merkmale; Zielwert laut Kundenvorgabe, üblich Ppk ≥ 1,67.'),
 ('Begriff: Produktionsfreigabemuster / Rückstellmuster','Referenzteile am Arbeitsplatz: das Produktionsfreigabemuster aus dem Serienstart bzw. das Rückstellmuster der letzten Produktion. Einen eigenen Prüfplan gibt es in der Produktion nicht; die Prüfungen stehen in der artikelbezogenen Arbeitsanweisung.'),
 ('Abkürzungen','PT = Produkt-/Projekttechnik (nicht Prozesstechnik). RPP = Robust Production Processes, Team im Qualitätsmanagement. QS = Qualitätssicherung Produktion. PQB = Qualitätsprüfer/in. FOSS = ERP-System, ARPL = FOSS-Modul Arbeitsplanpflege, MES = Authentig. KPLI = wöchentliche Kapazitäts- und Planungsabstimmung Produktion/Logistik.')]
h['A1']='Hinweise zur Checkliste'; h['A1'].font=font(size=14,bold=True,color='00435C')
r=3
for a,b in zeilen_h:
    h.cell(r,1,a).font=font(bold=True); h.cell(r,1).alignment=WRAP
    h.cell(r,2,b).font=font(); h.cell(r,2).alignment=WRAP
    h.row_dimensions[r].height=15*max(1,-(-len(b)//95)); r+=1
r+=1
h.cell(r,1,'Beispiel einer ausgefüllten Zeile').font=font(bold=True,color='00435C'); r+=1
for c,t in enumerate(['Nr / Kriterium','Nachweis · Verantwortlich · Status · Bemerkung · Termin'],1):
    x=h.cell(r,c,t); x.font=font(bold=True); x.fill=KOPF; x.border=RAND
r+=1
h.cell(r,1,'10  Prozessparameter sind freigegeben und in der Maschine gespeichert').font=font(); h.cell(r,1).alignment=WRAP
h.cell(r,2,'Einstelldatenblatt · Prozesstechnik · offen · Nachdruck noch nicht optimiert, Freigabe nach 2. Optimierungsschleife · 20.11.2026').font=font()
h.cell(r,2).alignment=WRAP
for c in (1,2): h.cell(r,c).border=RAND
h.row_dimensions[r].height=42
h.cell(r+1,1,'Beispielwerte sind frei gewählt.').font=font(size=8,italic=True,color='666666')
h.page_setup.orientation='landscape'; h.page_setup.paperSize=h.PAPERSIZE_A4; h.page_setup.fitToWidth=1; h.page_setup.fitToHeight=1; h.sheet_properties.pageSetUpPr.fitToPage=True
wb.save(OUT); print('ok', OUT, 'Punkte', nr, 'Zeilen', erste, letzte)
