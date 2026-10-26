"""Sprint 1, WEA-17: Ort, Land und aktuelle Temperatur.
Sprint 2, WEA-21: dazu der Wetterzustand, WEA-22/23: dazu der Wind.
Sprint 3, WEA-33: dazu die Vorhersage für morgen.
Alle Werte stammen aus demselben Datensatz, ohne weitere Abfrage."""

from .client import Location
from .conditions import condition_from_code, condition_from_response
from .errors import finite_number, temperature_from_response

CONDITION_UNAVAILABLE = "Wetterzustand nicht verfügbar"
WIND_UNAVAILABLE = "Wind nicht verfügbar"
FORECAST_UNAVAILABLE = "Vorhersage nicht verfügbar"
# In der Tagesliste der Antwort steht an Index 0 heute und an Index 1 morgen.
TOMORROW_INDEX = 1


def format_weather(location: Location, data: dict) -> str:
    """Formatiert Temperatur, Wetterzustand und Wind desselben Datensatzes.

    Die Temperatur ist Pflicht; fehlen Zustand oder Wind, steht dort der
    jeweilige Hinweis und die übrigen Werte bleiben lesbar.
    """
    temperature = temperature_from_response(data)
    condition = condition_from_response(data) or CONDITION_UNAVAILABLE
    return (f"{location.name}, {location.country}: {temperature:g} °C, "
            f"{condition}, {wind_from_response(data)}")


def format_tomorrow(location: Location, data: dict) -> str:
    """WEA-33: Wetterzustand und Temperaturbereich für morgen.

    Fehlt ein Temperaturwert, ist er nicht endlich, stimmt die Einheit nicht
    oder enthält die Antwort keinen morgigen Tag, steht dort
    "Vorhersage nicht verfügbar". Ein fehlender oder unbekannter Wettercode
    lässt den Temperaturbereich stehen. In allen Fällen ohne Absturz und ohne
    erfundene Werte (US-06, AK 3).
    """
    place = f"{location.name}, {location.country}, morgen: "
    temperatures = _tomorrow_temperatures(data)
    if temperatures is None:
        return place + FORECAST_UNAVAILABLE
    minimum, maximum = temperatures
    condition = _tomorrow_condition(data) or CONDITION_UNAVAILABLE
    return f"{place}{condition}, {minimum:g} bis {maximum:g} °C"


def _tomorrow_temperatures(data: dict):
    """Tiefst- und Höchstwert für morgen in °C oder None, wenn einer fehlt."""
    daily = _daily(data)
    units = data.get("daily_units") if isinstance(data, dict) else None
    if daily is None or not isinstance(units, dict):
        return None
    values = []
    for key in ("temperature_2m_min", "temperature_2m_max"):
        value = _tomorrow_value(daily.get(key))
        if not finite_number(value) or units.get(key) != "°C":
            return None
        values.append(value)
    return values[0], values[1]


def _tomorrow_condition(data: dict):
    """Zustand für morgen; None, wenn der Code fehlt oder unbekannt ist.

    conditions.condition_from_response liest `current` und passt hier nicht:
    die Tagesvorhersage liefert den Code als Liste unter `daily`. Die Prüfung
    des Codes selbst übernimmt conditions.condition_from_code.
    """
    daily = _daily(data)
    return condition_from_code(_tomorrow_value(daily.get("weather_code")) if daily else None)


def _daily(data: dict):
    daily = data.get("daily") if isinstance(data, dict) else None
    return daily if isinstance(daily, dict) else None


def _tomorrow_value(values):
    """Der Wert für morgen aus einer Tagesliste, sonst None."""
    if not isinstance(values, list) or len(values) <= TOMORROW_INDEX:
        return None
    return values[TOMORROW_INDEX]


def wind_from_response(data: dict) -> str:
    """WEA-22/23: Wind mit Einheit km/h; 0 km/h ist ein gültiger Wert."""
    current = data.get("current", {})
    units = data.get("current_units", {})
    wind_speed = current.get("wind_speed_10m") if isinstance(current, dict) else None
    wind_unit = units.get("wind_speed_10m") if isinstance(units, dict) else None
    if finite_number(wind_speed) and wind_unit == "km/h":
        return f"Wind: {wind_speed:g} km/h"
    return WIND_UNAVAILABLE
