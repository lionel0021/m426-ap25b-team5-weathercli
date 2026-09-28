# Sprint 2 – Windgeschwindigkeit (US-03)

## Umfang

Lionel bearbeitet WEA-22 und WEA-23 für US-03: `wind_speed_10m` aus derselben
Open-Meteo-Antwort wie die Temperatur lesen, in km/h ausgeben und den Wert
`0` als gültige Windgeschwindigkeit behandeln.

## Umsetzung auf `feature/WEA-22-23-wind`

- Die Forecast-Abfrage fordert `temperature_2m` und `wind_speed_10m` gemeinsam
  mit Celsius- und km/h-Einheiten an.
- Temperatur bleibt der erforderliche Messwert. Ein fehlender, nicht endlicher
  oder nicht als km/h ausgewiesener Windwert lässt die Temperaturausgabe
  bestehen und wird als `Wind nicht verfügbar` angezeigt.
- Ein Windwert von `0 km/h` wird regulär formatiert.
- Die Wetterausgabe verwendet Werte aus derselben API-Antwort.

## Prüfstand

In diesem Arbeitsgang wurden keine Tests ausgeführt. Der Sprint-1-Nachweis
deckt die Windänderung nicht ab. Review und Team-Abnahme stehen noch aus.
