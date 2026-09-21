"""Schnittstelle für Nicos API-Tasks WEA-15 und WEA-16 in Sprint 1."""

from dataclasses import dataclass
from .errors import WeatherError


@dataclass(frozen=True)
class Location:
    name: str
    country: str
    latitude: float
    longitude: float


def resolve_city(city: str) -> Location:
    """WEA-15: request_json + unique_location aus errors.py verwenden."""
    raise WeatherError("Ortssuche noch nicht implementiert (WEA-15, Nico).")


def current_temperature(location: Location) -> float:
    """WEA-16: request_json + temperature_from_response aus errors.py nutzen."""
    raise WeatherError("Wetterabfrage noch nicht implementiert (WEA-16, Nico).")


def current_weather(location: Location) -> dict:
    """Kompatibler Adapter für Sprint 1: ausschliesslich Temperatur.

    current_temperature muss die Celsius-Einheit zuvor mit
    errors.temperature_from_response geprüft haben. Nico kann alternativ
    hier direkt die geprüfte API-Antwort zurückgeben.
    """
    return {
        "current": {"temperature_2m": current_temperature(location)},
        "current_units": {"temperature_2m": "°C"},
    }
