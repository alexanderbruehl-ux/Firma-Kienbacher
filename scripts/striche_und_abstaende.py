"""Seitliche Striche (gezeichnete Linien) entfernen; optional leere Absätze aufräumen.
python3 striche_und_abstaende.py ENTPACKT_DIR [--abstaende]"""
import sys
from lxml import etree
D = sys.argv[1]; ABST = '--abstaende' in sys.argv
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
      'mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006',
      'v': 'urn:schemas-microsoft-com:vml',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
W = '{%s}' % NS['w']
p = f'{D}/word/document.xml'
baum = etree.parse(p); wurzel = baum.getroot()

def ist_linie(el):
    if el.xpath('.//a:prstGeom[@prst="straightConnector1"]', namespaces=NS): return True
    if el.xpath('.//v:shape[contains(@type,"_x0000_t32")]', namespaces=NS): return True
    return False
def hat_bild(el):
    return bool(el.xpath('.//v:imagedata|.//a:blip', namespaces=NS))

n = 0
for el in wurzel.xpath('//mc:AlternateContent', namespaces=NS):
    if el.getparent() is not None and ist_linie(el) and not hat_bild(el):
        el.getparent().remove(el); n += 1
for el in wurzel.xpath('//w:pict|//w:drawing', namespaces=NS):
    if el.getparent() is not None and ist_linie(el) and not hat_bild(el):
        el.getparent().remove(el); n += 1
print('Striche entfernt:', n)

if ABST:
    body = wurzel.find(W + 'body')
    def text(pp): return ''.join(pp.itertext()).strip()
    def speziell(pp):
        return bool(pp.xpath('.//w:drawing|.//w:pict|.//mc:AlternateContent|.//w:object|.//w:br[@w:type="page"]|.//w:sectPr', namespaces=NS))
    def leer(pp): return pp.tag == W + 'p' and not text(pp) and not speziell(pp)
    kinder = list(body)
    gruppen = []; i = 0
    while i < len(kinder):
        if leer(kinder[i]):
            j = i
            while j < len(kinder) and leer(kinder[j]): j += 1
            gruppen.append((i, j)); i = j
        else: i += 1
    weg = 0
    for i, j in gruppen:
        danach = kinder[j] if j < len(kinder) else None
        seitenumbruch = danach is not None and bool(danach.xpath('.//w:br[@w:type="page"]', namespaces=NS))
        ende = danach is None or danach.tag == W + 'sectPr'
        if seitenumbruch or ende: behalten = 0          # vor Seitenumbruch / am Dokumentende: alle weg
        elif i == 0: behalten = 1                       # Anfang: ein Leerabsatz vor dem Titel
        else: behalten = 1                              # sonst höchstens ein Leerabsatz
        for k in range(i + behalten, j):
            body.remove(kinder[k]); weg += 1
    print('leere Absätze entfernt:', weg, '| verbleibend leer:', sum(1 for k in body if leer(k)))
baum.write(p, xml_declaration=True, encoding='UTF-8', standalone=True)
