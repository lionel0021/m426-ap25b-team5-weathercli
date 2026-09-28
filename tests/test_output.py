import unittest
from weathercli.client import Location, WeatherError
from weathercli.output import format_weather


class OutputTests(unittest.TestCase):
    place = Location("New York", "USA", 40.7, -74.0)

    def payload(self, value=20, unit="°C"):
        return {"current": {"temperature_2m": value},
                "current_units": {"temperature_2m": unit}}

    def test_temperature_including_zero_and_negative(self):
        for value in (0, 20.5, -8):
            with self.subTest(value=value):
                self.assertEqual(format_weather(self.place, self.payload(value)),
                                 f"New York, USA: {value:g} °C, Wind nicht verfügbar")

    def test_wind_is_formatted_in_kmh_including_zero(self):
        data = {"current": {"temperature_2m": 20, "wind_speed_10m": 0},
                "current_units": {"temperature_2m": "°C", "wind_speed_10m": "km/h"}}
        self.assertEqual(format_weather(self.place, data),
                         "New York, USA: 20 °C, Wind: 0 km/h")

    def test_missing_or_invalid_wind_keeps_temperature_visible(self):
        invalid = [
            {"current": {"temperature_2m": 20},
             "current_units": {"temperature_2m": "°C"}},
            {"current": {"temperature_2m": 20, "wind_speed_10m": "12"},
             "current_units": {"temperature_2m": "°C", "wind_speed_10m": "km/h"}},
            {"current": {"temperature_2m": 20, "wind_speed_10m": 12},
             "current_units": {"temperature_2m": "°C", "wind_speed_10m": "m/s"}},
        ]
        for data in invalid:
            with self.subTest(data=data):
                self.assertEqual(format_weather(self.place, data),
                                 "New York, USA: 20 °C, Wind nicht verfügbar")

    def test_invalid_temperature_rejects_success_output(self):
        for value in (None, "20", True, float("nan"), float("inf")):
            with self.subTest(value=value), self.assertRaises(WeatherError):
                format_weather(self.place, self.payload(value))

    def test_invalid_payload_or_temperature_unit(self):
        for data in (None, [], {}, {"current": []}, self.payload(unit="°F")):
            with self.subTest(data=data), self.assertRaises(WeatherError):
                format_weather(self.place, data)
