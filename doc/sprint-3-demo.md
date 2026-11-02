# Demo Sprint 3 (WEA-42)

Ablauf für die Demo im Sprint Review. Fünf Aufrufe, feste Reihenfolge, jeder
zeigt ein Akzeptanzkriterium einer umgesetzten Story.

**Voraussetzungen**

- `--morgen` (US-06) ist seit PR #16 auf `main`; die Demo braucht den aktuellen Stand.
- Installation nach README auf einer frischen virtuellen Umgebung
  (`python -m venv .venv`, `pip install .`, danach `weather "Zürich"`).
  Am 26.10.2026 so geprüft und ohne Fehler durchgelaufen.
- Terminal auf UTF-8, siehe «Umlaute» unten.

## Ablauf

| # | Aufruf | Zeigt | Erwartete Ausgabe (26.10.2026) | Exit |
| ---: | --- | --- | --- | --- |
| 1 | `weather "Zürich"` | US-01, US-02, US-03: Ort, Temperatur, Zustand, Wind in einem Aufruf | `Zürich, Schweiz: 10.2 °C, Bewölkt, Wind: 0.5 km/h` | 0 |
| 2 | `weather "New York"` | US-04: mehrteiliger Name, aufgelöst auf New York City | `New York City, Vereinigte Staaten: 5.8 °C, Klar, Wind: 8.5 km/h` | 0 |
| 3 | `weather "Zürich" --morgen` | US-06: Zustand und Temperaturbereich für morgen | `Zürich, Schweiz, morgen: Bewölkt, 8 bis 16.4 °C` | 0 |
| 4 | `weather "Springfield"` | Fehlerfall: mehrdeutiger Ort, keine erfundenen Werte | `Fehler: Der Ort ist mehrdeutig. Bitte eine genauere Ortsangabe eingeben.` | 1 |
| 5 | `weather --help` | US-05: Bedienung ohne externe Anleitung, nennt `--morgen` | Hilfetext mit Syntax, Optionen und drei Beispielen | 0 |

Temperatur- und Windwerte ändern sich mit jeder Abfrage; gleich bleiben Format,
Reihenfolge der Angaben und Exit-Code.

## Ersatz ohne Internet

Die Ausgaben aller fünf Aufrufe stehen mitgeschrieben in
[demo-ausgaben.txt](demo-ausgaben.txt) (aufgenommen am 26.10.2026). Fällt im
Review das Internet aus, wird diese Datei gezeigt statt live abgefragt.

Zusätzlich auf dem Demo-Gerät ein Bildschirmfoto der fünf Ausgaben machen und
unter `doc/images/` ablegen; das Mitschrieb-Textfile deckt den Inhalt ab, ein
Bild wirkt in der Präsentation aber schneller.

## Umlaute im Demo-Terminal (gehört zu WEA-41)

Am 26.10.2026 auf Windows 11 geprüft:

- Konsole auf UTF-8 (`chcp 65001` oder `$env:PYTHONIOENCODING = "utf-8"`):
  alle Zeichen korrekt, `Zürich`, `Bewölkt`, `°C`.
- Konsole auf cp1252 (Windows-Standard): `ü`, `ö` und `°` sind in cp1252
  enthalten und erscheinen korrekt. Nur Zeichen, die cp1252 nicht kennt, werden
  zu `?`, zum Beispiel `weather "Łódź"` → `?ód?, Polen: 9 °C, Bewölkt, Wind: 14.4 km/h`,
  Exit 0 statt Abbruch (Fix aus PR #9).

Für die Demo genügt also der Standard; die Demo-Orte Zürich und New York sind
in beiden Fällen lesbar. Trotzdem vorher einmal `weather "Zürich"` im
Demo-Terminal ausführen und hinschauen.

## Durchlauf vom 02.11.2026

Im Auftrag von Eduart mit Claude Code auf Eduarts Laptop ausgeführt, Stand `50f2bd9`,
frische venv. Ob dieser Laptop das Demo-Gerät der Präsentation war, ist hier nicht
festgehalten.

| # | Aufruf | Ausgabe | Exit |
| ---: | --- | --- | --- |
| 1 | `weather "Zürich"` | `Zürich, Schweiz: 5.1 °C, Bewölkt, Wind: 9.7 km/h` | 0 |
| 2 | `weather "New York"` | `New York City, Vereinigte Staaten: 7 °C, Klar, Wind: 8.9 km/h` | 0 |
| 3 | `weather "Zürich" --morgen` | `Zürich, Schweiz, morgen: Bewölkt, 4.6 bis 7.9 °C` | 0 |
| 4 | `weather "Springfield"` | `Fehler: Der Ort ist mehrdeutig. Bitte eine genauere Ortsangabe eingeben.` | 1 |
| 5 | `weather --help` | Hilfetext, beginnt mit `usage: weather "STADT" [--morgen]` | 0 |

## Offen

- Bildschirmfoto der fünf Ausgaben ablegen.
