# Portfolio – Team 5 · WeatherCLI

Modul M426 · Software mit agilen Methoden entwickeln · AP 25b
Repository: https://github.com/lionel0021/m426-ap25b-team5-weathercli

---

## 1. Team und Produkt

**Produkt:** WeatherCLI — eine Kommandozeilen-Anwendung, die aktuelle Wetterdaten
und Vorhersagen direkt im Terminal ausgibt, ohne dass eine Website oder App
geöffnet werden muss.

**Team 5:**

| Name | Rolle |
|---|---|
| Eduart Maliqi | Product Owner |
| Fidan | Scrum Master |
| Nico | Entwickler |
| Lionel | Entwickler |

---

## 2. Product Vision

Schnellen und einfachen Zugriff auf aktuelle Wetterdaten und Vorhersagen direkt im
Terminal ermöglichen.

- **Motivation:** Wetterinformationen schnell abrufen.
- **Positive Veränderung:** keine Website oder App öffnen müssen, sondern direkt
  im Terminal nachsehen.
- **Zielgruppe:** Personen, die häufig im Terminal arbeiten (Entwicklerinnen und
  Entwickler), und Personen, die schnell Wetterdaten brauchen.
- **Needs:** aktuelles Wetter abrufen, Vorhersage für eine gewünschte Stadt
  anzeigen, einfache Bedienung, übersichtliche Wetterinformationen.
- **Business Goals:** Anforderungen des Projekts erfüllen, Teamarbeit mit Scrum
  üben, sauberen und wartbaren Code entwickeln, Projekt termingerecht abschliessen.

**Product Vision Board:** [Product Vision – WeatherCLI.png](./Product%20Vision%20–%20WeatherCLI.png)
**KI-Bewertung der Vision:** [ki-bewertung.md](./ki-bewertung.md)

---

## 3. Product Backlog

**Priorisierungsmethode:** Value/Effort — nach Nutzen für die Benutzerin im
Verhältnis zum Aufwand, abgeleitet aus der Story Map. Release 1 der Story Map
bildet den MVP und damit den Kopf des Backlogs.

**Story Map (Auftrag 3.1):** [StoryBoard.png](./StoryBoard.png)
**Vollständiges Backlog mit den geschärften Stories:** [product-backlog.md](./product-backlog.md)

Die fünf obersten Stories nach dem Refinement an Modultag 4:

| # | Story | Board-Eintrag |
|---|---|---|
| WCLI-1 | Aktuelles Wetter für eine Stadt abfragen | [#1](https://github.com/lionel0021/m426-ap25b-team5-weathercli/issues/1) |
| WCLI-2 | Verständliche Meldung bei unbekannter Stadt | [#2](https://github.com/lionel0021/m426-ap25b-team5-weathercli/issues/2) |
| WCLI-3 | Hilfe bei fehlender Eingabe | [#3](https://github.com/lionel0021/m426-ap25b-team5-weathercli/issues/3) |
| WCLI-4 | Wind und Luftfeuchtigkeit mit anzeigen | [#4](https://github.com/lionel0021/m426-ap25b-team5-weathercli/issues/4) |
| WCLI-5 | Vorhersage für die nächsten Tage abrufen | [#5](https://github.com/lionel0021/m426-ap25b-team5-weathercli/issues/5) |

Alle fünf Stories sind als GitHub Issues erfasst und damit auch ausserhalb des
Unterrichts bearbeitbar — sie liegen nicht mehr nur als Foto der Story Map vor.

Beim Refinement haben wir die Karten der Story Map neu geschnitten: statt entlang
der technischen Schichten („Wetter laden" / „Wetter anzeigen") entlang dem, was
die Benutzerin tut. Jede der fünf Stories geht durch alle Ebenen und liefert eine
sichtbare Terminalausgabe. Keine davon ist mehr ein Epic.

**Definition of Done:** [definition-of-done.md](./definition-of-done.md)

---

## 4. Sprints

### Sprint 0 (Modultage 1–4)

**Ziel:** Produktidee festlegen, Backlog aufbauen und arbeitsfähig machen.

**Ergebnisse:**
- Product Vision Board erstellt und per KI bewertet
- Story Map mit fünf Epics und drei Releases
- Product Backlog mit fünf geschärften Stories an der Spitze, als Issues #1–#5 im Repository erfasst
- Definition of Done vereinbart (6 Kriterien)

**Retrospective** (Volltext: [retrospective-sprint0.md](./retrospective-sprint0.md)):

- *Was hat funktioniert:* Vision war nach einer Runde abgestimmt; die Story Map
  hat den Umfang sichtbar gemacht; die Arbeit liess sich gut parallel aufteilen.
- *Was hat gebremst:* Die Stories lagen nur als Foto vor, nicht als Board-Einträge —
  ausserhalb des Unterrichts konnte niemand daran weiterarbeiten. Zudem waren die
  Karten technisch geschnitten und einzeln nicht schätzbar.

**Verbesserungsmassnahme für Sprint 1:**
> Jede Story, die wir in Sprint 1 ziehen, existiert als Eintrag im GitHub-Board,
> bevor jemand mit dem Code beginnt — und wird beim Statuswechsel sofort
> verschoben (To Do → In Progress → Done).

*Nachprüfbar an Modultag 6:* Für jede bearbeitete Story existiert ein
Board-Eintrag, und keiner steht am Sprint-Ende noch in „To Do", obwohl der Code
gemerged ist. Der Scrum Master prüft es zu Beginn jedes Daily.

*Sprint Planning, Daily-Notizen und Review werden an Modultag 5 ergänzt.*

### Sprint 1 (ab Modultag 5)

*Wird an Modultag 5 gefüllt.*
