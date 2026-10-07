# Abschnitt 7.5.4 Verfahren — Review (Zwischenstand)

Status: **in Bearbeitung.** Teil des großen, bisher unveränderten
Original-Rohtexts (siehe `PROJEKTSTATUS.md`). Enthält laut erster
Durchsicht: veraltete Rollennamen, eine nie besprochene Rolle
("interner Reklamationskoordinator"), alte interne Dokumentcodes
("7A-51-3", "6A-32-1"), ungeklärte Modul-/Systemnamen.

---

## 7.5.4.1.1 Grobplanung

**Alter Text (Version k, unverändert):**
> "Kundenbestellungen werden vom VKI geprüft und ins FOSS übergeben.
> Entsprechend Lagerstand und Bedarfen werden die Produktionsaufträge
> eingelastet. Im Modul KPLI werden die aktuellen Bedarfe ermittelt."

**Neuer Text:**
> Kundenbestellungen werden vom Verkaufsinnendienst (VKI) geprüft und
> ins FOSS übergeben. Die Produktionsplanung und -steuerung ermittelt
> anhand des KPLI-Moduls die aktuellen Bedarfe und lastet die
> Produktionsaufträge entsprechend Lagerstand und Bedarf ein.

**Klärungen:**
- VKI = Verkaufsinnendienst (neu aufgetretener Begriff, bestätigt)
- KPLI = Modul UND gleichnamiges Meeting sind dasselbe/verknüpft
  (bestätigt, siehe `BEGRIFFE.md`)
- Tätigkeit jetzt explizit der Rolle **Produktionsplanung und
  -steuerung** zugeordnet (vorher unpersönlich/passiv formuliert),
  konsistent mit `PRODUKTIONSPLANUNG.md`

---

## 7.5.4.2 Feinplanung

**Alter Text (Version k, unverändert):**
> "Diese erfolgt aufgrund der freigegebenen FOSS-Aufträge übersichtlich
> in TIG und auf der Planungstafel mit Produktionsinfo der Aufträge
> durch die Produktionsplanung. Die Planungstafel steht der
> Arbeitsvorbereitung der einzelnen Fachabteilungen zur Verfügung,
> wobei in den bereits aufliegenden Aufträgen alle vorzubereitenden
> Details angeführt sind. Gleichzeitig erfolgt täglich bzw. nach Bedarf
> ein kurzes Informationsgespräch an der Planungstafel mit den dazu
> benötigten Personen (AV, QM, Lager, Logistik). Die Planung wird
> täglich aktualisiert, um eine gewisse Flexibilität beizubehalten. Der
> Schichtplan am Bildschirm zeigt die aktuelle Werkerzuteilung an den
> Arbeitsplätzen; die Mitarbeiterqualifikationsmatrix wird dazu
> einbezogen, die entsprechende Produktschulung wird vor der Zuteilung
> des Werkers durch die Stelle Produktionsleitung überprüft."

**Neuer Text:**
> Die Feinplanung erfolgt auf Basis der freigegebenen FOSS-Aufträge
> durch die Produktionsplanung und -steuerung, einschließlich der
> Personaleinsatzplanung unter Berücksichtigung der
> Mitarbeiterqualifikationen. Die konkrete Vorgehensweise ist in einer
> eigenen Anweisung zur Feinplanung geregelt.

**Methodik-Prinzip (für den Rest von 7.5.4 und das gesamte Dokument):**
**Pro eigenständigem Verfahren exakt eine Anweisung, nie eine
unbestimmte Mehrzahl.** Gehören mehrere im Originaltext genannte
Tätigkeiten (hier: Planungswerkzeug-Nutzung UND
Mitarbeiterqualifikationsabgleich) zu demselben Verfahren (hier:
Feinplanung inkl. Personaleinsatzplanung), bekommen sie **eine**
gemeinsame Anweisung. Nur wirklich eigenständige, inhaltlich getrennte
Verfahren bekommen jeweils eine eigene.

**Offener Punkt (für später, außerhalb dieses Dokuments):** Die
Anweisung zur Feinplanung existiert noch nicht und müsste geschaffen
werden (Details: TIG, Planungstafel, Mitarbeiterqualifikationsmatrix,
Schichtplan).

**Weggelassen (vage/unklar, nicht übernommen):** "AV, QM, Lager,
Logistik" als Teilnehmer des täglichen Informationsgesprächs — AV
(Arbeitsvorbereitung, jetzt Digitale Prozessentwicklung & Lean
Management) und QM (unklar: QMB oder QS) waren nicht eindeutig genug
zuordenbar und wurden nicht in den neuen Text übernommen.

## 7.5.4.3 Zeitlich begrenzte Änderungen in der Produktionsprozesslenkung

**Alter Text (Version k, unverändert):**
> "Änderungen werden generell als interne Projekte geführt und
> entsprechend den Erfordernissen an die AV mitgeteilt. In den
> wöchentlichen Produktionsbesprechungen werden die Themen besprochen.
> Im Modul ARPL besteht die Möglichkeit, zeitlich begrenzte Änderungen
> mit Ablauftermin im Arbeitsplan einzutragen; diese Zusatzanweisungen
> sind an den Auftragspapieren ersichtlich, bis die Änderung terminlich
> abgelaufen ist. Temporäre Produktänderungen werden gemäß den
> Anforderungen von PT und QM/RPP auf Konformität geprüft; es erfolgt
> eine Rückmeldung an die Produkttechnik über den Status des
> betreffenden PA's mittels Eintragung im Schichtlogbuch SF/PQB. Ein
> Prüfmittelwechsel erfolgt generell nicht, da nur 1 Satz angefertigt
> wurde. Alle in der Produktion vorhandenen Messmittel haben einen
> gültigen Prüfstatus. Ein Wechsel des Werkzeuges von der
> Standardspritzgussmaschine auf die geeignete Ersatzmaschine ist
> grundsätzlich erlaubt, da in der Prozessentwicklungsphase Vorserie
> immer eine Ausweichmaschine mit bemustert wird. Derselbe Vorgang gilt
> für den Fall, wenn der Standardladungsträger nicht verfügbar ist, mit
> alternativen Gebinden."

**Neuer Text:**
> Änderungen werden generell als interne Projekte geführt und
> entsprechend den Erfordernissen an die Produktionsplanung und
> -steuerung mitgeteilt. In den regelmäßig stattfindenden
> Produktionsbesprechungen werden die Themen besprochen. Im
> FOSS-Modul ARPL (Arbeitsplanpflege) besteht die Möglichkeit, zeitlich
> begrenzte Änderungen mit Ablauftermin im Arbeitsplan einzutragen;
> diese Zusatzanweisungen sind an den Auftragspapieren ersichtlich, bis
> die Änderung terminlich abgelaufen ist. Temporäre Produktänderungen
> werden gemäß den Anforderungen der Produkt-/Projekttechnik und von
> RPP (Robust Production Processes, Team der Qualitätsmanagement-
> Abteilung) auf Konformität geprüft; es erfolgt eine Rückmeldung an
> die Produkt-/Projekttechnik über den Status des betreffenden
> Produktionsauftrags (PA) mittels Eintragung im Schichtlogbuch durch
> Teamleitung Spritzguss-Produktion/PQB. Ein Prüfmittelwechsel erfolgt
> generell nicht, da Prüfmittel nur in der benötigten Anzahl
> angefertigt werden (üblicherweise ein Satz); alle in der Produktion
> vorhandenen Messmittel haben einen gültigen Prüfstatus. Ein Wechsel
> des Werkzeuges von der Standardspritzgussmaschine auf die geeignete
> Ersatzmaschine ist grundsätzlich erlaubt, da in der
> Prozessentwicklungsphase Vorserie immer eine Ausweichmaschine
> mitbemustert wird. Derselbe Vorgang gilt, wenn der
> Standardladungsträger nicht verfügbar ist, mit alternativen
> Gebinden.

**Klärungen:**
- "Wöchentliche Produktionsbesprechungen" existieren nicht als fixer
  Rhythmus → "regelmäßig stattfindende Produktionsbesprechungen"
  (keine konkrete Frequenz im Dokument, siehe Methodik-Grundsatz zu
  variablen Detailangaben)
- ARPL = FOSS-Modul zur Pflege von Arbeitsplänen
- QM = gesamte Qualitätsmanagement-Abteilung mit allen Teilfunktionen;
  QMB = die normativ geforderte Rolle, bei Kienbacher wahrgenommen vom
  Abteilungsleiter QM (bestätigt konsistent mit
  `PROJEKTSTATUS.md`-Organisationsteam-Abschnitt)
- RPP = Robust Production Processes, eigenes Team innerhalb der
  Qualitätsmanagement-Abteilung — das Team, mit dem sich die Produkt-/
  Projekttechnik bei der Lenkungsplan-Pflege abstimmt (siehe
  `PROZESSTECHNIK_BEMUSTERUNG.md`, dort entsprechend korrigiert)
- PA = Produktionsauftrag, eine von mehreren Betriebsauftragskategorien
  (weitere: VA, FGA, MA — hier nicht weiter vertieft)

**Wichtiger Methodik-Hinweis (von Alexander korrigiert):** Eine alte
Rollen-Abkürzung aus Version k (hier: "AV") darf **nicht** automatisch
durch die nächstliegende umbenannte Rolle ersetzt werden — da mehrere
Nachfolgerollen infrage kommen können (hier: Digitale
Prozessentwicklung & Lean Management, Produktionsplanung und
-steuerung, oder Prozesstechnik und Bemusterung), muss **vor** der
Ersetzung immer nachgefragt werden, welche Rolle inhaltlich tatsächlich
gemeint ist. In diesem Fall: **Produktionsplanung und -steuerung**.

## 7.5.4.4 Abwicklung der Produktionsaufträge

**Alter Text (Version k, unverändert):**
> "Für die allgemeine Vorbereitung der Formen ist der Schichtführer
> zuständig. Der Einbau der Formen erfolgt durch den Schichtführer oder
> mit Aushilfe geschulter Mitarbeiter bei Bedarf. Produktionslogistik /
> Wareneingang ist für die rechtzeitige Vorbereitung der entsprechenden
> Einlegeteile zuständig, Boxenbauer für die Gebindebereitstellung und
> interne Transporte von der Produktion ins Lager. Der Lagerarbeiter
> ist für die rechtzeitige Vorbereitung der Materialien zuständig. Der
> Schichtführer hat nun die Aufgabe, die Produktion abzuwickeln
> (7A-51-3), entsprechende Qualitätskontrollen mittels Prüfbegleitkarte
> durchzuführen und Vorkommnisse zu beheben."

**Neuer Text:**
> **7.5.4.4 Abwicklung der Produktionsaufträge (exemplarisch für
> Spritzguss)**
>
> Für die allgemeine Vorbereitung der Spritzgusswerkzeuge ist die
> Teamleitung Spritzguss-Produktion verantwortlich. Der Einbau der
> Werkzeuge erfolgt primär durch Einsteller/Rüster. Die
> Produktionslogistik ist für die rechtzeitige Vorbereitung der
> Einlegeteile zuständig, der Boxenbauer für die Gebindebereitstellung
> und interne Transporte von der Produktion ins Lager. Die Teamleitung
> Lager ist für die rechtzeitige Vorbereitung der Materialien
> zuständig. Die Teamleitung Spritzguss-Produktion wickelt die
> Produktion ab, führt die entsprechenden Qualitätskontrollen mittels
> Prüfbegleitkarte durch und behebt Vorkommnisse.

**Korrekturen/Klärungen:**
- "Formen" → "Spritzgusswerkzeuge" (Begriffskonsistenz)
- Klammerzusatz in der Überschrift ("exemplarisch für Spritzguss")
  statt zusätzlichem Satz im Fließtext — macht transparent, dass
  analoge Abläufe in anderen Bereichen gelten (z. B. Kleben in der
  Endfertigung), ohne das explizit auszuformulieren
- "(7A-51-3)" entfernt (alter interner Dokumentcode, siehe
  `MITGELTENDE_UNTERLAGEN.md`-Prinzip: keine konkreten
  Dokumentnummern im Fließtext)
- "Lagerarbeiter" → "Teamleitung Lager" (konsistent mit `LAGER.md`)

**Wichtiger Methodik-Fund (neue Rolle entdeckt durch Rollen-Gegenprüfung):**
Der Satz "Einbau erfolgt primär durch Einsteller/Rüster" wurde zunächst
vorschnell übernommen (von Alexander als Korrektur eingebracht), stand
aber im Widerspruch zu `SCHICHTFUEHRER.md` Themenblock 1 ("Umbau und
Einstellung der Produktionsmaschinen" als Teamleitungs-Aufgabe). Nach
systematischer Gegenprüfung **aller** Rollen (nicht nur der
naheliegendsten) stellte sich heraus: "Einsteller/Rüster" ist
tatsächlich eine **neue, eigenständige Fachrolle** (bereits in
`PRODUKTIONSLEITER.md` Themenblock 14 als unterstelltes Personal der
Teamleitung erwähnt, aber nie eigens ausgearbeitet) — siehe
`EINSTELLER_RUESTER.md`. Kein Widerspruch: Teamleitung bleibt
verantwortlich/entscheidungsbefugt (Parametrierung, finale Freigabe mit
PQB), Einsteller/Rüster führen den Einbau als unterstelltes Fachpersonal
durch.

**Methodik-Grundsatz (von Alexander verschärft):** Bei jeder
Rollenzuordnung in 7.5.4 müssen **alle** bereits bestehenden Rollen
gegengeprüft werden (nicht nur die naheliegendste), um Widersprüche zu
bestehenden AKV-Inhalten zu vermeiden.

## 7.5.4.5 Abweichungsmanagement im laufenden Betrieb (vormals "Begleitende Produktionsarbeiten")

**Alter Text (Version k, unverändert):**
> "Störungen werden, wenn möglich, sogleich behoben. Vom QMB / PL wird
> dann geprüft, ob Korrekturmaßnahmen notwendig sind, um
> Wiederholungsfehler zu vermeiden. Laufende Qualitätskontrollen werden
> vom PQB nach geregelter Häufigkeit lt. Arbeits- und Prüfanweisung
> durchgeführt und protokolliert. Interne Reklamationen werden über den
> Reklamationsbericht dokumentiert; der interne Reklamationskoordinator
> führt die Maßnahmenverfolgung nach dem 8D-Verfahren durch. Eine
> geregelte Wartung u. Instandhaltung (siehe Wartungslisten) dient als
> vorbeugende Maßnahme zur Produktionssicherheit (6A-32-1). Der
> Teamleader ist für die Auslieferqualität, für die Auswertung der
> Produktionsvorkommnisse verantwortlich u. hat bei Bedarf Maßnahmen
> einzuleiten."

**Neuer Text:**
> Störungen werden, wenn möglich, sogleich behoben. Die QS prüft
> anschließend, ob Korrekturmaßnahmen notwendig sind, um
> Wiederholungsfehler zu vermeiden. Laufende Qualitätskontrollen werden
> vom PQB nach geregelter Häufigkeit lt. Arbeits- und Prüfanweisung
> durchgeführt und protokolliert. Reklamationen mit externer Relevanz
> werden über einen 8D-Report bearbeitet: Der Auftrag dazu ergeht vom
> QMB an den Produktionsleiter, die QS unterstützt bei der
> Durchführung. Eine geregelte Wartung und Instandhaltung dient als
> vorbeugende Maßnahme zur Produktionssicherheit. Die Teamleitung
> Spritzguss-Produktion ist für die Auslieferqualität sowie die
> Auswertung der Produktionsvorkommnisse verantwortlich und hat bei
> Bedarf Maßnahmen einzuleiten.

**Korrekturen/Klärungen (gegen alle bestehenden Rollen geprüft):**
- **"QMB / PL" → "QS"** beim Korrekturmaßnahmen-Check: Per
  `QS.md` ist es QS, die den Bedarf feststellt (nicht QMB), während
  die Produktionsleitung entscheidet
- **"Interner Reklamationskoordinator" entfernt** — diese Rolle
  existiert nicht. Geklärter Ablauf: Reklamationen mit **externer
  Relevanz** werden im Auftrag des QMB vom **Produktionsleiter**
  bearbeitet (8D-Report), **QS unterstützt**. Abgrenzung zu
  Teamleitung/PQB (die allgemein auch Maßnahmenverfolgung bei
  Q-Abweichungen machen, siehe `PQB.md`): die externe Relevanz/der
  Kundenbezug. `QS.md` bleibt unverändert (Formulierung dort passt
  bereits).
- "(siehe Wartungslisten)" und alter Dokumentcode "(6A-32-1)" entfernt
- "Teamleader" → "Teamleitung Spritzguss-Produktion" (konsistent mit
  "exemplarisch für Spritzguss"-Rahmen aus 7.5.4.4)
- **Überschrift geändert:** "Begleitende Produktionsarbeiten" (vage) →
  "Abweichungsmanagement im laufenden Betrieb" (präziser,
  etablierter QM-Begriff, deckt Störungen/Qualitätsabweichungen/
  Reklamationen einheitlich ab)

## 7.5.4.6 Material

*Noch zu bearbeiten.*
