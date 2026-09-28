"""Sprint 1, WEA-17: Ort, Land und aktuelle Temperatur.
Sprint 2, WEA-21: dazu der Wetterzustand aus demselben Datensatz."""

from .client import Location
from .conditions import condition_from_response
from .errors import temperature_from_response

CONDITION_UNAVAILABLE = "Wetterzustand nicht verfügbar"


def format_weather(location: Location, data: dict) -> str:
    """Formatiert Werte desselben aktuellen Datensatzes, ohne weitere Abfrage."""
    temperature = temperature_from_response(data)
    condition = condition_from_response(data) or CONDITION_UNAVAILABLE
    return f"{location.name}, {location.country}: {temperature:g} °C, {condition}"
