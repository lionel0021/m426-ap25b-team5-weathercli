# Sprint 3 – Stabilisierung und Installation

## WEA-36/37: Installation und README

Am 26.10.2026 wurde das Paket in einer frischen Windows-Umgebung installiert:

```powershell
python -m venv .venv-wea36
.venv-wea36\Scripts\python.exe -m pip install .
.venv-wea36\Scripts\weather.exe --help
.venv-wea36\Scripts\weather.exe "Zürich"
.venv-wea36\Scripts\weather.exe "New York"
.venv-wea36\Scripts\weather.exe "Zürich" --morgen
```

Installation und Aufruf funktionierten. Die Live-Beispiele stehen in der
[README](../README.md). Die Ausgaben mit `Zürich` und `Bewölkt` wurden in einer
UTF-8-PowerShell geprüft. Die morgige Vorhersage verwendet den nächsten
Kalendertag in der Ortszeitzone.

Die CLI-Änderung ergänzt `--morgen`; Open-Meteo liefert tägliche Tiefst- und
Höchsttemperatur, Wettercode und maximale Windgeschwindigkeit für den Folgetag.
Die Vorhersage meldet einen verständlichen Fehler, wenn Pflichtwerte fehlen.

## WEA-41: Stabilisierung

- `python -m unittest discover -s tests -v`: 47 Tests erfolgreich auf dem
  Arbeitsbranch.
- Der lokale Branch `feature/WEA-22-23-wind` zeigt auf `b4be608`; der Commit
  ist damit weiter auf diesem Branch vorhanden.
- Der `--morgen`-Aufruf und Umlaute in `Zürich` und `Bewölkt` liefen in der
  frisch installierten Umgebung.
- Die Startprüfung durch alle vier Teammitglieder ist noch offen. Die
  bestehenden Einträge für Fidan, Lionel und Nico stehen in
  [Portfolio, Sprint 2](portfolio.md#sprint-2-28092026-und-19102026-review-und-retro-am-26102026);
  Eduarts Eintrag bezieht sich auf einen früheren Stand. Vor «Done» müssen alle
  vier den neuen Stand starten und ihre Ergebnisse dort bestätigen.
- Die Tests sind auf dem Arbeitsbranch gelaufen. Nach Integration in `main`
  müssen sie dort erneut geprüft werden.

## WEA-29: Sprint-2-Review

Das Ticket weist die Durchführung Fidan als Scrum Master zu. Fidan muss WEA-9
und WEA-10 einzeln anhand der Akzeptanzkriterien und DoD besprechen und das
Ergebnis in den beiden YouTrack-Stories dokumentieren. Diese Teamhandlung ist
noch nicht als erfolgt bestätigt.
