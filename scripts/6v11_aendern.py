import re, sys
from xml.sax.saxutils import escape
P = sys.argv[1]
x = open(P, encoding="utf-8").read()
AUTHOR, DATE = "Alexander Brühl", "2026-11-09T15:00:00Z"
nid = [9100]
def att():
    nid[0] += 1; return f'w:id="{nid[0]}" w:author="{AUTHOR}" w:date="{DATE}"'
def r(t, rpr): return f'<w:r>{rpr}<w:t xml:space="preserve">{escape(t)}</w:t></w:r>'
def ins(t, rpr): return f'<w:ins {att()}>{r(t, rpr)}</w:ins>'
def dele(t, rpr): return f'<w:del {att()}><w:r>{rpr}<w:delText xml:space="preserve">{escape(t)}</w:delText></w:r></w:del>'
def ppr_ins(ppr):
    if '<w:rPr/>' in ppr: return ppr.replace('<w:rPr/>', f'<w:rPr><w:ins {att()}/></w:rPr>', 1)
    if '<w:rPr>' in ppr: return ppr.replace('<w:rPr>', f'<w:rPr><w:ins {att()}/>', 1)
    return ppr.replace('</w:pPr>', f'<w:rPr><w:ins {att()}/></w:rPr></w:pPr>')
def neu(ppr, teile):
    """teile = [(text, rpr), ...]; leere Liste = leerer eingefügter Absatz"""
    return f'<w:p>{ppr_ins(ppr)}' + "".join(ins(t, rp) for t, rp in teile) + '</w:p>'

paras = list(re.finditer(r'<w:p[ >].*?</w:p>', x, flags=re.S))
def P_(i): return paras[i].group(0)
def ppr(i): return re.search(r'<w:pPr>.*?</w:pPr>', P_(i), flags=re.S).group(0)
def text(i): return "".join(re.findall(r'<w:t(?: [^>]*)?>([^<]*)</w:t>', P_(i)))
def finde(anfang):
    t = [i for i in range(len(paras)) if text(i).startswith(anfang)]; assert len(t) == 1, (anfang, t); return t[0]

iG = finde("Sie gilt ausdrücklich auch für Schulungen")
iC = finde("Cyber-Security-Schulungen werden dabei als regelmäßige")
iB = finde("b) gesetzlich geforderten Unterweisungen (Brandschutz und Arbeitsplatzunterweisung)")
iN = finde("Handelte es sich um neu entstandene Aufgaben")

N  = '<w:rPr><w:bCs/></w:rPr>'          # normaler Text in 6.2.5
NB = '<w:rPr><w:b/><w:bCs/></w:rPr>'    # fett in 6.2.5
G  = '<w:rPr><w:szCs w:val="22"/></w:rPr>'
aend = {}

# 1) Geltungsbereich
aend[iG] = P_(iG) + neu(ppr(iG), []) + neu(ppr(iG), [("Sie gilt auch für überlassene Arbeitskräfte (Leiharbeit), PraktikantInnen und befristet Beschäftigte. Für betriebsfremde Personen gilt Abschnitt C.", G)])

# 2) 6.2.4 b) Pflichtunterweisungen
aend[iC] = P_(iC) + neu(ppr(iC), [("Unterweisungen nach ASchG § 14, insbesondere über gefährliche Arbeitsstoffe anhand der gültigen Betriebsanweisungen und über die Benutzung der arbeitsplatzbezogenen PSA, sind regelmäßige Pflichtunterweisungen und werden mindestens einmal jährlich durchgeführt. Welche Betriebsanweisungen für welchen Arbeitsbereich gelten, ergibt sich aus dem Gefahrstoffkataster. Die Unterweisungen werden in BMD PI mit einem Fälligkeitsdatum erfasst, das ihre Gültigkeit auf 12 Monate begrenzt; mit jeder jährlichen Unterweisung wird das Fälligkeitsdatum neu gesetzt. Die LTG HRM überwacht die Fälligkeiten und informiert die AL rechtzeitig vor Ablauf. Die Durchführung obliegt dem jeweiligen AL bzw. einer von ihm befugten, fachkundigen Person; die Sicherheitsfachkraft unterstützt bei Bedarf. Bei PSA gegen tödliche Gefahren oder bleibende Gesundheitsschäden (Atemschutz, Absturzsicherung) umfasst die Unterweisung eine praktische Übung (Anlegen, Sitz- und Dichtheitsprüfung).", ''),])

# 3) 6.2.5 A b) – Klammer erweitern (nur im zweiten Run)
p = P_(iB)
alt_run = re.findall(r'<w:r[ >].*?</w:r>', p, flags=re.S)[1]
assert "(Brandschutz und Arbeitsplatzunterweisung)" in alt_run
neu_run = (r(" gesetzlich geforderten Unterweisungen (Brandschutz", N) + dele(" und", N) + ins(",", N)
           + r(" Arbeitsplatzunterweisung", N)
           + ins(", Unterweisung über die am Arbeitsplatz verwendeten gefährlichen Arbeitsstoffe anhand der gültigen Betriebsanweisungen sowie über die Benutzung der arbeitsplatzbezogenen PSA – jeweils vor Aufnahme der Tätigkeit", N)
           + r(") als auch ", N))
aend[iB] = p.replace(alt_run, neu_run, 1)

# 4) 6.2.5 A – Nachunterweisung und Nachweis
pN = ppr(iN)
aend[iN] = P_(iN) + neu(pN, []) + neu(pN, [
    ("Anlassbezogene Nachunterweisung:", NB),
    (" Bei Versetzung oder Änderung des Aufgabenbereichs, bei Einführung neuer oder geänderter Arbeitsstoffe, Arbeitsmittel, Arbeitsverfahren oder PSA sowie nach Unfällen oder Beinaheunfällen werden die betroffenen MitarbeiterInnen erneut unterwiesen. Betriebsanweisungen werden von der Produktionsleitung freigegeben; bei einer neuen oder geänderten Betriebsanweisung informiert die Produktionsleitung die betroffenen AL und die LTG HRM. Bei neuen Arbeitsstoffen sowie bei Änderungen mit neuen Gefahren oder Schutzmaßnahmen erfolgt die Unterweisung vor der nächsten Verwendung; rein redaktionelle Änderungen werden bei der nächsten jährlichen Unterweisung behandelt.", N)]) \
  + neu(pN, []) + neu(pN, [
    ("Nachweis der Unterweisungen:", NB),
    (" Unterweisungen werden mit Datum, Inhalt (Nummer und Fassung der Betriebsanweisung bzw. PSA), unterweisender Person und Unterschrift der Unterwiesenen dokumentiert, als interne Schulungsdokumentation in DocuWare abgelegt und in BMD PI mit Fälligkeitsdatum erfasst. Mit der Unterschrift bestätigen die MitarbeiterInnen, dass sie die Unterweisung verstanden haben. MitarbeiterInnen, die der deutschen Sprache nicht ausreichend mächtig sind, werden in einer für sie verständlichen Sprache bzw. bildgestützt unterwiesen.", N)])

for i in sorted(aend, reverse=True):
    s, e = paras[i].span(); x = x[:s] + aend[i] + x[e:]
open(P, "w", encoding="utf-8").write(x)
print("geändert:", sorted(aend), "| Revisions-IDs bis", nid[0])
