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

## Merge in main am 28.09.2026 (Nico)

`feature/WEA-22-23-wind` war von einem Stand vor US-02 abgezweigt und liess sich
nicht ohne Konflikt mergen: `client.current_weather` und `output.format_weather`
waren in beiden Zweigen geändert. Aufgelöst, ohne eine der Stories zu verlieren:

- Eine Abfrage mit `current=temperature_2m,weather_code,wind_speed_10m`
  (`temperature_unit=celsius`, `wind_speed_unit=kmh`) trägt alle drei Werte.
- `output.format_weather` zeigt Temperatur, Wetterzustand und Wind:
  `Zürich, Schweiz: 18.3 °C, Klar, Wind: 4.6 km/h`.
- Die Windprüfung stammt unverändert aus dem Feature-Branch und liegt jetzt in
  `output.wind_from_response`.

## Prüfstand

Der Feature-Branch enthielt keine Tests; das Ausgabeformat änderte sich, die
bestehenden Tests schlugen deshalb fehl. Beim Merge ergänzt und angepasst:

- `0 km/h` wird als Wert ausgegeben, nicht als fehlend (WEA-23)
- fehlender Windwert, Text, `true`, `NaN` sowie eine andere Einheit als km/h
  ergeben `Wind nicht verfügbar`; Ort, Temperatur und Zustand bleiben sichtbar
- CLI- und Ausgabetests erwarten das kombinierte Format

`python -m unittest discover -s tests`: **43 Tests erfolgreich**.

Live am 28.09.2026: `Zürich, Schweiz: 18.3 °C, Klar, Wind: 4.6 km/h`,
`New York City, Vereinigte Staaten: 14.9 °C, Leichter Sprühregen, Wind: 19.8 km/h`,
`Reykjavík, Island: 6.9 °C, Sprühregen, Wind: 8.6 km/h`. Fehlerfälle unverändert:
mehrdeutiger Ort und nicht erreichbarer Dienst enden mit Exit-Code 1.

Review durch Lionel und die Team-Abnahme nach DoD stehen noch aus.
