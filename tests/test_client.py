"""Tests für Nicos API-Anbindung (WEA-15, WEA-16) mit gekürzten echten Open-Meteo-Antworten."""

import unittest
from unittest.mock import patch

from weathercli.client import (FORECAST_URL, GEOCODING_URL, Location, WeatherError,
                               current_temperature, current_weather, resolve_city)


def place(name, country, population=None, feature_code="PPL", latitude=47.37, longitude=8.55):
    return {"name": name, "country": country, "population": population,
            "feature_code": feature_code, "latitude": latitude, "longitude": longitude}


ZUERICH = [place("Zürich", "Schweiz", 415367, "PPLA", 47.36667, 8.55),
           place("Zurich", "Niederlande", 145), place("Zurich", "Vereinigte Staaten"),
           place("Sidi Amar", "Algerien"),
           place("Zürich (Kreis 11)", "Schweiz", 54260, "PPLX")]
NEW_YORK = [place("York", "Vereinigte Staaten", 7864, "PPLA2"),
            place("New York", "Vereinigtes Königreich"), place("New York", "Jamaika"),
            place("New York City", "Vereinigte Staaten", 8804190, latitude=40.71, longitude=-74.01)]
FRANKFURT = [place("Frankfurt am Main", "Deutschland", 650000, "PPLA3"),
             place("Frankfurt", "Deutschland"), place("Frankfurt (Oder)", "Deutschland", 57015)]
SPRINGFIELD = [place("Springfield", "Vereinigte Staaten", 170188),
               place("Springfield", "Vereinigte Staaten", 154341)]


class ResolveCityTests(unittest.TestCase):
    def resolve(self, city, response):
        with patch("weathercli.client.request_json", return_value=response) as request:
            return resolve_city(city), request

    def test_query_parameters(self):
        _, request = self.resolve("Zürich", {"results": ZUERICH})
        request.assert_called_once_with(GEOCODING_URL, {
            "name": "Zürich", "count": 20, "language": "de", "format": "json"})

    def test_dominant_city_is_resolved_without_other_places(self):
        for city in ("Zürich", "zürich", "Zurich", "ZURICH"):
            with self.subTest(city=city):
                location, _ = self.resolve(city, {"results": ZUERICH})
                self.assertEqual(location, Location("Zürich", "Schweiz", 47.36667, 8.55))

    def test_multiword_name_finds_city_not_similar_place(self):
        location, _ = self.resolve("New York", {"results": NEW_YORK})
        self.assertEqual(location, Location("New York City", "Vereinigte Staaten", 40.71, -74.01))

    def test_name_may_continue_as_whole_word(self):
        location, _ = self.resolve("Frankfurt", {"results": FRANKFURT})
        self.assertEqual(location.name, "Frankfurt am Main")

    def test_single_match_without_population(self):
        location, _ = self.resolve("Genf", {"results": [place("Genf", "Schweiz"), place("Genfeld", "Deutschland")]})
        self.assertEqual(location.name, "Genf")

    def test_similar_sized_places_are_ambiguous(self):
        for results in (SPRINGFIELD, [place("New York", "Jamaika"), place("New York", "Vereinigtes Königreich")]):
            with self.subTest(results=results), self.assertRaisesRegex(WeatherError, "mehrdeutig"):
                self.resolve(results[0]["name"], {"results": results})

    def test_no_match_when_results_missing_or_only_other_names(self):
        for response in ({"generationtime_ms": 0.2}, {"results": []},
                         {"results": [place("Münchendorf", "Österreich", 2992)]}):
            with self.subTest(response=response), self.assertRaisesRegex(WeatherError, "Kein Ort gefunden"):
                self.resolve("Muenchen", response)

    def test_malformed_results_are_rejected(self):
        for response in ({"results": None}, {"results": [None]},
                         {"results": [{**ZUERICH[0], "country": None}]},
                         {"results": [{**ZUERICH[0], "latitude": "47"}]}):
            with self.subTest(response=response), self.assertRaises(WeatherError):
                self.resolve("Zürich", response)

    def test_service_error_is_passed_on(self):
        with patch("weathercli.client.request_json", side_effect=WeatherError("nicht erreichbar")):
            with self.assertRaisesRegex(WeatherError, "nicht erreichbar"):
                resolve_city("Zürich")


class CurrentTemperatureTests(unittest.TestCase):
    place = Location("Zürich", "Schweiz", 47.36667, 8.55)

    def forecast(self, value=16.3, unit="°C"):
        return {"latitude": 47.36, "longitude": 8.56,
                "current_units": {"time": "iso8601", "temperature_2m": unit},
                "current": {"time": "2026-09-21T08:15", "temperature_2m": value}}

    def test_query_parameters_and_temperature(self):
        with patch("weathercli.client.request_json", return_value=self.forecast()) as request:
            self.assertEqual(current_temperature(self.place), 16.3)
        request.assert_called_once_with(FORECAST_URL, {
            "latitude": 47.36667, "longitude": 8.55,
            "current": "temperature_2m", "temperature_unit": "celsius"})

    def test_zero_and_negative_are_valid(self):
        for value in (0, -7.5):
            with self.subTest(value=value):
                with patch("weathercli.client.request_json", return_value=self.forecast(value)):
                    self.assertEqual(current_temperature(self.place), value)

    def test_missing_or_invalid_temperature_is_an_error(self):
        broken = [{}, {"current": {}}, self.forecast(None), self.forecast("16"),
                  self.forecast(unit="°F"), {"current": {"temperature_2m": 16.3}}]
        for data in broken:
            with self.subTest(data=data), self.assertRaises(WeatherError):
                with patch("weathercli.client.request_json", return_value=data):
                    current_temperature(self.place)

    def test_adapter_returns_checked_temperature_for_output(self):
        with patch("weathercli.client.request_json", return_value=self.forecast(-2)):
            self.assertEqual(current_weather(self.place), {
                "current": {"temperature_2m": -2}, "current_units": {"temperature_2m": "°C"}})


if __name__ == "__main__":
    unittest.main()
