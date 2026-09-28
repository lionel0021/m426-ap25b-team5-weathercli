# WeatherCLI

Umgesetzt: US-01, US-04 und US-05 aus Sprint 1, dazu US-02 (Wetterzustand) und
US-03 (Wind) aus Sprint 2. Python 3.10+.

## Start

```powershell
python -m weathercli --help
python -m weathercli "Zürich"
python -m weathercli "New York"
```

Ausgabe zum Beispiel `Zürich, Schweiz: 15.4 °C, Klar, Wind: 12.4 km/h`. Ort,
Temperatur, Wetterzustand und Wind stammen aus einer Abfrage bei Open-Meteo
(kein API-Schlüssel); dafür ist eine Internetverbindung nötig. Fehlt ein Wert,
steht dort `Wetterzustand nicht verfügbar` oder `Wind nicht verfügbar`, die
übrigen Angaben bleiben sichtbar.

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
| 2 | WEA-22,23: Wind (US-03), in Umsetzung | WEA-19,20,21: Wetterzustand (US-02), noch offen |

Die neue Verteilung berücksichtigt den höheren Aufwand der API-Anbindungen.
Sie ist eine Arbeitsteilung, keine bestätigte exakte 50/50-Stundenschätzung.
Die bestehende Ortsnamen-Verarbeitung inklusive Tests wird Nico zur Prüfung
übergeben; sie muss nicht neu geschrieben werden.

## API- und Ausgabeschnittstelle

- Nico: `client.resolve_city(city) -> Location`, Geocoding mit `count=20`,
  `language=de`, geprüft über `errors.request_json` und `errors.unique_location`.
  `count=20`, weil bei `count=5` für "New York" New York City fehlt.
  Vor der Prüfung bleiben nur passende Orte: Name gleich der Eingabe oder mit ihr
  als ganzem Wort beginnend, ohne Stadtteile; Gross/Klein und Akzente zählen nicht.
  Hat ein Ort mindestens zehnmal mehr Einwohner als jeder andere, gilt er als
  gemeint ("Zürich"), sonst ist die Eingabe mehrdeutig ("Springfield").
- Nico: `client.current_temperature(location) -> float`, Forecast mit
  `current=temperature_2m`, `temperature_unit=celsius`. Antwort über
  `errors.temperature_from_response` prüfen; fehlende Temperatur ist ein Fehler.
- `client.current_weather` fragt Temperatur und `wind_speed_10m` gemeinsam ab.
  Temperatur wird als °C validiert; Wind wird nur mit endlichem Zahlenwert und
  bestätigter Einheit km/h übernommen. `0 km/h` ist ein gültiger Wert.
- Lionel: `errors.py` behandelt HTTP-/DNS-/Timeoutfehler, ungültiges JSON,
  API-Fehler, unbekannte/mehrdeutige Orte und ungültige Orts-/Temperaturdaten.
  Diese Helfer sind getestet; Nico muss sie in die echten API-Aufrufe einbinden.
- Nico: `conditions.condition_from_response(data) -> str | None` (WEA-19, WEA-20)
  liest `weather_code` und übersetzt ihn über `WMO_CONDITIONS` ins Deutsche;
  fehlender oder unbekannter Code ergibt `None`.
- `client.current_weather` fragt `current=temperature_2m,weather_code,wind_speed_10m`
  mit `wind_speed_unit=kmh` in einem Aufruf ab, damit alle Werte aus derselben
  Messung stammen. Die Temperatur ist Pflicht, Zustand und Wind sind optional.
- `output.format_weather` zeigt Ort, Land, Temperatur, Wetterzustand (WEA-21) und
  Wind (WEA-22/23); fehlt ein optionaler Wert, steht dort der Hinweis dazu.
- `WeatherError`: CLI schreibt auf stderr und endet mit Code 1. Eingabefehler:
  Code 2. Erfolg/Hilfe: Code 0. Keine erfundenen Wetterwerte.

API-Dokumentation: [Geocoding](https://open-meteo.com/en/docs/geocoding-api),
[Wetterabfrage](https://open-meteo.com/en/docs).

## Tests und Abnahme

```powershell
python -m unittest discover -s tests -v
```

Der Sprint-1-Prüfnachweis mit 33 Tests und ohne Live-API steht in
[us-01-validation.md](doc/us-01-validation.md). Für die aktuelle Sprint-2-
Windänderung wurden in diesem Arbeitsgang keine Tests ausgeführt. Review und
Startprüfungen bei allen Teammitgliedern stehen noch aus.
Siehe [Sprintplan und Prüfnachweis](doc/sprint-1.md) und
[Definition of Done](doc/definition-of-done.md).
