# Projektstatus – Revision 7V-5-1 (Stand: siehe Datum letzter Commit)

## Kontext

Alexander ist Produktionsleiter bei einem automotive-zertifizierten
(IATF 16949) Kunststoff-Spritzguss-Unternehmen (Kienbacher). Er überarbeitet
gemeinsam mit Claude die QM-Verfahrensanweisung „Auftragsabwicklung in der
Produktion" (Dok. 7V-5-1, Version k → l), um sie an den aktuellen
Organisationszustand anzupassen und die IATF-16949-Konformität sicherzustellen.

## Methodik / Vorgehen

- **Organisierendes Prinzip: AKV** (Aufgaben / Kompetenzen / Verantwortung)
  - **Verantwortung** = wofür wird die Person am Ergebnis gemessen (Rechenschaft)
  - **Aufgaben** = was ist regelmäßig zu tun (Tätigkeiten)
  - **Kompetenzen/Befugnisse** = was darf eigenständig entschieden/angeordnet werden
  - Ein Punkt kann in mehreren Spalten stehen (z. B. wenn dieselbe Person entscheidet
    UND operativ mitwirkt – siehe Beispiel „ungeplante Kapazitätsmaßnahmen").
- **Zusätzliche Themenfelder** (nicht als eigene Matrix-Spalte, sondern als inhaltliche
  Ergänzung *innerhalb* der drei AKV-Spalten – **Option B**, siehe Entscheidung):
  - **Führung**: klassische Personalführung (Zielvereinbarung, Feedback, Entwicklung,
    Konfliktmanagement, Vorbildfunktion) – gilt für alle Führungsrollen
  - **Außensicht**: nur bei der Rolle **Produktionsleiter** – Repräsentation,
    Schnittstelle nach außen/oben. Bei nachgelagerten Rollen (z. B. Schichtführer) NICHT relevant.
  - **Sicherheit**: Arbeitssicherheit, gesetzliche Pflichten (z. B. ASchG)
  - **Umwelt**: Umweltbewusstsein, Ressourcenschonung
- **Vorgehensweise in der Diskussion**: sehr langsam, Punkt für Punkt aus der
  bestehenden Liste (Version k), nichts überspringen, Rückfragen stellen statt
  raten, unternehmensspezifische Begriffe klären bevor sie ins Dokument kommen.
- Alexander ergänzt nach dem gemeinsamen Grobentwurf noch weitere
  unternehmensspezifische Details selbst.
- **Grundsatz: Keine namentliche Nennung von Stelleninhabern.** Ein
  QM-Dokument beschreibt Rollen/Funktionen, nicht Personen – auch wenn
  eine Position aktuell eindeutig einer bestimmten Person zugeordnet
  ist (z. B. zur Klärung im Organigramm), wird das im Dokument nicht
  namentlich festgehalten.
- **Grundsatz: Keine variablen, organisatorischen Detailangaben im
  Dokument** (z. B. Anzahl Mitarbeiter/Teamgröße, prozentuale
  Aufteilung von Ressourcen auf Rollen, konkrete Kennzahlen-Zielwerte
  wie OEE/MTBF/MTTR-Sollwerte). Solche Angaben ändern sich erfahrungs-
  gemäß häufig und würden bei jeder Änderung eine Dokumentrevision
  erfordern. Das Dokument ist als Prozess-/Verfahrensanweisung zu
  schreiben (Abläufe, Rollen, AKV, Prozesse, Input-/Output-Faktoren),
  orientiert an IATF 16949/ISO 9001 und
  Prozessmanagement-Grundmodellen (Turtle-Diagramm, Ishikawa/
  Fischgrät). Die **Kompetenz**, bestimmte Kennzahlen/Zielwerte
  festzulegen, bleibt im Dokument (AKV-Aussage); die **konkreten
  Zahlenwerte selbst** nicht.
- **Grundsatz: Jede Rolle muss für sich allein lesbar und vollständig
  sein.** Verweise der Art „siehe Rolle X" sind nur zwischen Rollen
  zulässig, die strukturell eine gemeinsame Basis teilen (z. B. die
  Teamleitungen untereinander über `FUEHRUNG_HAUPTPROZESS.md`/
  `FUEHRUNG_UNTERSTUETZUNGSPROZESSE.md`). Für alle anderen Rollen
  (z. B. PQB ist keine Teamleitungsfunktion) muss der eigene AKV-Anteil
  eines gemeinsamen Prozesses (z. B. Sperrentscheidung) **vollständig
  in der eigenen Rollenbeschreibung ausformuliert** werden, auch wenn
  eine andere Rolle denselben Prozess aus ihrer Sicht ebenfalls
  beschreibt.
- **Arbeitsregel SharePoint-Sync (Token-/Zeit-Effizienz):** Inhaltliche
  Arbeit läuft laufend in den `notes/*.md`-Dateien (günstig, reiner Text);
  `scripts/build.js` und das Word-Dokument in `working/*.docx` werden
  NICHT automatisch nach jeder einzelnen Ergänzung neu generiert. Ein
  Neu-Generieren von `working/*.docx` sowie ein Re-Upload zum SharePoint
  (Ordner „Claude Dateien") erfolgen nur auf explizite Anfrage von
  Alexander („ändere das DOC am SharePoint" o. ä.) — Grund: der Upload
  einer Binärdatei (.docx) erfordert eine vollständige Base64-Übertragung
  des gesamten Dateiinhalts und ist dadurch pro Vorgang token-/zeitintensiv,
  unabhängig vom Umfang der einzelnen inhaltlichen Änderung.

## Bearbeitungsstand

| Rolle (Dok. 7.5.3.x) | Status |
|---|---|
| 1 Produktionsleiter | ✅ Inhaltlich fertig abgestimmt (Themenblöcke 1–14 + Vertretung), siehe `PRODUKTIONSLEITER.md` — noch nicht in `working/*.docx` eingearbeitet |
| 2 Schichtführer → **Teamleitung Spritzguss-Produktion (Schichtführer)** (Umbenennung zur eindeutigen Klarstellung, analog zu den anderen Teamleitungsfunktionen) | ✅ Inhaltlich fertig abgestimmt (Themenblöcke 1–8), siehe `SCHICHTFUEHRER.md` — noch nicht in `working/*.docx` eingearbeitet |
| 3 Maschinenpersonal (Werker) → **Werker** (Sammelbegriff für Maschinenpersonal, Montage- und Endfertigungspersonal) | ✅ Inhaltlich fertig abgestimmt (Themenblock 1, gilt identisch für alle drei Bereiche), siehe `WERKER.md` |
| 4 Fertigung Montage → **Teamleitung Montage** | ✅ Inhaltlich fertig abgestimmt (Themenblöcke 1–4), siehe `MONTAGE.md` |
| 5 Boxenbauer | ✅ Inhaltlich fertig abgestimmt (Themenblöcke 1–2), siehe `BOXENBAUER.md` |
| 6 Produktionslogistiker | ✅ Inhaltlich fertig abgestimmt (Themenblöcke 1–3), siehe `PRODUKTIONSLOGISTIKER.md` |
| 7 Produktionsplanung → **Produktionsplanung und -steuerung** (Umbenennung) | ✅ Inhaltlich fertig abgestimmt (Themenblöcke 1–4), siehe `PRODUKTIONSPLANUNG.md` |
| 8 Arbeitsvorbereitung → **Digitale Prozessentwicklung & Lean Management** (Umbenennung + inhaltliche Neuausrichtung) | ✅ Inhaltlich fertig abgestimmt (Themenblöcke 1–6), siehe `DIGITALE_PROZESSENTWICKLUNG.md` |
| 9 Qualitätsprüfer/in (PQB) | ✅ Inhaltlich fertig abgestimmt (Themenblöcke 1–5), siehe `PQB.md` (Verhältnis zu neuer Rolle „QS" bereits geklärt, siehe OFFENE_ROLLEN.md) |
| 10 Lager (Materialvorbereitung) → **Teamleitung Lager** | ✅ Inhaltlich fertig abgestimmt (Themenblöcke 1–7), siehe `LAGER.md` |
| 11 Alle Mitarbeiter | ✅ Inhaltlich fertig abgestimmt (Themenblöcke 1–5), siehe `ALLE_MITARBEITER.md` |
| **NEU: Produktionskoordination (Organisation/Personal)** | 🔶 Wesentlicher Kern abgestimmt (Themenblöcke 1–2), siehe `PRODUKTIONSKOORDINATION.md` |
| **NEU: Prozesstechnik und Bemusterung** | ✅ Inhaltlich fertig abgestimmt (Themenblöcke 1–4), siehe `PROZESSTECHNIK_BEMUSTERUNG.md` |
| **NEU: QS (Qualitätssicherung Produktion)** | ✅ Inhaltlich fertig abgestimmt (Themenblöcke 1–5), siehe `QS.md` |
| **NEU: Endfertigung** (Bereich, geführt durch Teamleitung Endfertigung = Produktionskoordination) | ✅ Inhaltlich fertig abgestimmt (Themenblöcke 1–2), siehe `ENDFERTIGUNG.md` — Produktionskoordination als eigene Rolle noch separat auszuarbeiten |
| **NEU: Automatisierung** | ✅ Inhaltlich fertig abgestimmt (Themenblöcke 1–4), siehe `AUTOMATISIERUNG.md` |
| **NEU: Teamleitung Instandhaltung** | 🔶 Normrahmen abgestimmt (IATF 16949 §8.5.1.5), siehe `INSTANDHALTUNG.md` — betriebsspezifische Details von Alexander noch zu ergänzen |
| **NEU: Teamleitung Werkzeugbau** | 🔶 Normrahmen abgestimmt (IATF 16949 §8.5.1.6), siehe `WERKZEUGBAU.md` — betriebsspezifische Details von Alexander noch zu ergänzen |

Details zu den neuen/umbenannten Rollen: siehe `OFFENE_ROLLEN.md`.

### Gruppierung der Führungsrollen (Teamleiter)

Um Doppelungen zu vermeiden, werden die Teamleitungsfunktionen nicht einzeln
und unabhängig voneinander ausgearbeitet, sondern in zwei Gruppen mit
jeweils gemeinsamer AKV-Basis (Turtle-Diagramm-Logik: Hauptprozess = Input-
Bereitstellung/Transformation/Output-Versand; Unterstützungsprozess =
Ressourcen-Bereitstellung „Mit was"):

- **Hauptprozess** (`FUEHRUNG_HAUPTPROZESS.md`): Teamleitung Lager,
  Teamleitung Spritzguss-Produktion (Schichtführer), Teamleitung Montage,
  Teamleitung Endfertigung
- **Unterstützungsprozesse** (`FUEHRUNG_UNTERSTUETZUNGSPROZESSE.md`):
  Teamleitung Instandhaltung, Teamleitung Werkzeugbau

Reihenfolge: gemeinsame AKV-Basis Hauptprozess ✅ erarbeitet (abgeleitet aus
Schichtführer), danach Montage/Endfertigung/Lager, danach die Gruppe
Unterstützungsprozesse.

## Nächster konkreter Schritt

Rolle **Produktionsleiter** ist inhaltlich vollständig abgestimmt
(Themenblöcke 1–14 + Abschnitt „Vertretung", siehe PRODUKTIONSLEITER.md).

**Teamleitung Spritzguss-Produktion (Schichtführer)** ist inhaltlich
vollständig abgestimmt: allgemeine AKV-Punkte in `FUEHRUNG_HAUPTPROZESS.md`
(Themenblöcke A–H) verallgemeinert, `SCHICHTFUEHRER.md` enthält nur noch
die Spritzguss-spezifischen Ausprägungen (Themenblöcke 1, 6, 8) sowie die
schichtspezifische Besonderheit Schichtübergabe (Themenblock 9).

Beide Rollen noch nicht in `working/*.docx` eingearbeitet.

**Teamleitung Montage** ist inhaltlich vollständig abgestimmt (Themenblöcke
1–4, siehe `MONTAGE.md`); Themenblock C in `FUEHRUNG_HAUPTPROZESS.md`
wurde um die Rückmeldung fehlerhafter Kaufteile ergänzt.

**Teamleitung Endfertigung** ist inhaltlich vollständig abgestimmt
(Themenblöcke 1–2, siehe `ENDFERTIGUNG.md`).

**Teamleitung Lager** ist inhaltlich vollständig abgestimmt (Themenblöcke
1–7, siehe `LAGER.md`) — damit ist die Gruppe **Führungsrollen im
Hauptprozess** vollständig abgearbeitet.

Gruppe **Unterstützungsprozesse** (Teamleitung Instandhaltung, Teamleitung
Werkzeugbau) ist mit Normrahmen abgestimmt (betriebsspezifische Details
von Alexander noch zu ergänzen).

**Produktionskoordination** (Personalunion mit Teamleitung Endfertigung,
Vertretung des Produktionsleiters Bereich Organisation/Personal) ist im
wesentlichen Kern abgestimmt (siehe `PRODUKTIONSKOORDINATION.md`).

**Maschinenpersonal (Werker)** ist inhaltlich fertig abgestimmt (siehe
`WERKER.md`).

Alexander hat entschieden, zunächst die übrigen **einfacheren Rollen ohne
Vertretungsbezug** durchzugehen: Boxenbauer, Produktionslogistiker,
Produktionsplanung, Digitale Prozessentwicklung & Lean Management, PQB,
Alle Mitarbeiter, Automatisierung. Danach folgen **Prozesstechnik und
Bemusterung** sowie **QS (Qualitätssicherung Produktion)** (Teil der
Vertretungsstruktur des Produktionsleiters, siehe `OFFENE_ROLLEN.md`).

**Boxenbauer** ist inhaltlich fertig abgestimmt (siehe `BOXENBAUER.md`).

**Produktionslogistiker** ist inhaltlich fertig abgestimmt (siehe
`PRODUKTIONSLOGISTIKER.md`).

**Produktionsplanung und -steuerung** ist inhaltlich fertig abgestimmt
(siehe `PRODUKTIONSPLANUNG.md`).

**Digitale Prozessentwicklung & Lean Management** ist inhaltlich fertig
abgestimmt (siehe `DIGITALE_PROZESSENTWICKLUNG.md`).

**Qualitätsprüfer/in (PQB)** und **Alle Mitarbeiter** sind inhaltlich
fertig abgestimmt (siehe `PQB.md`, `ALLE_MITARBEITER.md`).

**Automatisierung** ist inhaltlich fertig abgestimmt (siehe
`AUTOMATISIERUNG.md`). Damit sind alle "einfacheren Rollen ohne
Vertretungsbezug" abgearbeitet.

**Prozesstechnik und Bemusterung** und **QS (Qualitätssicherung
Produktion)** sind inhaltlich fertig abgestimmt (siehe
`PROZESSTECHNIK_BEMUSTERUNG.md`, `QS.md`). Damit ist jede identifizierte
Rolle aus `OFFENE_ROLLEN.md` mindestens im Erstentwurf ausgearbeitet —
**alle Rollen des Dokuments haben jetzt einen inhaltlichen Stand.**

**Verbleibende offene Punkte:**
- `INSTANDHALTUNG.md`/`WERKZEUGBAU.md`: betriebsspezifische Details, die
  Alexander noch ergänzt (Ersatzteilhaltung, Fremdfirmen,
  Dokumentationssystem, Kundenwerkzeuge-Besonderheiten) — Teamgröße und
  konkrete Kennzahlen-/Fristen-Zahlenwerte bewusst NICHT mehr Teil
  dieser Liste, siehe neuer Methodik-Grundsatz unten
  (Verschleißteile-Management bereits entsprechend gelöst: Verweis auf
  ERP-System statt konkreter Werte)
- Werkzeugbau-Rollenstruktur final geklärt: eine Teamleitungsfunktion,
  ergänzt durch fachlich-technische Mitwirkung erfahrener Mitarbeiter
  (keine eigene Führungsfunktion); siehe `WERKZEUGBAU.md`
- `PRODUKTIONSKOORDINATION.md`: weitere wiederkehrende Themen, falls
  Alexander noch etwas auffällt
- **Gliederung ergänzt um drei neue Abschnitte** (ISO 9001/IATF-konforme
  Standardgliederung einer Verfahrensanweisung; Änderungshistorie
  bewusst weggelassen):
  - ✅ **Mitgeltende Unterlagen** — fertig, siehe
    `MITGELTENDE_UNTERLAGEN.md` (generische Formulierung nach
    Prozesskategorie: Kern-/Führungs-/Unterstützungsprozesse, keine
    konkreten Dokumentnummern)
  - ⬜ **Aufzeichnungen (Records)** — noch zu erarbeiten
  - ⬜ **Begriffe/Abkürzungen** — noch zu erarbeiten (nur tatsächlich im
    Dokument verwendete Begriffe/Abkürzungen, Auswahl aus `BEGRIFFE.md`)
- `scripts/build.js`/`working/*.docx`: noch nicht auf dem Stand aller in
  diesem Durchgang fertiggestellten Rollen (Produktionskoordination,
  Werker, Boxenbauer, Produktionslogistiker, Produktionsplanung,
  Digitale Prozessentwicklung, PQB, Alle Mitarbeiter, Automatisierung,
  Prozesstechnik und Bemusterung, QS) — Neu-Generierung und SharePoint-
  Sync nur auf explizite Anfrage (siehe Arbeitsregel oben)
- Ein zweiter Durchgang über alle Rollen (Review/Konsistenzprüfung,
  Formulierungen) steht noch aus

## Bereits geklärte, generelle Struktur-Entscheidungen

- **QMB/QS-Korrespondenzstruktur** (zweistufig):
  - Schicht-/Team-Ebene: Schichtführer/Teamleiter ↔ **QMB**
  - Gesamtheitliche Ebene: Produktionsleitung ↔ **QS (Qualitätssicherung Produktion)**
  - Ablauf bei Korrekturmaßnahmen: QS stellt Bedarf fest → Produktionsleitung
    entscheidet über konkrete Maßnahme → QS prüft Wirksamkeit und gibt frei
    (z. B. Entsperren von Teilen/Prozessen). Damit ist ein Vier-Augen-Prinzip
    zwischen Produktions- und Qualitätsseite auf beiden Ebenen etabliert.
- **Dreiteilige Vertretungsstruktur des Produktionsleiters** (siehe OFFENE_ROLLEN.md
  für Details der einzelnen Vertretungsfunktionen):
  1. Organisation/Personal → Produktionskoordination
  2. Technik → Prozesstechnik und Bemusterung
  3. Qualität → QS Produktion (bewusst AUSSERHALB der Produktionsabteilung
     angesiedelt — 4-Augen-Prinzip)

### Organisationsteam (Stabsfunktionen des Produktionsleiters)

Stabsfunktionen, die dem Produktionsleiter zuarbeiten (im Unterschied zu
den operativen Teamleitungen im Haupt-/Unterstützungsprozess), gegliedert
in zwei Ebenen:

- **Ebene A – Vertretungsfunktionen** (mit Eskalations-/
  Entscheidungsbefugnis bei Abwesenheit des Produktionsleiters; entspricht
  der dreiteiligen Vertretungsstruktur):
  - Produktionskoordination (Organisation/Personal)
  - Prozesstechnik und Bemusterung (Technik)
  - QS – Qualitätssicherung Produktion (Qualität); **Besonderheit:** Der
    Produktionsleiter hat **keine Weisungsbefugnis gegenüber QS**
    (bewusst organisatorisch außerhalb der Produktionsabteilung
    angesiedelt, 4-Augen-Prinzip; QS ist organisatorisch der
    Qualitätsabteilung zugeordnet). Umgekehrt hat QS **fachliche
    Weisungsbefugnis gegenüber dem Produktionsleiter in Q-Themen**
    (spätestens über den QMB durchsetzbar). **QMB ist eine
    Abteilungsleiter-Funktion, gleichrangig mit dem Produktionsleiter**
    (nicht nur eine Stabsstelle).
- **Ebene B – unterstützende Fachfunktionen** (keine formale
  Vertretungsbefugnis):
  - **Produktionsplanung und -steuerung** — Sonderstellung: funktional
    allen anderen vorgelagert, zeitliche Taktgeber-Funktion ("Gehirn der
    Produktion"); niemand führt etwas zeitlich unabhängig von dieser
    Instanz durch, auch relevant für Personalkapazitäten
  - Digitale Prozessentwicklung & Lean Management

**Automatisierung** gehört NICHT zum Organisationsteam, sondern
konzeptionell zur Gruppe Unterstützungsprozesse (neben Werkzeugbau,
Instandhaltung) — ähnliche Logik der Ressourcen-/Technikbereitstellung;
zusätzlich enge Vernetzung mit Prozesstechnik und Bemusterung bei
Neuprojekten/Änderungen (technisch prozessgestaltend).
