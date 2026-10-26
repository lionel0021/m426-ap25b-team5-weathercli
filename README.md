# WeatherCLI

WeatherCLI zeigt für einen Ort die aktuelle Temperatur, den Wetterzustand und
den Wind. Mit `--morgen` erscheint die Vorhersage für den nächsten Kalendertag
in der Zeitzone des Orts. Die Wetterdaten kommen von Open-Meteo.

## Installation und erster Aufruf

In einem frischen Klon sind es fünf Schritte:

1. Virtuelle Umgebung anlegen: `python -m venv .venv`
2. Aktivieren: Windows `.venv\Scripts\Activate.ps1`; macOS/Linux `source .venv/bin/activate`.
3. Im Projektordner installieren: `python -m pip install .`
4. Aktuelles Wetter abfragen: `weather "Zürich"`
5. Vorhersage anzeigen: `weather "Zürich" --morgen`

Falls die Shell-Skriptausführung unter Windows die Aktivierung verhindert,
verwende stattdessen `.venv\Scripts\weather.exe` nach Schritt 3. Auf macOS und
Linux liegt der Befehl unter `.venv/bin/weather`.

## Beispiele

Die Beispielausgaben zeigen echte Open-Meteo-Antworten; Werte und Vorhersagen
ändern sich mit der Zeit.

```text
> weather "Zürich"
Zürich, Schweiz: 10.6 °C, Bewölkt, Wind: 1.3 km/h

> weather "New York"
New York City, Vereinigte Staaten: 5.4 °C, Klar, Wind: 8.7 km/h

> weather "Zürich" --morgen
Zürich, Schweiz: Morgen 2026-10-27, Bewölkt, 7.9–16.3 °C, Wind bis 4 km/h

> weather --help
usage: weather "STADT" [--morgen]

Zeigt Temperatur, Wetterzustand und Wind einer Stadt.

Argumente:
  STADT       genau eine Stadt

Optionen:
  -h, --help  Hilfe anzeigen und beenden
  --morgen    Vorhersage fuer morgen anzeigen

Beispiele: weather "Zürich" | weather "New York" | weather "Zürich" --morgen
```

Die Wetterbeispiele wurden am 26.10.2026 live mit Open-Meteo abgerufen. Die
Vorhersage bezieht sich auf den nächsten Kalendertag in der Zeitzone von Zürich.
`weather --help` funktioniert ohne Internetverbindung.

## Grenzen

- Pro Aufruf wird ein Ort abgefragt.
- Für Wetterdaten ist eine Internetverbindung nötig.
- Wetter- und Geocoding-Daten stammen von Open-Meteo.
- Fehlen optionale Wind- oder Wetterzustandsdaten, bleiben die übrigen Werte
  sichtbar und der fehlende Wert wird gekennzeichnet.

## Entwicklung

Voraussetzung ist Python 3.10 oder neuer. Es werden keine externen
Laufzeitpakete benötigt.

Tests:

```powershell
python -m unittest discover -s tests -v
```
