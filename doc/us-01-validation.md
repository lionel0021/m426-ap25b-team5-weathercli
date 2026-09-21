# US-01 – aktueller Prüfnachweis

Der aktuelle Plan steht in [sprint-1.md](sprint-1.md). Sprint 1 enthält US-01,
US-04 und US-05; Wind und Wetterzustand gehören in Sprint 2.

US-01 / WEA-8 bleibt in Bearbeitung:

- Lionel: WEA-13, WEA-14, WEA-17 und neu WEA-18.
- Nico (nico.schult): WEA-15 und WEA-16, API-Integration noch offen.

Lionels Implementierung umfasst Projektstruktur, CLI, Temperaturausgabe und
getestete Fehlerbehandlung. `errors.py` stellt die Helfer bereit, die Nico in
seine API-Funktionen integriert. Die gesamte Testsuite enthält 20 erfolgreiche
Tests mit simulierten Daten; die vollständige Live-Temperaturabfrage ist noch
nicht abgenommen. Frühere Live-Ergebnisse des verworfenen Gesamtentwurfs gelten
nicht als Nachweis für den aktuellen Stand.

Review, Integration in den gemeinsamen Hauptbranch und Startprüfung aller
Teammitglieder stehen noch aus. Siehe [Definition of Done](definition-of-done.md).
