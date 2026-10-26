# Product Backlog – WeatherCLI

Stand: 28.09.2026, nach Abschluss der Umsetzung von Sprint 1. Quelle:
[Story Map](images/StoryBoard.png), Sprintplanung und aktuelles YouTrack-Board.

## Aktuelle Reihenfolge und Planung

| Rang | Story | Priorität | Story Points | Sprint | Board-Status |
| ---: | --- | --- | ---: | --- | --- |
| 1 | US-01 – Aktuelle Temperatur für eine Stadt | Must | 8 | Sprint 1 | Erledigt |
| 2 | US-02 – Aktuellen Wetterzustand erkennen | Must | 3 | Sprint 2 | Offen |
| 3 | US-04 – Mehrteilige Stadtnamen | Should | 3 | Sprint 1 | Erledigt |
| 4 | US-05 – Bedienung ohne externe Anleitung | Should | 2 | Sprint 1 | Erledigt |
| 5 | US-03 – Aktuelle Windgeschwindigkeit sehen | Should | 2 | Sprint 2 | Offen |

Sprint 1 umfasst US-01, US-04 und US-05. Die zugehörigen Tasks WEA-13 bis
WEA-18 sowie WEA-24 bis WEA-28 stehen im Board auf «Erledigt». Die Umsetzung
ist auf `main`; der aktuelle Testnachweis und noch offene DoD-Prüfungen stehen
im [Sprintplan](sprint-1.md).

Die Reihenfolge folgt MoSCoW: zuerst die beiden Must-Stories US-01 und US-02,
danach die Should-Stories. In Sprint 2 kommt US-02 deshalb vor US-03. WEA-19 bis WEA-21 gehören zu
US-02, WEA-22 und WEA-23 zu US-03 und sind aktuell offen. US-02 und US-03
sollen aus Sprint 1 entfernt werden, damit der Sprint-1-Burndown den wirklich
vereinbarten Umfang zeigt. Termine und Kapazität für Sprint 2 werden im
nächsten Planning bestätigt.

**Aufgabenverwaltung:** [WeatherCLI in YouTrack](https://weathercli.youtrack.cloud/).
Die fünf Stories und ihre Tasks sind dort erfasst. Der oben dokumentierte
Status wurde am 28.09.2026 mit dem aktuellen Sprint- und Aufgabenboard
abgeglichen.

## Vereinbarungen für die fünf Stories

Vorgeschlagene Bedienung: `weather "Zürich"` für aktuelles Wetter, `weather --help` für Hilfe. Ein Aufruf verarbeitet genau eine Stadt und beendet sich danach. Fehlgeschlagene Abfragen zeigen eine verständliche Meldung und einen Exit-Code ungleich 0. Vorhersage, Verlauf und Einstellungen bleiben ausserhalb dieser fünf Stories. Befehlsname und Wetterdienst sind vor der Schätzung im Team zu bestätigen.

## US-01 – Aktuelle Temperatur für eine Stadt abrufen

**Priorität:** 1 · Must · **Status:** Erledigt · **Schätzung:** 8 Story Points · **Sprint:** 1

Als Person, die im Terminal arbeitet, möchte ich die aktuelle Temperatur einer eingegebenen Stadt sehen, damit ich meine Kleidung für den nächsten Weg wählen kann, ohne eine weitere Anwendung zu öffnen.

### Akzeptanzkriterien

1. Bei einer bekannten, eindeutig gefundenen Stadt und erreichbarem Wetterdienst zeigt `weather "Zürich"` den aufgelösten Stadtnamen, das Land und die aktuelle Temperatur mit der Einheit °C; der Exit-Code ist 0.
2. Bei fehlender Stadt zeigt `weather` einen Hinweis auf das fehlende Argument sowie einen gültigen Beispielaufruf; der Exit-Code ist ungleich 0.
3. Liefert die Ortssuche keinen Treffer oder mehrere mögliche Orte, zeigt die Anwendung eine verständliche Meldung und fordert eine genauere Ortsangabe; sie gibt keine Temperatur für einen ungeklärten Ort aus.
4. Bei nicht erreichbarem Wetterdienst oder fehlender Temperatur erscheint eine Fehlermeldung und ein Exit-Code ungleich 0; es werden keine erfundenen Wetterwerte ausgegeben.

**Umfang:** Ein Ort, aktuelle Temperatur, Textausgabe. Keine interaktive Ortsauswahl. Dies ist der erste vollständige Weg von der Eingabe über die Datenabfrage bis zur sichtbaren Ausgabe.

## US-02 – Aktuellen Wetterzustand erkennen

**Priorität:** 2 · Must · **Status:** Sprint 2 ausgewählt · **Schätzung:** 3 Story Points · **Sprint:** 2

Als Person, die einen kurzen Weg im Freien plant, möchte ich zusätzlich zur Temperatur den aktuellen Wetterzustand lesen, damit ich entscheiden kann, ob ich einen Regenschutz mitnehme.

### Akzeptanzkriterien

1. Bei erfolgreicher Abfrage ergänzt `weather "Zürich"` die Ausgabe um einen ausgeschriebenen deutschen Wetterzustand, beispielsweise «Regen» oder «Bewölkt»; ein numerischer Wettercode allein genügt nicht.
2. Ort und Temperatur bleiben in derselben Ausgabe sichtbar; der Wetterzustand gehört zum selben abgefragten Ort und aktuellen Datensatz.
3. Fehlt der Wetterzustand oder ist der gelieferte Code unbekannt, erscheint «Wetterzustand nicht verfügbar»; vorhandene Temperaturdaten bleiben sichtbar und die Anwendung stürzt nicht ab.

**Umfang:** Aktueller Zustand, keine Regenwahrscheinlichkeit oder Prognose. Baut auf US-01 auf und ergänzt Datenabfrage, Zuordnung und sichtbare Ausgabe.

## US-03 – Aktuelle Windgeschwindigkeit sehen

**Priorität:** 5 · Should · **Status:** Sprint 2 ausgewählt · **Schätzung:** 2 Story Points · **Sprint:** 2

Als Person, die mit dem Velo unterwegs ist, möchte ich die aktuelle Windgeschwindigkeit am abgefragten Ort sehen, damit ich vor der Abfahrt die Bedingungen einschätzen kann.

### Akzeptanzkriterien

1. Bei verfügbaren Winddaten zeigt `weather "Zürich"` zusätzlich eine beschriftete Windgeschwindigkeit mit der Einheit km/h für denselben Ort.
2. Ein Windwert von 0 wird als `0 km/h` angezeigt und nicht als fehlender Wert behandelt.
3. Fehlen verwertbare Winddaten, erscheint «Wind nicht verfügbar»; die übrigen verfügbaren Wetterinformationen bleiben lesbar.

**Umfang:** Ein aktueller Zahlenwert mit Einheit; keine Windrichtung, Böen oder Warnstufen. Baut auf US-01 auf; US-02 ist keine Voraussetzung.

## US-04 – Wetter für eine Stadt mit mehrteiligem Namen abrufen

**Priorität:** 3 · Should · **Status:** Erledigt · **Schätzung:** 3 Story Points · **Sprint:** 1

Als reisende Terminalnutzerin möchte ich Wetter für eine Stadt mit Leerzeichen im Namen abrufen, damit ich auch für solche Reiseziele passende Wetterinformationen erhalte.

### Akzeptanzkriterien

1. `weather "New York"` verarbeitet den gesamten Namen als einen Ort und zeigt bei erfolgreicher eindeutiger Ortssuche das aktuelle Wetter für New York mit Land und Temperatur.
2. Führende und nachfolgende Leerzeichen innerhalb des Arguments werden ignoriert: `weather "  New York  "` fragt denselben Ort wie `weather "New York"` ab.
3. Ein Argument, das nur Leerzeichen enthält, zeigt einen Hinweis auf die fehlende Stadt und einen Beispielaufruf; der Exit-Code ist ungleich 0.
4. Mehrere unquotierte Ortsargumente wie `weather New York` werden mit einem Hinweis auf die nötigen Anführungszeichen und einem Exit-Code ungleich 0 abgewiesen; es wird nicht stillschweigend nur «New» abgefragt.

**Umfang:** Ein mehrteiliger Ortsname, keine Abfrage mehrerer Städte. Baut auf US-01 auf und deckt Eingabe, Ortssuche und sichtbares Ergebnis ab.

## US-05 – Wetterbefehl ohne externe Anleitung bedienen

**Priorität:** 4 · Should · **Status:** Erledigt · **Schätzung:** 2 Story Points · **Sprint:** 1

Als neue Terminalnutzerin möchte ich die gültige Syntax und konkrete Beispiele direkt im Terminal sehen, damit ich meine erste Wetterabfrage ohne externe Anleitung ausführen kann.

### Akzeptanzkriterien

1. `weather --help` zeigt den Zweck der Anwendung, die Syntax `weather "STADT"` und je ein Beispiel mit einem einteiligen und einem mehrteiligen Stadtnamen; der Exit-Code ist 0.
2. Die Hilfe lässt sich auch ohne Internetverbindung anzeigen und benötigt keine Wetterabfrage.
3. Eine unbekannte Option wie `weather --unbekannt` zeigt die betreffende Option, einen Hinweis auf `weather --help` und einen Exit-Code ungleich 0.

**Umfang:** Eine Hilfeseite und Rückmeldung zu unbekannten Optionen; keine interaktive Befehlsshell. Eigenständiger sichtbarer Nutzen ohne Abhängigkeit vom Wetterdienst.

## Weitere Einträge – nach Sprint 2 zu verfeinern

Diese Themen aus der Story Map sind noch nicht schätzbereit und ausdrücklich
keine ausgewählten Sprint-2-Stories.

| Reihenfolge | Thema | MoSCoW | Nächster Zuschnitt |
| --- | --- | --- | --- |
| 6 | Wettervorhersage | Should | Einen konkreten Zeitraum und sichtbare Werte festlegen |
| 7 | Mehrere Städte vergleichen | Could | Zwei Orte in einem Aufruf vergleichen |
| 8 | Letzte Städte vorschlagen | Could | Einen zuletzt verwendeten Ort erneut abfragen |
| 9 | Weitere Wetterdaten / Details | Could | Einen zusätzlichen Wert mit konkretem Nutzen auswählen |
| 10 | Verlauf / Befehlsverlauf | Could | Wetterverlauf und Befehlshistorie zuerst unterscheiden |
| 11 | Einstellungen speichern | Could | Eine konkrete Benutzereinstellung wählen |
| 12 | Erneute Anfrage ermöglichen | Could | Nutzeraktion für einen gezielten Wiederholungsversuch klären |

### Umgang mit der bisherigen Story Map

«Stadt eingeben», «Wetter laden» und «Wetter anzeigen» bilden gemeinsam US-01. Sie werden nicht als technische Teil-Stories geplant. Ungültige Städte, fehlende Eingaben und Verbindungsfehler sind prüfbare Fehlerfälle der betreffenden Stories. Ein separater Beenden-Befehl entfällt beim vorgeschlagenen Einmalaufruf. Technische Aufgaben wie CLI-Verarbeitung, API-Anbindung und Ausgabeformatierung werden im Planning unter den jeweiligen Stories erfasst.

### Refinement für Sprint 2 (28.09.2026, PO)

- US-02 und US-03 sind für Sprint 2 ausgewählt; Schätzungen von 3 und 2 Story
  Points bleiben bestehen. Beide Stories sind kleiner als zwei Modultage und
  müssen nicht weiter gesplittet werden.
- US-02: Open-Meteo liefert den Zustand als WMO-Wettercode (`current=weather_code`).
  Die Übersetzung in deutschen Text (z. B. 0 → «Klar», 61 → «Regen») gehört zur
  Story; unbekannte Codes ergeben «Wetterzustand nicht verfügbar».
- US-03: Wind über `current=wind_speed_10m` mit `wind_speed_unit=kmh`; ein Wert
  von 0 ist gültig und wird als `0 km/h` angezeigt.
- Wetterzustand, Wind und Temperatur kommen aus demselben Forecast-Aufruf, damit
  alle Werte zum selben Ort und Zeitpunkt gehören.
- Offen im Board: US-02 und US-03 aus Sprint 1 entfernen und Sprint 2 zuordnen;
  Retro-Massnahme aus Sprint 1 als Eintrag im Sprint Backlog anlegen.


## Sprint 3 – Vorbereitung (Stand 19.10.2026, PO)

**Sprintziel (Vorschlag):** Das Produkt ist präsentierbar. Eine Person installiert
WeatherCLI mit wenigen Befehlen, fragt `weather "Zürich"` ab, sieht die Prognose für
morgen und bekommt bei einem kurzen Verbindungsproblem keinen unnötigen Fehler.

**Story Points:** bewusst leer. Die schätzt das Team im Planning Poker (Tag 8);
jede Story muss in einem Modultag machbar sein, sonst wird sie vor dem Sprint
gesplittet. Sprint 3 hat nur einen Modultag, deshalb zuerst die Stories 1 und 2,
Story 3 nur bei freier Kapazität.

| Rang | Story | Priorität | Story Points | Begründung |
| ---: | --- | --- | ---: | --- |
| 1 | US-06 – Wetter für morgen sehen | Should | offen | Grösster fehlender Funktionsbereich der Story Map (Rang 6, Vorhersage), auf einen Tag geschnitten |
| 2 | US-07 – Installation und Demo ohne Hilfe | Should | offen | Präsentierbarkeit: Das Produkt muss sich an Tag 8 vorführen lassen |
| 3 | US-08 – Kurzer Verbindungsfehler wird wiederholt | Could | offen | Story Map Rang 12, erhöht die Robustheit der Demo |

Die Wettervorhersage über mehrere Tage ist bewusst nicht in US-06: Sie ist zu
gross für einen Modultag und bleibt als Folgestory im Backlog.

### US-06 – Wetter für morgen sehen

Als Person, die den nächsten Tag plant, möchte ich mit `weather "Zürich" --morgen`
Wetterzustand und Temperaturbereich für morgen sehen, damit ich Kleidung und Weg
im Voraus wählen kann.

**Akzeptanzkriterien**

1. `weather "Zürich" --morgen` zeigt Ort, Land, Wetterzustand auf Deutsch sowie
   Tiefst- und Höchsttemperatur in °C für den morgigen Tag; der Exit-Code ist 0.
2. Ohne `--morgen` bleibt die Ausgabe von `weather "Zürich"` unverändert (aktuelle
   Temperatur, Zustand, Wind).
3. Fehlen die Vorhersagedaten oder ist der Wettercode unbekannt, erscheint «Vorhersage nicht
   verfügbar» beziehungsweise «Wetterzustand nicht verfügbar»; die Anwendung stürzt nicht ab
   und erfindet keine Werte.
4. `weather --help` nennt die Option `--morgen` mit einem Beispiel.

**Umfang:** Nur der morgige Tag, ein Ort. Keine Mehrtagesvorhersage, keine Stundenwerte.
**Technischer Hinweis:** Open-Meteo `daily=weather_code,temperature_2m_max,temperature_2m_min`;
die Wettercode-Übersetzung aus `weathercli/conditions.py` wird wiederverwendet.

### US-07 – Installation und Demo ohne Hilfe

Als neue Person im Team möchte ich WeatherCLI nach der README installieren und die
Beispielabfragen ausführen können, damit ich das Produkt ohne Rückfrage ausprobieren kann.

**Akzeptanzkriterien**

1. Die README beschreibt in höchstens fünf Schritten Installation (`pip install .`) und den
   ersten Aufruf `weather "Zürich"`; auf einer frischen virtuellen Umgebung funktionieren
   die Schritte genau so.
2. Die README zeigt je ein Beispiel mit einteiligem Namen, mehrteiligem Namen, `--morgen`
   und `--help` mit der echten Ausgabe.
3. Die README nennt bekannte Grenzen (nur ein Ort pro Aufruf, Internet nötig, Open-Meteo als
   Datenquelle).
4. Eine Person aus dem Team, die den Code nicht geschrieben hat, führt die Schritte aus und
   bestätigt es im Ticket.

**Umfang:** Dokumentation und Prüfung, kein neuer Code ausser Korrekturen, die beim Prüfen auffallen.

### US-08 – Kurzer Verbindungsfehler wird wiederholt

Als Person mit instabilem WLAN möchte ich, dass `weather "Zürich"` bei einem kurzen
Verbindungsproblem automatisch noch einmal versucht wird, damit ich nicht selbst neu starten muss.

**Akzeptanzkriterien**

1. Scheitert die erste Abfrage mit Timeout oder DNS-Fehler und die zweite gelingt, zeigt die
   Anwendung das normale Wetter; der Exit-Code ist 0.
2. Scheitern beide Versuche, erscheint die bisherige verständliche Fehlermeldung mit Exit-Code
   ungleich 0; es gibt höchstens einen zweiten Versuch.
3. Fehler, die ein Wiederholen nicht lösen kann (unbekannter Ort, ungültige Antwort), werden
   nicht wiederholt.

**Umfang:** Ein automatischer Wiederholversuch, keine Einstellung, kein Dialog.

### Offen vor dem Planning (Tag 8)

- Planning Poker für US-06 bis US-08 im Team durchführen und die Story Points oben eintragen.
- Issues in YouTrack anlegen, bevor jemand Code schreibt (Retro-Massnahme Sprint 0), und die
  Tasks im Planning gemeinsam aus den Kriterien ableiten.
- Ist US-06 grösser als ein Modultag, vorher splitten (zum Beispiel Zustand zuerst, Temperaturbereich danach).
