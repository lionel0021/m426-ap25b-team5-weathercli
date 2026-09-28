# US-02 – Prüfnachweis Wetterzustand

Story WEA-9 mit den Tasks WEA-19 (Code auslesen), WEA-20 (WMO-Codes auf Deutsch)
und WEA-21 (Zustand in der Ausgabe). Umgesetzt von Nico am 28.09.2026.

## Umsetzung

`client.current_weather` fragt `current=temperature_2m,weather_code` in **einem**
Aufruf ab. Temperatur und Zustand stammen damit aus derselben Messung, wie es
Akzeptanzkriterium 2 verlangt. `conditions.condition_from_response` übersetzt den
Code über die Tabelle `WMO_CONDITIONS` ins Deutsche und gibt `None` zurück, wenn
der Code fehlt, keine ganze Zahl ist oder nicht in der Tabelle steht.
`output.format_weather` hängt den Zustand an die bestehende Zeile an.

## Live-Abnahme vom 28.09.2026

Ausgeführt mit `python -m weathercli ...` gegen die echte Open-Meteo-API.
Temperatur und Zustand sind Momentwerte.

| Aufruf | Ausgabe | Exit | Kriterium |
| --- | --- | --- | --- |
| `weather "Zürich"` | `Zürich, Schweiz: 15.4 °C, Klar` | 0 | AK 1, AK 2 |
| `weather "Bern"` | `Bern, Schweiz: 11.6 °C, Klar` | 0 | AK 1, AK 2 |
| `weather "Reykjavik"` | `Reykjavík, Island: 6.7 °C, Leichter Sprühregen` | 0 | AK 1 |
| `weather "New York"` | `New York City, Vereinigte Staaten: 15 °C, Leichter Regen` | 0 | AK 1, AK 2 |
| `weather "Springfield"` | `Fehler: Der Ort ist mehrdeutig. Bitte eine genauere Ortsangabe eingeben.` | 1 | unverändert aus US-01 |
| `weather` | `Fehler: Die Stadt fehlt.` plus Beispielaufruf | 2 | unverändert aus US-01 |

In allen Fällen steht ein ausgeschriebener deutscher Zustand, nie eine blosse
Zahl. Ort und Temperatur bleiben in derselben Zeile sichtbar.

## Fehlender oder unbekannter Zustand (AK 3)

Ein fehlender Code lässt sich live nicht erzwingen, deshalb mit simulierten
Antworten geprüft (`tests/test_conditions.py`, `tests/test_output.py`):

- fehlendes `weather_code`, `null`, Text statt Zahl, `true`, Kommazahl, `NaN`
  und ein unbekannter Code wie 4 oder 123 ergeben je `None`
- die Ausgabe zeigt dann `Zürich, Schweiz: 15.4 °C, Wetterzustand nicht verfügbar`
- die Temperatur bleibt sichtbar, die Anwendung endet ohne Absturz

`python -m unittest discover -s tests`: **40 Tests erfolgreich**.

## Offen

Review durch Lionel und die Startprüfung im Team nach
[Definition of Done](definition-of-done.md), Punkte 3 und 4.
