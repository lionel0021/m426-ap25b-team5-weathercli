# WeatherCLI

Aktueller Arbeitsumfang: **nur Sprint 1**, US-01, US-04 und US-05.
Python 3.10+. US-02 (Wetterzustand) und US-03 (Wind) sind für Sprint 2 geplant.
Windanzeige und zugehörige Tests wurden aus dem aktuellen Stand entfernt.

## Start

```powershell
python -m weathercli --help
python -m weathercli "Zürich"
python -m weathercli "New York"
```

Hilfe und Eingabeprüfung funktionieren. Die API-Funktionen sind lokal noch
Platzhalter: Wetteraufrufe enden derzeit mit einer deutlichen Fehlermeldung und
Exit-Code 1. Nico integriert die echten Abfragen.

Optional unter Windows:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -e .
.venv\Scripts\weather --help
```

Unter Linux/macOS liegen diese Programme in `.venv/bin/`.
Keine externen Laufzeitpakete erforderlich; die Installation nutzt setuptools.

## Neue Verteilung

| Sprint | Lionel | Nico (nico.schult) |
| --- | --- | --- |
| 1 | WEA-13,14,17,18: Projekt, CLI, Temperaturausgabe, Fehlerbehandlung | WEA-15,16: Ortssuche und Wetter-API |
| 1 | WEA-26,27,28: Hilfe und unbekannte Optionen (US-05) | WEA-24,25: Ortsnamen und Eingabeprüfung (US-04) |
| 2 | WEA-22,23: Wind (US-03), noch offen | WEA-19,20,21: Wetterzustand (US-02), noch offen |

Die neue Verteilung berücksichtigt den höheren Aufwand der API-Anbindungen.
Sie ist eine Arbeitsteilung, keine bestätigte exakte 50/50-Stundenschätzung.
Die bestehende Ortsnamen-Verarbeitung inklusive Tests wird Nico zur Prüfung
übergeben; sie muss nicht neu geschrieben werden.

## Schnittstelle für Sprint 1

- Nico: `client.resolve_city(city) -> Location`, Geocoding mit `count=5`,
  `language=de`. Dazu `errors.request_json` und `errors.unique_location` nutzen.
- Nico: `client.current_temperature(location) -> float`, Forecast mit
  `current=temperature_2m`, `temperature_unit=celsius`. Antwort über
  `errors.temperature_from_response` prüfen; fehlende Temperatur ist ein Fehler.
- `client.current_weather` bleibt als kompatibler Adapter für die CLI bestehen.
  Es liefert nur `current.temperature_2m` und die geprüfte Einheit `°C`.
  Nico kann alternativ direkt eine validierte API-Antwort zurückgeben.
- Lionel: `errors.py` behandelt HTTP-/DNS-/Timeoutfehler, ungültiges JSON,
  API-Fehler, unbekannte/mehrdeutige Orte und ungültige Orts-/Temperaturdaten.
  Diese Helfer sind getestet; Nico muss sie in die echten API-Aufrufe einbinden.
- `output.format_weather` zeigt nur Ort, Land und Temperatur.
- `WeatherError`: CLI schreibt auf stderr und endet mit Code 1. Eingabefehler:
  Code 2. Erfolg/Hilfe: Code 0. Keine erfundenen Wetterwerte.

API-Dokumentation: [Geocoding](https://open-meteo.com/en/docs/geocoding-api),
[Wetterabfrage](https://open-meteo.com/en/docs).

## Tests und Abnahme

```powershell
python -m unittest discover -s tests -v
```

20 Tests erfolgreich, ohne Live-API. Die End-to-End-Abnahme erfolgt nach Nicos
Integration. Review, Commit/Integration in den gemeinsamen Hauptbranch und
Startprüfungen bei allen Teammitgliedern fehlen noch.
Siehe [Sprintplan und Prüfnachweis](doc/sprint-1.md) und
[Definition of Done](doc/definition-of-done.md).
