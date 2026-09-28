"""Sprint 1, WEA-17: Ort, Land und aktuelle Temperatur.
Sprint 2, WEA-21: dazu der Wetterzustand, WEA-22/23: dazu der Wind.
Alle Werte stammen aus demselben Datensatz, ohne weitere Abfrage."""

from .client import Location
from .conditions import condition_from_response
from .errors import finite_number, temperature_from_response

CONDITION_UNAVAILABLE = "Wetterzustand nicht verfügbar"
WIND_UNAVAILABLE = "Wind nicht verfügbar"


def format_weather(location: Location, data: dict) -> str:
    """Formatiert Temperatur, Wetterzustand und Wind desselben Datensatzes.

    Die Temperatur ist Pflicht; fehlen Zustand oder Wind, steht dort der
    jeweilige Hinweis und die übrigen Werte bleiben lesbar.
    """
    temperature = temperature_from_response(data)
    condition = condition_from_response(data) or CONDITION_UNAVAILABLE
    return (f"{location.name}, {location.country}: {temperature:g} °C, "
            f"{condition}, {wind_from_response(data)}")


def wind_from_response(data: dict) -> str:
    """WEA-22/23: Wind mit Einheit km/h; 0 km/h ist ein gültiger Wert."""
    current = data.get("current", {})
    units = data.get("current_units", {})
    wind_speed = current.get("wind_speed_10m") if isinstance(current, dict) else None
    wind_unit = units.get("wind_speed_10m") if isinstance(units, dict) else None
    if finite_number(wind_speed) and wind_unit == "km/h":
        return f"Wind: {wind_speed:g} km/h"
    return WIND_UNAVAILABLE
