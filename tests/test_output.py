import unittest
from weathercli.client import Location, WeatherError
from weathercli.output import format_weather


class OutputTests(unittest.TestCase):
    place = Location("New York", "USA", 40.7, -74.0)

    def payload(self, value=20, unit="°C", code=63, wind=12.4, wind_unit="km/h"):
        return {"current": {"temperature_2m": value, "weather_code": code,
                            "wind_speed_10m": wind},
                "current_units": {"temperature_2m": unit, "weather_code": "wmo code",
                                  "wind_speed_10m": wind_unit}}

    def test_temperature_including_zero_and_negative(self):
        for value in (0, 20.5, -8):
            with self.subTest(value=value):
                self.assertEqual(format_weather(self.place, self.payload(value)),
                                 f"New York, USA: {value:g} °C, Regen, Wind: 12.4 km/h")

    def test_condition_is_written_out_next_to_place_and_temperature(self):
        self.assertEqual(format_weather(self.place, self.payload(code=0)),
                         "New York, USA: 20 °C, Klar, Wind: 12.4 km/h")

    def test_missing_or_unknown_condition_keeps_temperature_visible(self):
        for code in (None, 4, "63"):
            with self.subTest(code=code):
                self.assertEqual(format_weather(self.place, self.payload(code=code)),
                                 "New York, USA: 20 °C, Wetterzustand nicht verfügbar, "
                                 "Wind: 12.4 km/h")

    def test_zero_wind_is_a_value_not_a_gap(self):
        self.assertEqual(format_weather(self.place, self.payload(wind=0)),
                         "New York, USA: 20 °C, Regen, Wind: 0 km/h")

    def test_missing_or_invalid_wind_keeps_the_other_values(self):
        for wind, unit in ((None, "km/h"), ("12", "km/h"), (True, "km/h"),
                           (float("nan"), "km/h"), (12.4, "mph"), (12.4, None)):
            with self.subTest(wind=wind, unit=unit):
                self.assertEqual(format_weather(self.place, self.payload(wind=wind, wind_unit=unit)),
                                 "New York, USA: 20 °C, Regen, Wind nicht verfügbar")

    def test_invalid_temperature_rejects_success_output(self):
        for value in (None, "20", True, float("nan"), float("inf")):
            with self.subTest(value=value), self.assertRaises(WeatherError):
                format_weather(self.place, self.payload(value))

    def test_invalid_payload_or_temperature_unit(self):
        for data in (None, [], {}, {"current": []}, self.payload(unit="°F")):
            with self.subTest(data=data), self.assertRaises(WeatherError):
                format_weather(self.place, data)
