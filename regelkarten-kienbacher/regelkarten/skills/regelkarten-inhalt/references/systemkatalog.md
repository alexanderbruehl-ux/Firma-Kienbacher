# Systeme, Listen und Begriffe

**Nur was hier steht, darf ohne Rückfrage auf eine Karte.** Alles andere —
Modulnamen, Masken, Feldnamen, Tastenkombinationen, Buchungsarten, Berechtigungen —
wird beim Ersteller erfragt. Erfinden ist ausgeschlossen: eine erfundene Maske
kostet den Werker an der Maschine echte Zeit und die Karte ihre Glaubwürdigkeit.

## ERP und Systeme

| Kürzel | Was belegt ist | Quelle |
|---|---|---|
| **BARI** | zeigt zum Arbeitsgang Sollmenge, Istmenge und Ausschuss; dient der Mengenprüfung | RK-007 |
| **BARU** | zeigt die Etikettenbuchung im Anschluss | RK-007 |
| **ARLG** | zeigt den Materialbestand; dient der Bestandsprüfung | RK-008 |
| **FOSS-ORDAT** | ERP-Umgebung | Regelkarte „Auftrag fertig" Rev. 0.6 |
| **AG 300** | Kontrollarbeitsgang, auf den die Etikettenbuchung meistens läuft. Ein Auftrag kann mehrere Arbeitsgänge haben. | RK-007 |
| **TIG** | zeigt Ist- und Sollmenge | Moritz, 17.09.2026 |
| **KMOB** | Buchungskontrolle | Moritz, 17.09.2026 |
| **DIPO** | zeigt die Abrufe | Moritz, 17.09.2026 |

## Listen und Nachweise

| Name | Wofür | Quelle |
|---|---|---|
| **Schichtlogbuch** | Zeit, Ereignis, Ursache, Maßnahme, Neustart | Losenstein A1, A2, B1 |
| **Instandhaltungsliste** | Eintrag nach einer Maschinenstörung | Losenstein A1 |
| **Werkzeugbauliste** | Eintrag nach einem Werkzeugdefekt | Losenstein A2 |
| **Personalplan** | wird bei Personalausfall angepasst | Losenstein B1 |
| **FGA — Freigabeauftrag** | nach einer Reparatur oder Änderung in der Kavität durchzuführen | Losenstein A2 |
| **Prioliste** | Grundlage, wenn die Planung nicht erreichbar ist und das weitere Vorgehen festgelegt werden muss | Moritz, 17.09.2026 |
| **Auftragspapiere** | tragen die Sollmenge | Moritz, 17.09.2026 |
| **Stückzähler an der Maschine** | nur verlässlich, wenn er korrekt zurückgesetzt und die Sollmenge eingestellt ist - siehe Auftragsfreigabe | Moritz, 17.09.2026 |

## Zwei Sätze, die eine Karte falsch machen

- **„Das Modul entscheidet."** Ein ERP-Modul zeigt Informationen oder verarbeitet
  Buchungen. Über einen betrieblichen Ablauf entscheidet eine **Rolle**. Also nicht
  „BARI gibt frei", sondern „Der Schichtführer prüft in BARI und entscheidet".
- **„Buchen wie beim Etikett."** Angaben aus einem Vorgang werden nicht auf einen
  anderen übertragen, nur weil es ähnlich klingt. Für das Umpacketikett etwa sind
  BARI, BARU, Kontrollarbeitsgang und AG 300 ausdrücklich **nicht** bestätigt.

## Wenn etwas fehlt

Frag nach — gebündelt, nicht einzeln. Die fünf Fragen, die fast immer reichen:

1. In welchem Modul beginnt der Vorgang, und welche Maske oder Funktion wird geöffnet?
2. Welche Angaben werden eingegeben oder gescannt, und woher kommen sie?
3. Welcher Schritt ist nur Anzeige oder Druck, welcher verändert Menge, Gebinde,
   Charge oder Lagerort?
4. Was wird danach geprüft, und woran erkennt man, dass es gestimmt hat?
5. Wer hilft bei einer Abweichung?

Bis das geklärt ist, kommt der Schritt als **offene Frage** auf die Karte oder gar
nicht — nie als fertige Arbeitsanweisung.
