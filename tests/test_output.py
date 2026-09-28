import unittest
from weathercli.client import Location, WeatherError
from weathercli.output import format_weather


class OutputTests(unittest.TestCase):
    place = Location("New York", "USA", 40.7, -74.0)

    def payload(self, value=20, unit="°C", code=63):
        return {"current": {"temperature_2m": value, "weather_code": code},
                "current_units": {"temperature_2m": unit, "weather_code": "wmo code"}}

    def test_temperature_including_zero_and_negative(self):
        for value in (0, 20.5, -8):
            with self.subTest(value=value):
                self.assertEqual(format_weather(self.place, self.payload(value)),
                                 f"New York, USA: {value:g} °C, Regen")

    def test_condition_is_written_out_next_to_place_and_temperature(self):
        self.assertEqual(format_weather(self.place, self.payload(code=0)),
                         "New York, USA: 20 °C, Klar")

    def test_missing_or_unknown_condition_keeps_temperature_visible(self):
        for code in (None, 4, "63"):
            with self.subTest(code=code):
                self.assertEqual(format_weather(self.place, self.payload(code=code)),
                                 "New York, USA: 20 °C, Wetterzustand nicht verfügbar")

    def test_invalid_temperature_rejects_success_output(self):
        for value in (None, "20", True, float("nan"), float("inf")):
            with self.subTest(value=value), self.assertRaises(WeatherError):
                format_weather(self.place, self.payload(value))

    def test_invalid_payload_or_temperature_unit(self):
        for data in (None, [], {}, {"current": []}, self.payload(unit="°F")):
            with self.subTest(data=data), self.assertRaises(WeatherError):
                format_weather(self.place, data)
