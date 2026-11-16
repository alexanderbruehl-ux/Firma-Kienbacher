"""Freigabefassung erzeugen: alle Änderungen übernehmen, Kommentare und gelbe
Markierungen entfernen, Version und Datum in der Fußzeile setzen,
Gesamtseitenzahl als Feld NUMPAGES. Aufruf:
python3 freigabefassung.py ENTPACKT_DIR VERSION_ALT VERSION_NEU DATUM_ALT DATUM_NEU [--titel "..."]"""
import re, sys, os, glob, datetime
D, VA, VN, DA, DN = sys.argv[1:6]
TITEL = sys.argv[sys.argv.index('--titel')+1] if '--titel' in sys.argv else None
def lies(p): return open(p, encoding='utf-8').read()
def schreib(p, t): open(p, 'w', encoding='utf-8').write(t)

p = f'{D}/word/document.xml'; x = lies(p)
n_del = len(re.findall(r'<w:del\b[^>]*(?<!/)>', x))
x = re.sub(r'<w:del\b[^>]*(?<!/)>.*?</w:del>', '', x, flags=re.S)
n_ins = len(re.findall(r'<w:ins\b[^>]*(?<!/)>', x))
x = re.sub(r'<w:ins\b[^>]*(?<!/)>', '', x).replace('</w:ins>', '')
x = re.sub(r'<w:(?:ins|del)\b[^>]*/>', '', x)
x = re.sub(r'<w:(rPrChange|pPrChange|tblPrChange|trPrChange|tcPrChange|sectPrChange)\b.*?</w:\1>', '', x, flags=re.S)
n_kom = x.count('<w:commentReference')
x = re.sub(r'<w:commentRange(?:Start|End)\b[^>]*/>', '', x)
x = re.sub(r'<w:r\b(?:(?!</w:r>).)*?<w:commentReference\b[^>]*/>(?:(?!</w:r>).)*?</w:r>', '', x, flags=re.S)
n_hl = x.count('<w:highlight')
x = re.sub(r'<w:highlight\b[^>]*/>', '', x)
x = x.replace('<w:rPr></w:rPr>', '')
assert '<w:ins' not in x and '<w:del ' not in x and 'commentReference' not in x
schreib(p, x)
print(f'Änderungen übernommen: {n_ins} Einfügungen, {n_del} Löschungen; Kommentare entfernt: {n_kom}; Markierungen entfernt: {n_hl}')

# Kommentar-Teile entfernen
rp = f'{D}/word/_rels/document.xml.rels'; r = lies(rp)
r = re.sub(r'<Relationship [^>]*Target="comments[^"]*"[^>]*/>', '', r); schreib(rp, r)
ct = f'{D}/[Content_Types].xml'; c = lies(ct)
c = re.sub(r'<Override PartName="/word/comments[^"]*"[^>]*/>', '', c); schreib(ct, c)
for f in glob.glob(f'{D}/word/comments*.xml'): os.remove(f)

# Fußzeile: Version, Datum, Gesamtseitenzahl als Feld
for fp in glob.glob(f'{D}/word/footer*.xml'):
    y = lies(fp)
    if f'>{VA}<' not in y: continue
    y = y.replace(f'<w:t>{VA}</w:t>', f'<w:t>{VN}</w:t>', 1)
    assert DA in y; y = y.replace(f'>{DA}<', f'>{DN}<', 1)
    m = re.search(r'(<w:r>(<w:rPr>(?:(?!</w:rPr>).)*</w:rPr>)<w:t xml:space="preserve"> von )(\d+)(</w:t></w:r>)', y, flags=re.S)
    if m:  # feste Gesamtseitenzahl -> Feld NUMPAGES
        rpr = m.group(2)
        feld = (f'<w:r>{rpr}<w:t xml:space="preserve"> von </w:t></w:r>'
                f'<w:r>{rpr}<w:fldChar w:fldCharType="begin"/></w:r>'
                f'<w:r>{rpr}<w:instrText xml:space="preserve"> NUMPAGES </w:instrText></w:r>'
                f'<w:r>{rpr}<w:fldChar w:fldCharType="separate"/></w:r>'
                f'<w:r>{rpr}<w:t>{m.group(3)}</w:t></w:r>'
                f'<w:r>{rpr}<w:fldChar w:fldCharType="end"/></w:r>')
        y = y[:m.start()] + feld + y[m.end():]
        print('Fußzeile: feste Gesamtseitenzahl durch Feld NUMPAGES ersetzt')
    schreib(fp, y); print('Fußzeile', os.path.basename(fp), f': Version {VA}->{VN}, Datum {DA}->{DN}')

# Dokumenteigenschaften
cp = f'{D}/docProps/core.xml'; k = lies(cp)
jetzt = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
k = re.sub(r'<cp:lastModifiedBy>[^<]*</cp:lastModifiedBy>', '<cp:lastModifiedBy>Alexander Brühl</cp:lastModifiedBy>', k)
k = re.sub(r'(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)', rf'\g<1>{jetzt}\g<2>', k)
if TITEL: k = re.sub(r'<dc:title>[^<]*</dc:title>', f'<dc:title>{TITEL}</dc:title>', k)
schreib(cp, k)
