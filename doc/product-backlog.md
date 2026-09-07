# Product Backlog – WeatherCLI

**Priorisierungsmethode:** Value/Effort — geordnet nach Nutzen für die Benutzerin
im Verhältnis zum Aufwand, abgeleitet aus der Story Map
([StoryBoard.png](./StoryBoard.png), Release 1 = MVP).
Die Reihenfolge im Backlog ist die Reihenfolge, in der wir die Stories ziehen.

**Refinement-Stand:** Modultag 4. Die fünf obersten Stories sind geschärft
(Rolle, Nutzen, 2–4 prüfbare Akzeptanzkriterien, klein genug für zwei Modultage).
Alles darunter ist bewusst noch grob und wird vor dem nächsten Planning geschärft.

**Schnitt:** Wir haben die Story-Map-Karten *nicht* entlang der technischen
Schichten geschnitten (API-Zugriff / Formatierung / Ausgabe), sondern entlang
dem, was die Benutzerin tut. Jede Story unten geht durch alle Ebenen und liefert
etwas, das man im Terminal sehen kann. Die technischen Schritte stehen als
Aufgaben unter der jeweiligen Story.

---

## Sprint-1-Kandidaten (geschärft)

### WCLI-1 · Aktuelles Wetter für eine Stadt abfragen
Board: [Issue #1](https://github.com/lionel0021/m426-ap25b-team5-weathercli/issues/1)
**Als** Nutzerin, die im Terminal arbeitet,
**möchte ich** mit einem Befehl das aktuelle Wetter einer Stadt abrufen,
**damit** ich meine Arbeit nicht unterbrechen und keinen Browser öffnen muss.

Akzeptanzkriterien:
1. `weathercli Zürich` gibt für die Stadt Ortsname, Temperatur in °C und eine
   Wetterbeschreibung (z. B. „bewölkt") in einer Terminalausgabe aus.
2. Die ausgegebenen Werte stammen aus der Wetter-API und sind nicht älter als
   die zuletzt gemeldete Messung des Anbieters.
3. Ist die Stadt mehrdeutig oder unbekannt, bricht die Anwendung nicht ab,
   sondern gibt eine Zeile Text aus und beendet sich mit Exit-Code ungleich 0.
4. Der Befehl liefert die Ausgabe ohne weitere Eingabe durch die Nutzerin.

Aufgaben: API-Client, Argument-Parsing, Ausgabeformat, API-Key aus Umgebungsvariable.

---

### WCLI-2 · Verständliche Meldung bei unbekannter Stadt
Board: [Issue #2](https://github.com/lionel0021/m426-ap25b-team5-weathercli/issues/2)
**Als** Nutzerin, die sich vertippt hat,
**möchte ich** eine Meldung sehen, die mir sagt, was falsch war,
**damit** ich den Befehl korrigieren kann, statt einen Stacktrace zu deuten.

Akzeptanzkriterien:
1. `weathercli Zuerichhh` gibt aus: „Stadt 'Zuerichhh' wurde nicht gefunden."
2. Es erscheint kein Stacktrace und keine technische Fehlermeldung der Bibliothek.
3. Der Exit-Code ist 1.

Aufgaben: 404-Antwort der API abfangen, Fehlerausgabe auf stderr.

---

### WCLI-3 · Hilfe bei fehlender Eingabe
Board: [Issue #3](https://github.com/lionel0021/m426-ap25b-team5-weathercli/issues/3)
**Als** Nutzerin, die das Tool zum ersten Mal aufruft,
**möchte ich** bei einem Aufruf ohne Stadt sehen, wie der Befehl geht,
**damit** ich das Tool ohne Dokumentation benutzen kann.

Akzeptanzkriterien:
1. `weathercli` ohne Argument gibt eine Verwendungszeile aus, die mindestens
   ein vollständiges Beispiel enthält (`weathercli <Stadt>`).
2. `weathercli --help` gibt dieselbe Verwendungszeile aus und endet mit Exit-Code 0.
3. Der Aufruf ohne Argument endet mit Exit-Code ungleich 0.

Aufgaben: Usage-Text, Hilfe-Flag im Argument-Parsing.

---

### WCLI-4 · Wind und Luftfeuchtigkeit mit anzeigen
Board: [Issue #4](https://github.com/lionel0021/m426-ap25b-team5-weathercli/issues/4)
**Als** Nutzerin, die entscheidet, ob sie Velo fährt,
**möchte ich** neben der Temperatur auch Wind und Luftfeuchtigkeit sehen,
**damit** ich die Bedingungen einschätzen kann, ohne eine zweite Quelle zu öffnen.

Akzeptanzkriterien:
1. Die Ausgabe von `weathercli Bern` enthält zusätzlich Windgeschwindigkeit in km/h
   und Luftfeuchtigkeit in Prozent, jeweils mit Einheit.
2. Die Werte stehen untereinander in gleich ausgerichteten Zeilen (Label und Wert
   in fester Spaltenbreite).
3. Liefert die API einen dieser Werte nicht, erscheint in der Zeile `–` statt
   eines leeren Feldes oder `null`.

Aufgaben: zusätzliche Felder aus der API-Antwort, Formatierungsfunktion.

---

### WCLI-5 · Vorhersage für die nächsten Tage abrufen
Board: [Issue #5](https://github.com/lionel0021/m426-ap25b-team5-weathercli/issues/5)
**Als** Nutzerin, die eine Wanderung plant,
**möchte ich** die Vorhersage für die nächsten Tage im Terminal sehen,
**damit** ich einen Tag wählen kann, ohne eine Wetter-Website zu besuchen.

Akzeptanzkriterien:
1. `weathercli Chur --forecast` gibt für die nächsten drei Tage je eine Zeile mit
   Datum, Höchst- und Tiefsttemperatur und Wetterbeschreibung aus.
2. Ohne `--forecast` bleibt die Ausgabe aus WCLI-1 unverändert.
3. Ist die Stadt unbekannt, erscheint dieselbe Meldung wie in WCLI-2.

Aufgaben: Forecast-Endpunkt, Datumsformatierung, Flag im Argument-Parsing.

---

## Weiteres Backlog (noch nicht geschärft)

| # | Story / Epic | Herkunft Story Map |
|---|---|---|
| 6 | Ungültigen Befehl erkennen und melden | Release 2 |
| 7 | Verbindungsfehler melden und erneute Abfrage ermöglichen | Release 3 |
| 8 | Mehrere Städte in einem Aufruf abfragen | Release 3 |
| 9 | Zuletzt abgefragte Städte vorschlagen | Release 3 |
| 10 | Einstellungen (Standardstadt, Einheit) speichern | Release 3 |
