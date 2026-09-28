"""Wetterzustand aus dem WMO-Code der Open-Meteo-Antwort (WEA-19, WEA-20).

Open-Meteo liefert den Zustand nur als Zahl (`weather_code`, Einheit "wmo code").
Diese Tabelle uebersetzt die von Open-Meteo dokumentierten Codes in deutsche
Bezeichnungen. Ein fehlender oder unbekannter Code ergibt None; die Ausgabe
meldet dann "Wetterzustand nicht verfuegbar" (WEA-21).
"""

from .errors import finite_number

WMO_CONDITIONS = {
    0: "Klar",
    1: "Überwiegend klar",
    2: "Teilweise bewölkt",
    3: "Bewölkt",
    45: "Nebel",
    48: "Gefrierender Nebel",
    51: "Leichter Sprühregen",
    53: "Sprühregen",
    55: "Starker Sprühregen",
    56: "Leichter gefrierender Sprühregen",
    57: "Gefrierender Sprühregen",
    61: "Leichter Regen",
    63: "Regen",
    65: "Starker Regen",
    66: "Leichter gefrierender Regen",
    67: "Gefrierender Regen",
    71: "Leichter Schneefall",
    73: "Schneefall",
    75: "Starker Schneefall",
    77: "Schneegriesel",
    80: "Leichte Regenschauer",
    81: "Regenschauer",
    82: "Starke Regenschauer",
    85: "Leichte Schneeschauer",
    86: "Starke Schneeschauer",
    95: "Gewitter",
    96: "Gewitter mit leichtem Hagel",
    99: "Gewitter mit starkem Hagel",
}


def condition_from_response(data: dict):
    """Gibt den ausgeschriebenen Wetterzustand zurueck oder None.

    None steht fuer "nicht verfuegbar": kein `weather_code` in der Antwort,
    kein ganzzahliger Wert oder ein Code, den die Tabelle nicht kennt. Die
    Temperatur derselben Antwort bleibt davon unberuehrt.
    """
    if not isinstance(data, dict):
        return None
    current = data.get("current")
    if not isinstance(current, dict):
        return None
    code = current.get("weather_code")
    if not finite_number(code) or code != int(code):
        return None
    return WMO_CONDITIONS.get(int(code))
