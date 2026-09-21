"""WEA-18: gemeinsame HTTP- und Datenfehlerbehandlung für Nicos Anbindung."""

import json
import math
from http.client import HTTPException
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen


class WeatherError(Exception):
    """Verständlicher Fehlertext für stderr und Exit-Code 1."""


def finite_number(value):
    return type(value) in (int, float) and math.isfinite(value)


def request_json(endpoint: str, parameters: dict) -> dict:
    try:
        with urlopen(f"{endpoint}?{urlencode(parameters)}", timeout=10) as response:
            data = json.load(response)
    except HTTPError as error:
        error.close()
        raise WeatherError("Wetterdienst nicht erreichbar. Bitte später erneut versuchen.") from error
    except (URLError, OSError, HTTPException) as error:
        raise WeatherError("Wetterdienst nicht erreichbar. Bitte später erneut versuchen.") from error
    except (ValueError, UnicodeError) as error:
        raise WeatherError("Der Wetterdienst hat ungültige Daten geliefert.") from error
    if not isinstance(data, dict) or data.get("error"):
        raise WeatherError("Der Wetterdienst hat ungültige Daten geliefert.")
    return data


def unique_location(data: dict) -> dict:
    """Prüft die Ortssuche; liefert genau einen vollständigen Ort."""
    if not isinstance(data, dict) or data.get("error"):
        raise WeatherError("Die Ortssuche hat ungültige Daten geliefert.")
    results = data.get("results", [])
    if not isinstance(results, list):
        raise WeatherError("Die Ortssuche hat ungültige Daten geliefert.")
    if not results:
        raise WeatherError("Kein Ort gefunden. Bitte eine genauere Ortsangabe eingeben.")
    if len(results) != 1:
        raise WeatherError("Der Ort ist mehrdeutig. Bitte eine genauere Ortsangabe eingeben.")
    result = results[0]
    if not isinstance(result, dict):
        raise WeatherError("Die Ortssuche hat ungültige Daten geliefert.")
    for key in ("name", "country"):
        if not isinstance(result.get(key), str) or not result[key].strip():
            raise WeatherError("Die Ortssuche hat unvollständige Ortsdaten geliefert.")
    for key, limit in (("latitude", 90), ("longitude", 180)):
        value = result.get(key)
        if not finite_number(value) or not -limit <= value <= limit:
            raise WeatherError("Die Ortssuche hat ungültige Koordinaten geliefert.")
    return result


def temperature_from_response(data: dict) -> float:
    if not isinstance(data, dict) or data.get("error"):
        raise WeatherError("Aktuelle Temperatur nicht verfügbar.")
    current, units = data.get("current"), data.get("current_units")
    if not isinstance(current, dict) or not isinstance(units, dict):
        raise WeatherError("Aktuelle Temperatur nicht verfügbar.")
    temperature = current.get("temperature_2m")
    if not finite_number(temperature) or units.get("temperature_2m") != "°C":
        raise WeatherError("Aktuelle Temperatur in °C nicht verfügbar.")
    return temperature
