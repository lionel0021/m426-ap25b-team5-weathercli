"""Sprint 1, WEA-17: Ort, Land und aktuelle Temperatur."""

from .client import Location
from .errors import temperature_from_response


def format_weather(location: Location, data: dict) -> str:
    """Formatiert Werte desselben aktuellen Datensatzes, ohne weitere Abfrage."""
    temperature = temperature_from_response(data)
    return f"{location.name}, {location.country}: {temperature:g} °C"
