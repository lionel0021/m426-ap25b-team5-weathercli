# Zwei Sprints – aktueller Arbeitsumfang nur Sprint 1

## Verbindliche Arbeitsaufteilung dieses Auftrags

| Sprint | Stories | Nutzerergebnis |
| --- | --- | --- |
| 1 | US-01 (WEA-8), US-04 (WEA-11), US-05 (WEA-12) | Temperaturabfrage, Ortsnamen und Hilfe |
| 2 | US-02 (WEA-9), US-03 (WEA-10) | Wetterzustand und Wind |

Diese Aufteilung ersetzt den früheren Vorschlag, alle fünf Stories in Sprint 1
umzusetzen. Sprint 2 wird jetzt nur geplant, nicht implementiert.
Die Windfunktion wurde aus dem lokalen Code entfernt.

## Verantwortliche

| Entwickler | Sprint 1 | Sprint 2, offen |
| --- | --- | --- |
| Lionel | WEA-13,14,17,18,26,27,28 | WEA-22,23 |
| Nico (nico.schult) | WEA-15,16,24,25 | WEA-19,20,21 |

Lionel übernimmt zusätzlich die Fehlerbehandlung (WEA-18), Nico übernimmt
US-04. Die vorhandene Umsetzung der Ortsnamen-Verarbeitung wird zur Prüfung
übergeben und bleibt erhalten. WEA-16 war bereits bei Nico in Bearbeitung.
API-Arbeit wird höher gewichtet als einzelne CLI-Tasks; eine genaue
50/50-Stundenverteilung ist ohne gemeinsame Schätzung nicht belegt.

## Aktueller Nachweis

`python -m unittest discover -s tests -v`: **34 Tests erfolgreich**.

- Projekt, CLI und Ausgabe: Name, Land, Celsius, Null/negative Werte, Exit-Codes.
- WEA-18: Timeout, DNS, HTTP 503, unvollständige HTTP-Antwort, ungültiges JSON,
  API-Fehler, keine/mehrere Orte, ungültige Koordinaten und fehlende Temperatur.
- US-04: vollständiger mehrteiliger Name, Trimmen, leere/unquotierte Argumente;
  vorhandene Umsetzung zur Prüfung an Nico übergeben.
- US-05: Zweck, Syntax und Beispiele, Offline-Hilfe, unbekannte Option,
  Prozess-Exit-Codes.
- WEA-15, WEA-16 (Nico): Abfrageparameter, Auswahl des gemeinten Orts
  (Zürich, New York, Frankfurt), mehrdeutige und fehlende Orte, ungültige
  Ortsdaten, Temperatur inklusive 0 und negativ, fehlende Temperatur/Einheit.

Keine Wind- oder Wetterzustandsfunktion ist enthalten. Netzwerkfehler werden
mit simulierten Antworten getestet. Die Live-Abnahme des vollständigen
Nutzerablaufs vom 21.09.2026 steht in [us-01-validation.md](us-01-validation.md).
Die Schnittstelle für seine Integration steht in der README.

## Vorgehen und Status

Die Issues existierten vor der Umsetzung. Lionels Tasks sind über 50f2e05 und
Nicos API-Anbindung über PR #8 auf `main`; Nico hat Lionels Tasks geprüft,
Eduart hat Nicos PR freigegeben. US-01, US-04 und US-05 stehen in YouTrack auf
Done. Die verschobenen Wetterzustands- und Wind-Tasks gehören zu Sprint 2.

## Team-Startprüfung und Velocity vom 28.09.2026

Alle vier Teammitglieder haben bestätigt, dass sie WeatherCLI anhand der
dokumentierten Startanleitung auf ihrem Gerät starten und einen erfolgreichen
Beispielaufruf ausführen können.

| Teammitglied | Startprüfung |
| --- | --- |
| Eduart | erfolgreich |
| Fidan | erfolgreich |
| Lionel | erfolgreich |
| Nico | erfolgreich |

Damit ist Punkt 4 der Definition of Done für die abgeschlossenen
Sprint-1-Stories erfüllt. Die Velocity wird nur aus vollständig abgeschlossenen
User Stories berechnet:

| Abgeschlossene Story | Story Points |
| --- | ---: |
| US-01 / WEA-8 | 8 |
| US-04 / WEA-11 | 3 |
| US-05 / WEA-12 | 2 |
| **Velocity Sprint 1** | **13** |

## Grenze der YouTrack-Zuordnung

Die Sprintplanung wird in den Ticketbeschreibungen und hier festgehalten.
Das Erstellen eines Board-Sprints war zuerst mit HTTP 403 blockiert; seit
21.09.2026 besteht der Sprint "Sprint 1" auf beiden Boards. Dort liegen aber
auch US-02 und US-03, die nach dieser Planung erst zu Sprint 2 gehören - solange
das so bleibt, erreicht der Sprint-1-Burndown nie null. Das klärt der PO.
Sprint-2-Termine sind noch nicht festgelegt. Die früher blockierten Admin-Punkte
(Boardkopie löschen, Zugriffsnachweis nicolai.fricker) bleiben offen.
