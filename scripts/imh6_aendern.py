import re, sys
from xml.sax.saxutils import escape
P = sys.argv[1]
x = open(P, encoding="utf-8").read()
AUTHOR, DATE = "Alexander Brühl", "2026-11-09T12:00:00Z"
nid = [9000]
def att():
    nid[0] += 1
    return f'w:id="{nid[0]}" w:author="{AUTHOR}" w:date="{DATE}"'
def r(t, rpr): return f'<w:r>{rpr}<w:t xml:space="preserve">{escape(t)}</w:t></w:r>'
def ins(t, rpr): return f'<w:ins {att()}>{r(t, rpr)}</w:ins>'
def dele(t, rpr): return f'<w:del {att()}><w:r>{rpr}<w:delText xml:space="preserve">{escape(t)}</w:delText></w:r></w:del>'
def ppr_ins(ppr):
    # Absatzmarke als eingefügt markieren (w:ins als erstes Kind von w:rPr in w:pPr)
    if '<w:rPr>' in ppr:
        return ppr.replace('<w:rPr>', f'<w:rPr><w:ins {att()}/>', 1)
    return ppr.replace('</w:pPr>', f'<w:rPr><w:ins {att()}/></w:rPr></w:pPr>')
def neu(ppr, text, rpr): return f'<w:p>{ppr_ins(ppr)}{ins(text, rpr)}</w:p>'

paras = list(re.finditer(r'<w:p[ >].*?</w:p>', x, flags=re.S))
def P_(i): return paras[i].group(0)
def ppr(i): return re.search(r'<w:pPr>.*?</w:pPr>', P_(i), flags=re.S).group(0)
def rpr(i):
    run = re.search(r'<w:r[ >].*?</w:r>', P_(i), flags=re.S).group(0)
    m = re.search(r'<w:rPr>.*?</w:rPr>', run, flags=re.S); return m.group(0) if m else ''
def text(i): return "".join(re.findall(r'<w:t(?: [^>]*)?>([^<]*)</w:t>', P_(i)))
def ersetze(i, schritte, anhang=None):
    """Einlauf-Absatz: schritte = [(alt, neu), ...] in Textreihenfolge; anhang = Text am Ende einfügen."""
    p = P_(i); rp = rpr(i); t = text(i)
    assert len(re.findall(r'<w:r[ >]', p)) == 1, (i, "mehrere Runs")
    out, pos = "", 0
    for alt, neu_t in schritte:
        k = t.index(alt, pos)
        if k > pos: out += r(t[pos:k], rp)
        out += dele(alt, rp) + (ins(neu_t, rp) if neu_t else "")
        pos = k + len(alt)
    if pos < len(t): out += r(t[pos:], rp)
    if anhang: out += ins(anhang, rp)
    return re.sub(r'<w:r[ >].*?</w:r>', lambda m: out, p, count=1, flags=re.S)

# Plausibilitätsprüfungen der Ankerabsätze
assert text(14).startswith("Mitarbeitermotivation") and 'w:numId w:val="13"' in P_(14)
assert "Engage" in text(61) and "Engage" in text(70)
assert text(90) == "Durchführung von gesetzlich vorgeschriebenen Unterweisungen"
assert text(93).startswith("Mitarbeitermotivation") and text(96).startswith("Des Weiteren")
assert text(171).startswith("Brandgefährliche")

aend = {}
# 1) Inhaltsverzeichnis: neuer Eintrag 6.2.6 nach 6.2.5
aend[14] = P_(14) + neu(ppr(14), "Unterweisungen nach ASchG (gefährliche Arbeitsstoffe und PSA)", rpr(14))
# 2) 6.2.1 Engage
aend[61] = ersetze(61, [("Diese Mitarbeiter werden ebenfalls im Engage erfasst.",
                         "Die Schulungen dieser Mitarbeiter werden ebenfalls als interne Schulungsdokumentation in DocuWare dokumentiert.")])
# 3) 6.2.2 Engage
aend[70] = ersetze(70, [("(auch im Schulungssystem Engage)", "(Dokumentation als interne Schulungsdokumentation in DocuWare)")])
# 4) 6.2.4 Aufzählungspunkt
aend[90] = ersetze(90, [("von", "der")], anhang=" (siehe 6.2.6)")
# 5) neuer Abschnitt 6.2.6 nach dem Ende von 6.2.5
koerper_ppr, koerper_rpr = ppr(61), rpr(61)
liste_ppr, liste_rpr = ppr(90), rpr(90)
abschnitt = [
  neu(ppr(93), "Unterweisungen nach ArbeitnehmerInnenschutzgesetz (gefährliche Arbeitsstoffe und PSA)", rpr(93)),
  neu(koerper_ppr, "Alle MitarbeiterInnen, einschließlich überlassener Arbeitskräfte und PraktikantInnen, werden nachweislich über Sicherheit und Gesundheitsschutz, über den Umgang mit den an ihrem Arbeitsplatz verwendeten gefährlichen Arbeitsstoffen sowie über die richtige Benutzung, Pflege und Grenzen der zur Verfügung gestellten persönlichen Schutzausrüstung (PSA) unterwiesen (ASchG §§ 14, 69, 70). Die Unterweisung erfolgt", koerper_rpr),
  neu(liste_ppr, "vor Aufnahme der Tätigkeit (Bestandteil des Einschulungsplans),", liste_rpr),
  neu(liste_ppr, "bei Versetzung oder Änderung des Aufgabenbereichs, bei Einführung neuer oder geänderter Arbeitsstoffe, Arbeitsmittel, Arbeitsverfahren oder PSA sowie nach Unfällen und Beinaheunfällen,", liste_rpr),
  neu(liste_ppr, "wiederkehrend mindestens einmal jährlich.", liste_rpr),
  neu(koerper_ppr, "Grundlage sind die gültigen Betriebsanweisungen, die an den Verwendungsstellen ausgehängt sind, die Sicherheitsdatenblätter im Gefahrstoffkataster (DocuWare), die in der Arbeitsplatzevaluierung festgelegte PSA und der Hautschutzplan. Die Unterweisung umfasst auch das Verhalten bei Leckagen und Umweltnotfällen sowie die sachgerechte Entsorgung.", koerper_rpr),
  neu(koerper_ppr, "Für die Durchführung sind die Abteilungsleiter verantwortlich, für Planung (Fälligkeiten in BMD PI) und Dokumentation (interne Schulungsdokumentation in DocuWare) die LTG HRM. Ablauf, Fristen und Nachweis regelt die Verfahrensanweisung 6V-1-1.", koerper_rpr),
]
aend[96] = P_(96) + "".join(abschnitt)
# 6) PSA in 6.4.1 nach dem letzten Absatz
psa_ppr, psa_rpr = ppr(171), rpr(171)
psa_rpr_fett = psa_rpr.replace('<w:rPr>', '<w:rPr><w:b/>', 1)
psa = [
  neu(psa_ppr, "Persönliche Schutzausrüstung (PSA)", psa_rpr_fett),
  neu(psa_ppr, "Gefahren werden vorrangig durch Ersatz gefährlicher Arbeitsstoffe sowie durch technische und organisatorische Maßnahmen vermieden; PSA wird eingesetzt, wo diese Maßnahmen nicht ausreichen (ASchG §§ 7, 43).", psa_rpr),
  neu(psa_ppr, "Die erforderliche PSA legen die AL gemeinsam mit der Sicherheitsfachkraft auf Basis der Arbeitsplatzevaluierung sowie der Sicherheitsdatenblätter und Betriebsanweisungen fest, z. B. Handschuhmaterial und -stärke, Augen- und Atemschutz sowie Absturzsicherung. Ob für die verwendeten Atemschutzgeräte eine Eignungsuntersuchung erforderlich ist, beurteilt die Arbeitsmedizin. Hautschutz erfolgt nach dem Hautschutzplan.", psa_rpr),
  neu(psa_ppr, "PSA wird den MitarbeiterInnen kostenlos und in passender Größe zur Verfügung gestellt – durch HR direkt oder durch Befüllen der persönlichen PSA-Spinde. Beschafft wird nur PSA mit CE-Kennzeichnung (VO (EU) 2016/425). Die Ausgabe wird in der Ausgabeliste HR bzw. in der Befüllliste der PSA-Spinde dokumentiert (DocuWare).", psa_rpr),
  neu(psa_ppr, "Die MitarbeiterInnen sind zur bestimmungsgemäßen Benutzung verpflichtet (ASchG § 15); die AL bzw. Teamleitungen überwachen die Benutzung.", psa_rpr),
  neu(psa_ppr, "Beschädigte oder verbrauchte PSA wird umgehend ersetzt, PSA mit Ablaufdatum (z. B. Atemschutzfilter) rechtzeitig getauscht. PSA gegen Absturz wird gemäß Herstellerangaben, mindestens jährlich, durch eine fachkundige Person geprüft; die Prüfung wird dokumentiert. Kontaminierte PSA wird gemäß Betriebsanweisung entsorgt.", psa_rpr),
]
aend[171] = P_(171) + "".join(psa)

for i in sorted(aend, reverse=True):
    s, e = paras[i].span(); x = x[:s] + aend[i] + x[e:]
open(P, "w", encoding="utf-8").write(x)
print("geändert:", sorted(aend), "| Revisions-IDs bis", nid[0])
