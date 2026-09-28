"""Formatiert Ort, Temperatur und Windgeschwindigkeit für die CLI."""

from .client import Location
from .errors import finite_number, temperature_from_response


def format_weather(location: Location, data: dict) -> str:
    """Formatiert Temperatur und optionale Winddaten desselben Datensatzes."""
    temperature = temperature_from_response(data)
    current = data.get("current", {})
    units = data.get("current_units", {})
    wind_speed = current.get("wind_speed_10m") if isinstance(current, dict) else None
    wind_unit = units.get("wind_speed_10m") if isinstance(units, dict) else None
    if finite_number(wind_speed) and wind_unit == "km/h":
        wind = f"Wind: {wind_speed:g} km/h"
    else:
        wind = "Wind nicht verfügbar"
    return f"{location.name}, {location.country}: {temperature:g} °C, {wind}"
