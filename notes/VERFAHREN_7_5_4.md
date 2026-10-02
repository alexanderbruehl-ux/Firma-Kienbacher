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

*Noch zu bearbeiten.*

## 7.5.4.5 Begleitende Produktionsarbeiten

*Noch zu bearbeiten.*

## 7.5.4.6 Material

*Noch zu bearbeiten.*
