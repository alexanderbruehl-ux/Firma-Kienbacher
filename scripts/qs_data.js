const GRUNDSAETZLICHES = [
  "QS ist keine Serienfunktion für wiederkehrende, zyklische Prüfungen — das ist Aufgabe der PQB",
  "QS ist auch nicht für die Freigabe einzelner Produktionsaufträge zuständig",
  "QS agiert als übergeordnete, weiter und umfassender erfahrene und geschulte Q-Instanz",
];

const AUFGABEN = [
  "Sperren, Beurteilung, Pflege von Grenzmusterkatalogen, Erststückfreigaben (Systematik/Grundlagen) sowie interne Maßnahmen zur Verbesserung/Vermeidung von Reklamationen",
  "Beratung des Produktionsleiters bei strukturierter Problemlösung (8D) bei internen Qualitätsabweichungen",
  "Beurteilung der vom Produktionsleiter gesetzten Sofort-/Korrekturmaßnahmen; gemeinsame Prüfung der Wirksamkeit",
  "Entscheidung, ob und wie fehlerhafte Teile nachgearbeitet/repariert werden dürfen, inkl. erneuter Prüfung danach",
  "Durchführung/Koordination interner Prozess- und Produktaudits (über die laufende PQB-Prüfung hinaus)",
  "Überwachung, ob bei Prozessabweichungen die im Lenkungsplan festgelegten Reaktionspläne eingehalten werden",
  "Übergreifende Koordination/Steuerung der Tätigkeit der schichtbezogen aufgeteilten PQB",
  "Unterstützung des Produktionsleiters bei 8D-Reports zu Reklamationen mit externer Relevanz (Auftrag kommt vom QMB)",
  "Gemeinsame Definition von Vermeidungs-/Abstellmaßnahmen mit der Teamleitung bei Kundenreklamationen-Sofortmaßnahmen",
  "Prüfung nach Störungsbehebung, ob Korrekturmaßnahmen notwendig sind, um Wiederholungsfehler zu vermeiden",
  "Mitwirkung als Fachabteilung bei Unterweisungen (neben HR, SVP, SFK)",
  "Einbindung bei multidisziplinären, automatisierungsbedingten Prozessänderungen",
  "Kontrolle, Unterstützung und Einschulung neuen Personals (Qualitätsthemen)",
  "Kontrolle aller laufenden Aufträge: Teile- und Maschinenzustand, Ausschussquote, korrekte Ausschuss-Trennung direkt an der Maschine, korrekte Buchungen, ordnungsgemäße Auftragsvorbereitung (Erststück, Rückstellmuster, vollständig ausgefüllte Dokumente, gekennzeichnete Ausschussbehälter)",
  "Kontrolle, ob alle Gebinde (interne Gebinde oder Ausliefergebinde) korrekt laut Auftrag vorbereitet, gebucht und bezettelt sind",
  "Kontrolle, ob Arbeitsanweisungen und Verpackungsvorschriften am mobilen PC geöffnet/verfügbar sind",
  "Prüfung der Anweisungen auf Aktualität (hat sich im Prozess etwas geändert?)",
  "Kontrolle von Auffälligkeiten bei den Bauteilen; Besprechung von Werkzeugthemen (z. B. notwendige Reparaturen wie Grate, Verschmutzungen, Spritzprobleme) mit Schichtführer/Einsteller/Rüster und bei Bedarf mit Werkzeugbau",
  "Festlegung von FGAs (Freigabeauftrag) nach Werkzeugwartung/-reparatur aufgrund von Qualitätsthemen",
  "Kontrolle des Schichtlogbuchs auf Vollständigkeit (inkl. Vorkommnisse der 2. und 3. Schicht); Kontrolle der PQB-Einträge und der Schichtführer-Einträge",
  "Überblick über die Zuordnung des Personals zu den Maschinen, um den bestmöglichen Einsatz (Qualifikation und Produktivität) mit zu beurteilen",
  "Durchsicht des täglichen Ausschussberichts je Auftrag/Bauteil",
  "Kontrolle und Verifizierung der Buchungscodes auf Korrektheit; bei Auffälligkeiten Rückfrage und Korrektur",
  "Kontrolle des Bestands und der Abarbeitung des Sperrlagers (Nacharbeits-Aufträge)",
  "Organisation der erforderlichen Nacharbeit in Abstimmung mit der Produktionsplanung und -steuerung (PPS) bzgl. verfügbarem Personal",
  "Rückstellmusterkontrolle: Prüfung nach jeder abgeschlossenen Produktion, ob das Rückstellmuster (letztes Stück) den Qualitätsanforderungen entspricht — bei i. O. Ablage im RM-Regal, bei NIO Rückverfolgung des ersten Auftretens der Abweichung",
  "Laufende persönliche Betreuung/Beratung der anwesenden PQB",
  "Fachlicher Austausch vor Ort zu allen relevanten Tagesthemen",
  "Aktualisierung der Qualifikationsmatrix; dokumentierte Durchführung von Mitarbeiterschulungen (z. B. bei neuen Mitarbeitern oder Qualitätsproblemen)",
  "Beratende Begleitung aktueller Bemusterungsaufträge gegenüber Bemusterer und Technik: Sichtung der Qualitätsanforderungen der zu bemusternden Teile und Prüfung am Bauteil",
  "Anlage des Rückstellmusters im System (FOSS)",
  "Stichprobenprüfung an laufenden Bauteilen (visuell) als nächste Instanz nach PQB; Beauftragung von Bauteil-Messungen bei vermuteten Qualitätsabweichungen (zusätzlich zur 2-Stunden-Kontrolle der PQB)",
  "Bei SPAs (Sonderaufträgen) und speziellen Aufträgen (z. B. FGAs): Freigabe im Zweifelsfall durch QS anstelle der PQB",
  "Anstoß zur Anpassung von Arbeitsanweisungen und Verpackungsvorschriften; Durchführung von Packversuchen und Erarbeitung von Arbeitsabläufen inkl. Hilfsmittel/Ausstattung in Zusammenarbeit mit Projekttechnik und Verpackungsmanagement",
];

const VERANTWORTLICHKEIT = [
  "Vertretung des Produktionsleiters in allen qualitätsrelevanten Fragen (Bereich 3 von 3 der Vertretungsstruktur)",
  "Befugnis, Produktion/Versand zu stoppen, um Qualitätsprobleme zu korrigieren",
  "Fachliche Weisungsbefugnis gegenüber dem Produktionsleiter in Q-Themen (spätestens über den QMB durchsetzbar)",
  "Organisatorisch übergeordnet zu den PQB",
  "Freigabe-/Entscheidungsbefugnis bei Korrekturmaßnahmen (gibt nach Wirksamkeitsprüfung frei, z. B. Entsperren von Teilen/Prozessen)",
  "Verantwortlich dafür, dass bei Prozessabweichungen die Reaktionspläne aus dem Lenkungsplan eingehalten werden",
];

module.exports = { GRUNDSAETZLICHES, AUFGABEN, VERANTWORTLICHKEIT };
