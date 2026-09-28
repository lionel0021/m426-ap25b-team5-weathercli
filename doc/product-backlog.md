# Product Backlog – WeatherCLI

Stand: 28.09.2026, nach Abschluss der Umsetzung von Sprint 1. Quelle:
[Story Map](images/StoryBoard.png), Sprintplanung und aktuelles YouTrack-Board.

## Aktuelle Reihenfolge und Planung

| Rang | Story | Priorität | Story Points | Sprint | Board-Status |
| ---: | --- | --- | ---: | --- | --- |
| 1 | US-01 – Aktuelle Temperatur für eine Stadt | Must | 8 | Sprint 1 | Erledigt |
| 2 | US-04 – Mehrteilige Stadtnamen | Should | 3 | Sprint 1 | Erledigt |
| 3 | US-05 – Bedienung ohne externe Anleitung | Should | 2 | Sprint 1 | Erledigt |
| 4 | US-02 – Aktuellen Wetterzustand erkennen | Must | 3 | Sprint 2 | Offen |
| 5 | US-03 – Aktuelle Windgeschwindigkeit sehen | Should | 2 | Sprint 2 | Offen |

Sprint 1 umfasst US-01, US-04 und US-05. Die zugehörigen Tasks WEA-13 bis
WEA-18 sowie WEA-24 bis WEA-28 stehen im Board auf «Erledigt». Die Umsetzung
ist auf `main`; der aktuelle Testnachweis und noch offene DoD-Prüfungen stehen
im [Sprintplan](sprint-1.md).

Für Sprint 2 ist US-02 trotz tieferer ursprünglicher Reihenfolge vor US-03
einzuplanen, da sie als Must priorisiert ist. WEA-19 bis WEA-21 gehören zu
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

**Priorität:** 4 · Must · **Status:** Offen · **Schätzung:** 3 Story Points · **Sprint:** 2

Als Person, die einen kurzen Weg im Freien plant, möchte ich zusätzlich zur Temperatur den aktuellen Wetterzustand lesen, damit ich entscheiden kann, ob ich einen Regenschutz mitnehme.

### Akzeptanzkriterien

1. Bei erfolgreicher Abfrage ergänzt `weather "Zürich"` die Ausgabe um einen ausgeschriebenen deutschen Wetterzustand, beispielsweise «Regen» oder «Bewölkt»; ein numerischer Wettercode allein genügt nicht.
2. Ort und Temperatur bleiben in derselben Ausgabe sichtbar; der Wetterzustand gehört zum selben abgefragten Ort und aktuellen Datensatz.
3. Fehlt der Wetterzustand oder ist der gelieferte Code unbekannt, erscheint «Wetterzustand nicht verfügbar»; vorhandene Temperaturdaten bleiben sichtbar und die Anwendung stürzt nicht ab.

**Umfang:** Aktueller Zustand, keine Regenwahrscheinlichkeit oder Prognose. Baut auf US-01 auf und ergänzt Datenabfrage, Zuordnung und sichtbare Ausgabe.

## US-03 – Aktuelle Windgeschwindigkeit sehen

**Priorität:** 5 · Should · **Status:** Offen · **Schätzung:** 2 Story Points · **Sprint:** 2

Als Person, die mit dem Velo unterwegs ist, möchte ich die aktuelle Windgeschwindigkeit am abgefragten Ort sehen, damit ich vor der Abfahrt die Bedingungen einschätzen kann.

### Akzeptanzkriterien

1. Bei verfügbaren Winddaten zeigt `weather "Zürich"` zusätzlich eine beschriftete Windgeschwindigkeit mit der Einheit km/h für denselben Ort.
2. Ein Windwert von 0 wird als `0 km/h` angezeigt und nicht als fehlender Wert behandelt.
3. Fehlen verwertbare Winddaten, erscheint «Wind nicht verfügbar»; die übrigen verfügbaren Wetterinformationen bleiben lesbar.

**Umfang:** Ein aktueller Zahlenwert mit Einheit; keine Windrichtung, Böen oder Warnstufen. Baut auf US-01 auf; US-02 ist keine Voraussetzung.

## US-04 – Wetter für eine Stadt mit mehrteiligem Namen abrufen

**Priorität:** 2 · Should · **Status:** Erledigt · **Schätzung:** 3 Story Points · **Sprint:** 1

Als reisende Terminalnutzerin möchte ich Wetter für eine Stadt mit Leerzeichen im Namen abrufen, damit ich auch für solche Reiseziele passende Wetterinformationen erhalte.

### Akzeptanzkriterien

1. `weather "New York"` verarbeitet den gesamten Namen als einen Ort und zeigt bei erfolgreicher eindeutiger Ortssuche das aktuelle Wetter für New York mit Land und Temperatur.
2. Führende und nachfolgende Leerzeichen innerhalb des Arguments werden ignoriert: `weather "  New York  "` fragt denselben Ort wie `weather "New York"` ab.
3. Ein Argument, das nur Leerzeichen enthält, zeigt einen Hinweis auf die fehlende Stadt und einen Beispielaufruf; der Exit-Code ist ungleich 0.
4. Mehrere unquotierte Ortsargumente wie `weather New York` werden mit einem Hinweis auf die nötigen Anführungszeichen und einem Exit-Code ungleich 0 abgewiesen; es wird nicht stillschweigend nur «New» abgefragt.

**Umfang:** Ein mehrteiliger Ortsname, keine Abfrage mehrerer Städte. Baut auf US-01 auf und deckt Eingabe, Ortssuche und sichtbares Ergebnis ab.

## US-05 – Wetterbefehl ohne externe Anleitung bedienen

**Priorität:** 3 · Should · **Status:** Erledigt · **Schätzung:** 2 Story Points · **Sprint:** 1

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

### Vor dem Sprint-2-Planning prüfen

- US-02 und US-03 aus Sprint 1 entfernen und dem neuen Sprint 2 zuordnen.
- Sprint-2-Zeitraum und Teamkapazität festlegen.
- Prüfen, ob die bestehenden Schätzungen von 3 und 2 Story Points weiterhin
  zum bekannten Aufwand passen.
- Verantwortliche und Abnahmetermine für WEA-19 bis WEA-23 bestätigen.
