# Product Backlog – WeatherCLI

Stand: Auftrag 4.1, Sprint 0. Quelle: [Story Map](../doc/StoryBoard.png).

Die folgenden fünf Einträge sind für das Refinement und anschliessende Sprint-1-Planning vorbereitet. Die Reihenfolge ist ein Vorschlag nach MoSCoW und Nutzwert: zuerst eine vollständige Wetterabfrage, danach zusätzliche Informationen und Bedienhilfe. Schätzung, Kapazitätsabgleich und Zuteilung erfolgen im Planning. Der Umfang jeder Story ist auf höchstens zwei Modultage ausgelegt; das Team prüft dies bei der Schätzung.

**Aufgabenverwaltung:** [WeatherCLI in YouTrack](https://weathercli.youtrack.cloud/). Gemäss Rückmeldung von Lionel am 07.09.2026 sind die fünf Stories dort erfasst. Eine unabhängige Prüfung der Board-Einträge fand nicht statt. Im Repository ist wie gewünscht nur der YouTrack-Link hinterlegt.

## Vereinbarungen für die fünf Stories

Vorgeschlagene Bedienung: `weather "Zürich"` für aktuelles Wetter, `weather --help` für Hilfe. Ein Aufruf verarbeitet genau eine Stadt und beendet sich danach. Fehlgeschlagene Abfragen zeigen eine verständliche Meldung und einen Exit-Code ungleich 0. Vorhersage, Verlauf und Einstellungen bleiben ausserhalb dieser fünf Stories. Befehlsname und Wetterdienst sind vor der Schätzung im Team zu bestätigen.

## US-01 – Aktuelle Temperatur für eine Stadt abrufen

**Priorität:** 1 · Must · **Status:** Für Refinement vorbereitet · **Schätzung:** offen

Als Person, die im Terminal arbeitet, möchte ich die aktuelle Temperatur einer eingegebenen Stadt sehen, damit ich meine Kleidung für den nächsten Weg wählen kann, ohne eine weitere Anwendung zu öffnen.

### Akzeptanzkriterien

1. Bei einer bekannten, eindeutig gefundenen Stadt und erreichbarem Wetterdienst zeigt `weather "Zürich"` den aufgelösten Stadtnamen, das Land und die aktuelle Temperatur mit der Einheit °C; der Exit-Code ist 0.
2. Bei fehlender Stadt zeigt `weather` einen Hinweis auf das fehlende Argument sowie einen gültigen Beispielaufruf; der Exit-Code ist ungleich 0.
3. Liefert die Ortssuche keinen Treffer oder mehrere mögliche Orte, zeigt die Anwendung eine verständliche Meldung und fordert eine genauere Ortsangabe; sie gibt keine Temperatur für einen ungeklärten Ort aus.
4. Bei nicht erreichbarem Wetterdienst oder fehlender Temperatur erscheint eine Fehlermeldung und ein Exit-Code ungleich 0; es werden keine erfundenen Wetterwerte ausgegeben.

**Umfang:** Ein Ort, aktuelle Temperatur, Textausgabe. Keine interaktive Ortsauswahl. Dies ist der erste vollständige Weg von der Eingabe über die Datenabfrage bis zur sichtbaren Ausgabe.

## US-02 – Aktuellen Wetterzustand erkennen

**Priorität:** 2 · Must · **Status:** Für Refinement vorbereitet · **Schätzung:** offen

Als Person, die einen kurzen Weg im Freien plant, möchte ich zusätzlich zur Temperatur den aktuellen Wetterzustand lesen, damit ich entscheiden kann, ob ich einen Regenschutz mitnehme.

### Akzeptanzkriterien

1. Bei erfolgreicher Abfrage ergänzt `weather "Zürich"` die Ausgabe um einen ausgeschriebenen deutschen Wetterzustand, beispielsweise «Regen» oder «Bewölkt»; ein numerischer Wettercode allein genügt nicht.
2. Ort und Temperatur bleiben in derselben Ausgabe sichtbar; der Wetterzustand gehört zum selben abgefragten Ort und aktuellen Datensatz.
3. Fehlt der Wetterzustand oder ist der gelieferte Code unbekannt, erscheint «Wetterzustand nicht verfügbar»; vorhandene Temperaturdaten bleiben sichtbar und die Anwendung stürzt nicht ab.

**Umfang:** Aktueller Zustand, keine Regenwahrscheinlichkeit oder Prognose. Baut auf US-01 auf und ergänzt Datenabfrage, Zuordnung und sichtbare Ausgabe.

## US-03 – Aktuelle Windgeschwindigkeit sehen

**Priorität:** 3 · Should · **Status:** Für Refinement vorbereitet · **Schätzung:** offen

Als Person, die mit dem Velo unterwegs ist, möchte ich die aktuelle Windgeschwindigkeit am abgefragten Ort sehen, damit ich vor der Abfahrt die Bedingungen einschätzen kann.

### Akzeptanzkriterien

1. Bei verfügbaren Winddaten zeigt `weather "Zürich"` zusätzlich eine beschriftete Windgeschwindigkeit mit der Einheit km/h für denselben Ort.
2. Ein Windwert von 0 wird als `0 km/h` angezeigt und nicht als fehlender Wert behandelt.
3. Fehlen verwertbare Winddaten, erscheint «Wind nicht verfügbar»; die übrigen verfügbaren Wetterinformationen bleiben lesbar.

**Umfang:** Ein aktueller Zahlenwert mit Einheit; keine Windrichtung, Böen oder Warnstufen. Baut auf US-01 auf; US-02 ist keine Voraussetzung.

## US-04 – Wetter für eine Stadt mit mehrteiligem Namen abrufen

**Priorität:** 4 · Should · **Status:** Für Refinement vorbereitet · **Schätzung:** offen

Als reisende Terminalnutzerin möchte ich Wetter für eine Stadt mit Leerzeichen im Namen abrufen, damit ich auch für solche Reiseziele passende Wetterinformationen erhalte.

### Akzeptanzkriterien

1. `weather "New York"` verarbeitet den gesamten Namen als einen Ort und zeigt bei erfolgreicher eindeutiger Ortssuche das aktuelle Wetter für New York mit Land und Temperatur.
2. Führende und nachfolgende Leerzeichen innerhalb des Arguments werden ignoriert: `weather "  New York  "` fragt denselben Ort wie `weather "New York"` ab.
3. Ein Argument, das nur Leerzeichen enthält, zeigt einen Hinweis auf die fehlende Stadt und einen Beispielaufruf; der Exit-Code ist ungleich 0.
4. Mehrere unquotierte Ortsargumente wie `weather New York` werden mit einem Hinweis auf die nötigen Anführungszeichen und einem Exit-Code ungleich 0 abgewiesen; es wird nicht stillschweigend nur «New» abgefragt.

**Umfang:** Ein mehrteiliger Ortsname, keine Abfrage mehrerer Städte. Baut auf US-01 auf und deckt Eingabe, Ortssuche und sichtbares Ergebnis ab.

## US-05 – Wetterbefehl ohne externe Anleitung bedienen

**Priorität:** 5 · Should · **Status:** Für Refinement vorbereitet · **Schätzung:** offen

Als neue Terminalnutzerin möchte ich die gültige Syntax und konkrete Beispiele direkt im Terminal sehen, damit ich meine erste Wetterabfrage ohne externe Anleitung ausführen kann.

### Akzeptanzkriterien

1. `weather --help` zeigt den Zweck der Anwendung, die Syntax `weather "STADT"` und je ein Beispiel mit einem einteiligen und einem mehrteiligen Stadtnamen; der Exit-Code ist 0.
2. Die Hilfe lässt sich auch ohne Internetverbindung anzeigen und benötigt keine Wetterabfrage.
3. Eine unbekannte Option wie `weather --unbekannt` zeigt die betreffende Option, einen Hinweis auf `weather --help` und einen Exit-Code ungleich 0.

**Umfang:** Eine Hilfeseite und Rückmeldung zu unbekannten Optionen; keine interaktive Befehlsshell. Eigenständiger sichtbarer Nutzen ohne Abhängigkeit vom Wetterdienst.

## Weitere Einträge – nach Sprint 1 zu verfeinern

Diese Themen aus der Story Map sind noch nicht schätzbereit und ausdrücklich keine ausgewählten Sprint-1-Stories.

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

### Vor dem Planning prüfen

- Die fünf Stories stehen mit diesem Inhalt und dieser Reihenfolge im Team-Board; Links sind ergänzt.
- Befehlsname, Wetterdienst und Umgang mit mehrdeutigen Ortsnamen sind geklärt.
- Jede Story wird vom Team geschätzt; bei mehr als zwei Modultagen entlang einer nutzbaren Aktion weiter schneiden.
- Erst nach Kapazitätsabgleich Sprint-Zuordnung und Verantwortliche setzen.
