"""Open-Meteo-Anbindung für Sprint 1: Ortssuche (WEA-15) und Temperatur (WEA-16)."""

import unicodedata
from dataclasses import dataclass
from .errors import WeatherError, finite_number, request_json, temperature_from_response, unique_location

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
# Mit count=5 fehlt bei "New York" (language=de) New York City in den Treffern.
GEOCODING_COUNT = 20
# Ein passender Ort gilt als gemeint, wenn er mindestens zehnmal mehr
# Einwohner hat als jeder andere passende Ort.
DOMINANCE_FACTOR = 10


@dataclass(frozen=True)
class Location:
    name: str
    country: str
    latitude: float
    longitude: float


def resolve_city(city: str) -> Location:
    """WEA-15: Sucht die Stadt und liefert sie nur, wenn sie eindeutig ist."""
    data = request_json(GEOCODING_URL, {
        "name": city, "count": GEOCODING_COUNT, "language": "de", "format": "json",
    })
    place = unique_location(_candidates(data, city))
    return Location(place["name"], place["country"], place["latitude"], place["longitude"])


def _candidates(data: dict, city: str) -> dict:
    """Reduziert die Treffer auf die Orte, die mit der Eingabe gemeint sein können.

    Passend ist ein Ort, dessen Name der Eingabe entspricht oder mit ihr als
    ganzem Wort beginnt ("Frankfurt" -> "Frankfurt am Main"); Stadtteile (PPLX)
    zählen nicht. Unpassende Treffer wie "York" für "New York" fallen weg.
    Überragt ein passender Ort alle anderen deutlich, bleibt nur er übrig
    ("Zürich" statt Zurich in den Niederlanden). Ungültige Daten gehen
    unverändert an unique_location, das sie meldet.
    """
    results = data.get("results", [])
    if not isinstance(results, list) or not all(isinstance(result, dict) for result in results):
        return data
    wanted = _normalize(city)
    matches = [result for result in results
               if result.get("feature_code") != "PPLX" and _name_matches(result.get("name"), wanted)]
    populations = sorted((_population(result) for result in matches), reverse=True)
    if len(matches) > 1 and populations[0] >= DOMINANCE_FACTOR * max(populations[1], 1):
        matches = [max(matches, key=_population)]
    return {"results": matches}


def _name_matches(name, wanted: str) -> bool:
    if not isinstance(name, str):
        return False
    name = _normalize(name)
    return name == wanted or name.startswith(wanted + " ")


def _normalize(text: str) -> str:
    """Vergleichsform ohne Gross/Klein und Akzente: "  ZÜRICH " -> "zurich"."""
    decomposed = unicodedata.normalize("NFKD", text)
    without_accents = "".join(char for char in decomposed if not unicodedata.combining(char))
    return " ".join(without_accents.casefold().split())


def _population(result: dict) -> float:
    population = result.get("population")
    return population if finite_number(population) else 0


def current_temperature(location: Location) -> float:
    """WEA-16: Aktuelle Temperatur am Ort in °C, Einheit von der API bestätigt."""
    data = request_json(FORECAST_URL, {
        "latitude": location.latitude, "longitude": location.longitude,
        "current": "temperature_2m", "temperature_unit": "celsius",
    })
    return temperature_from_response(data)


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
