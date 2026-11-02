# Sprint 3 – Installation und Stabilisierung

Nachweise zu WEA-36/37 (Installation und README) und Stand der offenen Punkte
aus WEA-41. Der Arbeitsplan für Sprint 3 steht in [sprint-3.md](sprint-3.md).

## WEA-36/37: Installation und README

Am 26.10.2026 wurde das Paket von Lionel in einer frischen Windows-Umgebung
installiert:

```powershell
python -m venv .venv-wea36
.venv-wea36\Scripts\python.exe -m pip install .
.venv-wea36\Scripts\weather.exe --help
.venv-wea36\Scripts\weather.exe "Zürich"
.venv-wea36\Scripts\weather.exe "New York"
.venv-wea36\Scripts\weather.exe "Zürich" --morgen
```

Installation und Aufruf funktionierten. Die Ausgaben mit `Zürich` und `Bewölkt`
wurden in einer UTF-8-PowerShell geprüft. Die morgige Vorhersage verwendet den
nächsten Kalendertag in der Zeitzone des Orts.

Nico hat denselben Weg am 26.10.2026 unabhängig in einer frischen venv
nachgespielt (`python -m venv`, `python -m pip install .`, `weather "Zürich"`):
läuft ohne Fehler, Exit 0, keine externen Laufzeitpakete. Die Live-Beispiele in
der [README](../README.md) sind auf diesen Stand aktualisiert.

**US-07, AK 4 (nachgetragen am 02.11.2026, nach Sprint 3):** Auf Stand `77c21be`
wurden die fünf README-Schritte in einem frischen Klon auf Windows 11 mit
Python 3.13 ausgeführt. Eduart hat keinen Code geschrieben und hat die Prüfung in
Auftrag gegeben; ausgeführt hat sie Claude Code auf Eduarts Rechner. Alle Schritte
liefen ohne Änderung, die Aktivierung über `Activate.ps1` eingeschlossen.
`weather "Zürich"` und `weather "Zürich" --morgen` endeten mit Exit 0. Die
Bestätigung im YouTrack-Ticket WEA-36 steht noch aus.

Hinweis zum Verhalten bei fehlenden Daten: Die Vorhersage meldet keinen Fehler,
wenn Tageswerte fehlen, sondern gibt «Vorhersage nicht verfügbar»
beziehungsweise «Wetterzustand nicht verfügbar» aus und behält Exit-Code 0
(US-06, AK 3). Ein Fehler mit Exit 1 entsteht nur, wenn der Dienst nicht
erreichbar ist oder der Ort unbekannt beziehungsweise mehrdeutig ist.

## WEA-41: Stabilisierung

- `python -m unittest discover -s tests`: 58 Tests erfolgreich auf `main`
  (Stand 26.10.2026, nach dem Merge von US-06 und dieser README-Änderung).
- Umlaute: in einer UTF-8-Konsole alles korrekt; in einer cp1252-Konsole sind
  `ü`, `ö` und `°` ebenfalls korrekt, nur Zeichen ausserhalb von cp1252 werden
  zu `?` statt zum Abbruch (`weather "Łódź"` → Exit 0). Details im
  [Demo-Ablauf](sprint-3-demo.md).
- Commit `b4be608` liegt weiterhin nur auf `feature/WEA-22-23-wind`. Er testet
  den Stand vor US-02 und würde auf dem heutigen `main` fehlschlagen; alle Fälle
  daraus sind dort abgedeckt. Empfehlung aus dem Review zu PR #11: nicht
  übernehmen, Branch löschen.
- Startprüfung (DoD 4) im [Portfolio, Sprint 2](portfolio.md): Für Eduart ist
  der Stand `77c21be` am 02.11.2026 nachgetragen, Nico hat am 26.10.2026 den
  Stand vor US-06 geprüft. Fidan und Lionel fehlen ganz. Vor «Done» muss jede der
  vier Personen den aktuellen `main` starten und das Ergebnis dort eintragen.

## WEA-29: Sprint-2-Review

Das Ticket weist die Durchführung Fidan als Scrum Master zu. Fidan muss WEA-9
und WEA-10 einzeln anhand der Akzeptanzkriterien und der Definition of Done
besprechen und das Ergebnis in den beiden YouTrack-Stories dokumentieren. Diese
Teamhandlung ist noch nicht als erfolgt bestätigt.
