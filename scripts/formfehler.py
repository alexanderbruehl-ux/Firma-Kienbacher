"""Formfehler in IMH 6 (Vers. O) und 6V-1-1 (Vers. G) beheben – direkt in den <w:t>-Texten."""
import re, sys
F = sys.argv[1]  # Basisordner mit oimh/ und o6v/
def lies(p): return open(p, encoding='utf-8').read()
def schreib(p, t): open(p, 'w', encoding='utf-8').write(t)
def ersetze_t(x, alt, neu, anzahl=1):
    a = f'>{alt}</w:t>'; n = x.count(a)
    assert n == anzahl, (alt, n); return x.replace(a, f'>{neu}</w:t>')

# ---- IMH 6
p = f'{F}/oimh/word/document.xml'; x = lies(p)
toc_ende = x.find('Mitgeltende Dokumente und Formulare')
toc, rest = x[:toc_ende + 60], x[toc_ende + 60:]
toc = ersetze_t(toc, 'Unterweisungen nach ASchG (gefährliche Arbeitsstoffe und PSA)', 'Unterweisungen nach ArbeitnehmerInnenschutzgesetz (gefährliche Arbeitsstoffe und PSA)')
toc = ersetze_t(toc, '6.3.1 Werks – Anlagen – Einrichtungsplanung', '6.3.1 Werks-, Anlagen und Einrichtungsplanung')
toc = ersetze_t(toc, 'Sauberkeit der Arbeitsstätten', 'Sauberkeit der Betriebsstätten')
toc = ersetze_t(toc, 'Umgang mit Risiken und Chancen', 'Maßnahmen zum Umgang mit Risiken und Chancen')
toc = ersetze_t(toc, '6.6', '6.8')
toc = ersetze_t(toc, 'Mitgeltende Dokumente und Formulare', 'Mitgeltende Dokumente')
# fehlenden Eintrag 6.3.5 nach 6.3.4 Brandschutz einfügen (Absatz klonen)
m = re.search(r'<w:p\b(?:(?!<w:p\b).)*?>6\.3\.4 Brandschutz</w:t>.*?</w:p>', toc, flags=re.S)
klon = re.sub(r' w14:paraId="[^"]*"', '', m.group(0)).replace('>6.3.4 Brandschutz</w:t>', '>6.3.5 Erstellen von Layout-Plänen</w:t>')
toc = toc[:m.end()] + klon + toc[m.end():]
x = toc + rest
# Textteil
n = len(re.findall(r'>4\.6 Erstellen von Layout Plänen ?</w:t>', x)); assert n == 1, n
x = re.sub(r'>4\.6 Erstellen von Layout Plänen ?</w:t>', '>6.3.5 Erstellen von Layout-Plänen</w:t>', x)
assert x.count('Rechtliche Verpflichtung und andere Anforderungen') == 1
x = x.replace('Rechtliche Verpflichtung und andere Anforderungen', 'Rechtliche Verpflichtungen und andere Anforderungen')
k = x.count('Docuware'); x = x.replace('Docuware', 'DocuWare')
schreib(p, x); print(f'IMH 6: Inhaltsverzeichnis angeglichen, 6.3.5 ergänzt, „4.6“ -> 6.3.5, Überschrift 6.7, {k}x DocuWare')

# ---- 6V-1-1
p = f'{F}/o6v/word/document.xml'; x = lies(p)
for alt, neu in [('B.) Bewertung', 'B) Bewertung'), ('C.) Verhaltensregeln', 'C) Verhaltensregeln')]:
    assert x.count(alt) == 1, alt; x = x.replace(alt, neu)
k = x.count('Docuware'); x = x.replace('Docuware', 'DocuWare')
schreib(p, x)
h = f'{F}/o6v/word/header1.xml'; y = lies(h)
assert y.count('Zu Kap. 06 Management von Ressourcen') == 1
schreib(h, y.replace('Zu Kap. 06 Management von Ressourcen', 'Zu Kap. 06 Management der Ressourcen'))
print(f'6V-1-1: „B.)/C.)“ -> „B)/C)“, {k}x DocuWare, Kopfzeile „Management der Ressourcen“')

# Nachtrag: Überschrift 6.2.6 kurz (ASchG) in Inhaltsverzeichnis und Text, Tippfehler „6.3.3.“ im Inhaltsverzeichnis

# Nachtrag 17.11.2026: 6V-1-1 Überschrift 6.2.4 c) „Bewusstseinsergänzung“ -> „Bewusstseinsbildung“ (per sed im entpackten Dokument)
