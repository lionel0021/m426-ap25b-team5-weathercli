# Sprint 3 – Arbeitsplan für die Developer (26.10.2026)

Sprint 3 hat einen Modultag. Akzeptanzkriterien und Begründung stehen im
[Product Backlog](product-backlog.md#sprint-3--refinement-und-planung-26102026).
Diese Seite beschreibt, was konkret gebaut wird. Die Zuordnung ist ein Vorschlag;
Tasks werden gezogen, nicht verteilt.

## Reihenfolge

| Schritt | Eintrag | Vorschlag | Branch |
| ---: | --- | --- | --- |
| 1 | US-06 (WEA-31) Task WEA-32: Abfrage für morgen | Nico | `feature/US-06-morgen` |
| 1 | US-06 Tasks WEA-33 und WEA-34: Ausgabe und Option `--morgen` | Lionel | `feature/US-06-morgen` |
| 2 | US-06 Task WEA-35: Tests, PR, Review | Lionel und Nico | `feature/US-06-morgen` |
| 3 | US-07 (WEA-36) README und Installation, WEA-37 und WEA-38 | Lionel oder Nico, Prüfung durch Eduart oder Fidan | `docs/US-07-readme` |
| 4 | Stabilisieren (WEA-41) | Lionel und Nico | direkt über PRs |
| 4 | Demo vorbereiten (WEA-42) | Fidan | – |
| 4 | Präsentation vorbereiten (WEA-43) | Eduart und Fidan | – |
| 5 | US-08 (WEA-39, Task WEA-40) nur, wenn 1 bis 3 fertig sind | wer frei ist | `feature/US-08-wiederholung` |

Alle Issues liegen in YouTrack (WEA-31 bis WEA-43), niemandem zugewiesen: Wer einen
Task zieht, trägt sich ein und setzt ihn auf «In Arbeit». Jeder Branch startet vom
aktuellen `main`; Commit-Nachrichten nennen die Ticketnummer, z. B. `WEA-32: ...`.

## US-06 – Wetter für morgen sehen

### Task 1: Abfrage (`weathercli/client.py`)

Neue Funktion `tomorrow_forecast(location: Location) -> dict`, gleich aufgebaut wie
`current_weather`:

```python
request_json(FORECAST_URL, {
    "latitude": location.latitude, "longitude": location.longitude,
    "daily": "weather_code,temperature_2m_max,temperature_2m_min",
    "temperature_unit": "celsius", "timezone": "auto", "forecast_days": 2,
})
```

Echte Antwort für Zürich am 26.10.2026 (gekürzt). Index 0 ist heute, Index 1 ist morgen:

```json
{
  "daily_units": {"weather_code": "wmo code", "temperature_2m_max": "°C", "temperature_2m_min": "°C"},
  "daily": {"time": ["2026-10-26", "2026-10-27"], "weather_code": [3, 45],
            "temperature_2m_max": [11.7, 16.8], "temperature_2m_min": [6.8, 7.7]}
}
```

`timezone=auto` ist nötig, damit «morgen» nach Ortszeit des Orts gilt und nicht nach UTC.

### Task 2: Ausgabe (`weathercli/output.py`)

Neue Funktion `format_tomorrow(location: Location, data: dict) -> str`:

| Fall | Ausgabe |
| --- | --- |
| alles vorhanden | `Zürich, Schweiz, morgen: Nebel, 7.7 bis 16.8 °C` |
| Code fehlt oder unbekannt | `Zürich, Schweiz, morgen: Wetterzustand nicht verfügbar, 7.7 bis 16.8 °C` |
| Tiefst- oder Höchstwert fehlt, ist nicht endlich, Einheit nicht `°C`, oder `daily` hat keinen Index 1 | `Zürich, Schweiz, morgen: Vorhersage nicht verfügbar` |

- Den Zustand direkt über `conditions.WMO_CONDITIONS` übersetzen.
  `condition_from_response` liest nur `current` und passt hier nicht.
- Zahlen mit `:g` formatieren wie bei `format_weather`.
- Exit-Code bleibt in allen drei Fällen 0. Es werden keine Werte erfunden (AK 3).

### Task 3: Option `--morgen` (`weathercli/cli.py`)

- `parser.add_argument("--morgen", action="store_true", help="Wetter für morgen anzeigen")`
- Mit `--morgen`: `format_tomorrow(location, tomorrow_forecast(location))`.
  Ohne `--morgen`: unverändert `format_weather(...)` (AK 2).
- Epilog ergänzen: `weather "Zürich" --morgen` (AK 4).
- `weather --morgen` ohne Stadt endet wie bisher mit «Die Stadt fehlt.» und Exit 2.

### Task 4: Tests und Abschluss

- `tests/test_client.py`: Parameter von `tomorrow_forecast` (simulierte Antwort).
- `tests/test_output.py`: die drei Fälle aus der Tabelle oben, dazu Tiefstwert `0`
  und negative Werte.
- `tests/test_weather.py`: mit `--morgen`, ohne `--morgen` unverändert, Hilfe enthält `--morgen`.
- Live prüfen: `"Zürich" --morgen`, `"New York" --morgen`, `"Springfield" --morgen` (Exit 1).
  Ergebnis unten unter «Prüfnachweis» eintragen.
- PR nach `main`. Review durch den anderen Developer (DoD 3) **und** durch eine KI
  (KI-Reviewpunkt). Befunde und Entscheidung ins Portfolio, Abschnitt 7.

## US-07 – Installation und Demo ohne Hilfe

- README kürzen: Abschnitte «Neue Verteilung» und den veralteten Satz «keine Tests
  ausgeführt» entfernen; Schnittstellen-Details dürfen nach `doc/` wandern.
- «Installation» in höchstens fünf Schritten: venv anlegen, `pip install .`,
  `weather "Zürich"`. Auf einer frischen venv genau so durchspielen.
- Echte Ausgaben für `"Zürich"`, `"New York"`, `"Zürich" --morgen` und `--help` einfügen,
  sobald US-06 auf `main` ist.
- Grenzen nennen: ein Ort pro Aufruf, Internet nötig, Daten von Open-Meteo.
- Eduart oder Fidan führt die Schritte aus und bestätigt im Ticket (AK 4).

## US-08 – Kurzer Verbindungsfehler wird wiederholt (nur bei freier Kapazität)

- In `errors.request_json`: Bei `URLError`, `OSError` oder `HTTPException` genau einmal
  wiederholen. Bei `HTTPError` und ungültigem JSON nicht wiederholen. Achtung:
  `HTTPError` ist eine Unterklasse von `URLError` und muss deshalb zuerst abgefangen werden,
  wie heute schon.
- Tests mit simuliertem `urlopen`: erster Versuch Timeout und zweiter OK ergibt Daten;
  beide Timeout ergibt `WeatherError`; HTTP 500 wird genau einmal aufgerufen.

## Pflicht-Tasks

| Task | Fertig, wenn |
| --- | --- |
| Stabilisieren | Alle Tests auf `main` grün; Commit `b4be608` auf `feature/WEA-22-23-wind` übernommen oder Branch gelöscht; Startprüfung (DoD 4) von allen vier im Portfolio; Umlaute im Demo-Terminal geprüft |
| Demo vorbereiten | Fünf Aufrufe festgelegt (`"Zürich"`, `"New York"`, `"Zürich" --morgen`, `"Springfield"`, `--help`); auf dem Demo-Gerät einmal durchgespielt; Screenshot der Ausgaben als Ersatz ohne Internet |
| Präsentation vorbereiten | Gliederung (Vision, Inkrement, Scrum-Erfahrung, KI-Nutzung) und Sprechende festgelegt; einmal mit Zeitmessung geprobt |

## Prüfnachweis

US-06 (WEA-32 bis WEA-35), ausgeführt am 26.10.2026 von Nico auf Windows 11 mit
Python 3.13, Branch `feature/US-06-morgen`. `python -m unittest discover -s tests`:
58 Tests OK (vorher 43, neu 15 für `tomorrow_forecast`, `format_tomorrow`,
`condition_from_code` und `--morgen`).

| Aufruf | Ausgabe | Exit | Kriterium |
| --- | --- | --- | --- |
| `weather "Zürich" --morgen` | `Zürich, Schweiz, morgen: Bewölkt, 8.1 bis 16.4 °C` | 0 | AK 1 |
| `weather "New York" --morgen` | `New York City, Vereinigte Staaten, morgen: Bewölkt, 5.9 bis 14.6 °C` | 0 | AK 1, mehrteiliger Name |
| `weather "Springfield" --morgen` | `Fehler: Der Ort ist mehrdeutig. Bitte eine genauere Ortsangabe eingeben.` | 1 | mehrdeutiger Ort, keine erfundenen Werte |
| `weather "Zürich"` | `Zürich, Schweiz: 9.8 °C, Bewölkt, Wind: 1.4 km/h` | 0 | AK 2, Ausgabe unverändert |
| `weather --help` | nennt `--morgen` und das Beispiel `weather "Zürich" --morgen` | 0 | AK 4 |
| `weather --morgen` ohne Stadt | `Fehler: Die Stadt fehlt.` plus Beispielaufruf | 2 | Eingabefehler bleibt Exit 2 |

Fehlende Vorhersagedaten sind nicht live auslösbar und über Tests abgedeckt
(`Vorhersage nicht verfügbar` und `Wetterzustand nicht verfügbar`, je Exit 0, AK 3).
