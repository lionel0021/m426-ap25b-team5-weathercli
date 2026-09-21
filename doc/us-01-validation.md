# US-01 – aktueller Prüfnachweis

Der aktuelle Plan steht in [sprint-1.md](sprint-1.md). Sprint 1 enthält US-01,
US-04 und US-05; Wind und Wetterzustand gehören in Sprint 2.

US-01 / WEA-8 bleibt in Bearbeitung:

- Lionel: WEA-13, WEA-14, WEA-17 und neu WEA-18.
- Nico (nico.schult): WEA-15 und WEA-16, zur Prüfung.

Lionels Implementierung umfasst Projektstruktur, CLI, Temperaturausgabe und
getestete Fehlerbehandlung. `errors.py` stellt die Helfer bereit, die Nico in
seine API-Funktionen integriert. Die gesamte Testsuite enthält 33 erfolgreiche
Tests mit simulierten Daten. Frühere Live-Ergebnisse des verworfenen
Gesamtentwurfs gelten nicht als Nachweis für den aktuellen Stand.

## Live-Abnahme vom 21.09.2026 (Nico)

Ausgeführt mit `python -m weathercli ...` gegen die echte Open-Meteo-API.
Temperaturen sind Momentwerte.

| Aufruf | Ausgabe | Exit | Kriterium |
| --- | --- | --- | --- |
| `weather "Zürich"` | `Zürich, Schweiz: 17.2 °C` | 0 | US-01 AK 1 |
| `weather "Bern"` | `Bern, Schweiz: 17.5 °C` | 0 | US-01 AK 1 |
| `weather "Frankfurt"` | `Frankfurt am Main, Deutschland: 15.5 °C` | 0 | US-01 AK 1 |
| `weather` | `Fehler: Die Stadt fehlt.` und Beispielaufruf | 2 | US-01 AK 2 |
| `weather "Springfield"` | `Fehler: Der Ort ist mehrdeutig. Bitte eine genauere Ortsangabe eingeben.` | 1 | US-01 AK 3 |
| `weather "xyzabcqq"` | `Fehler: Kein Ort gefunden. Bitte eine genauere Ortsangabe eingeben.` | 1 | US-01 AK 3 |
| `weather "Zürich"` ohne Verbindung (Proxy auf geschlossenen Port) | `Fehler: Wetterdienst nicht erreichbar. Bitte später erneut versuchen.` | 1 | US-01 AK 4 |
| `weather "New York"` | `New York City, Vereinigte Staaten: 16.6 °C` | 0 | US-04 AK 1 |
| `weather "  New York  "` | `New York City, Vereinigte Staaten: 16.6 °C` | 0 | US-04 AK 2 |
| `weather "   "` | `Fehler: Die Stadt fehlt.` und Beispielaufruf | 2 | US-04 AK 3 |
| `weather New York` | `Fehler: Genau eine Stadt angeben; mehrteilige Namen in Anführungszeichen setzen.` | 2 | US-04 AK 4 |

Fehlende Temperatur (US-01 AK 4) lässt sich live nicht erzwingen und ist in
`tests/test_client.py` mit simulierten Antworten abgedeckt.

Review, Integration in den gemeinsamen Hauptbranch und Startprüfung aller
Teammitglieder stehen noch aus. Siehe [Definition of Done](definition-of-done.md).
