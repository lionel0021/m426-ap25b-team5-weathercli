# Demo Sprint 3 (WEA-42)

Ablauf für die Demo im Sprint Review. Fünf Aufrufe, feste Reihenfolge, jeder
zeigt ein Akzeptanzkriterium einer umgesetzten Story.

**Voraussetzungen**

- `--morgen` (US-06) ist auf `main`, also PR #16 gemergt. Vorher fehlt Aufruf 3:
  in der frischen venv von `main` antwortet `weather "Zürich" --morgen` mit
  `Fehler: unrecognized arguments: --morgen` und Exit 2.
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

## Offen

- Einmal komplett auf dem Demo-Gerät durchspielen (Nico, vor dem Review).
- Bildschirmfoto der fünf Ausgaben ablegen.
