import unittest
from weathercli.client import Location, WeatherError
from weathercli.output import format_tomorrow, format_weather


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


class TomorrowOutputTests(unittest.TestCase):
    """WEA-33: die drei Fälle aus der Tabelle in doc/sprint-3.md."""

    place = Location("Zürich", "Schweiz", 47.37, 8.55)

    def payload(self, code=45, minimum=7.7, maximum=16.8, unit="°C"):
        return {"daily_units": {"weather_code": "wmo code", "temperature_2m_max": unit,
                                "temperature_2m_min": unit},
                "daily": {"time": ["2026-10-26", "2026-10-27"], "weather_code": [3, code],
                          "temperature_2m_max": [11.7, maximum],
                          "temperature_2m_min": [2.2, minimum]}}

    def only_today(self):
        data = self.payload()
        for key in ("time", "weather_code", "temperature_2m_max", "temperature_2m_min"):
            data["daily"][key] = data["daily"][key][:1]
        return data

    def test_condition_and_temperature_range_for_tomorrow(self):
        self.assertEqual(format_tomorrow(self.place, self.payload()),
                         "Zürich, Schweiz, morgen: Nebel, 7.7 bis 16.8 °C")

    def test_today_is_not_used(self):
        """Heute ist Index 0 mit Code 3 und 2.2/11.7 °C und darf nicht erscheinen."""
        output = format_tomorrow(self.place, self.payload())
        self.assertNotIn("Bewölkt", output)
        self.assertNotIn("11.7", output)
        self.assertNotIn("2.2", output)

    def test_zero_and_negative_values_are_shown(self):
        for minimum, maximum, expected in ((0, 2.5, "0 bis 2.5 °C"),
                                           (-4, -0.5, "-4 bis -0.5 °C")):
            with self.subTest(minimum=minimum):
                self.assertEqual(format_tomorrow(self.place, self.payload(minimum=minimum,
                                                                         maximum=maximum)),
                                 f"Zürich, Schweiz, morgen: Nebel, {expected}")

    def test_missing_or_unknown_code_keeps_the_range(self):
        missing_code = self.payload()
        del missing_code["daily"]["weather_code"]
        short_code = self.payload()
        short_code["daily"]["weather_code"] = [3]
        for data in (self.payload(code=None), self.payload(code=4), self.payload(code="45"),
                     self.payload(code=True), missing_code, short_code):
            with self.subTest(data=data["daily"].get("weather_code")):
                self.assertEqual(format_tomorrow(self.place, data),
                                 "Zürich, Schweiz, morgen: Wetterzustand nicht verfügbar, "
                                 "7.7 bis 16.8 °C")

    def test_missing_invalid_or_incomplete_values_report_no_forecast(self):
        no_units = self.payload()
        del no_units["daily_units"]
        for data in (self.payload(minimum=None), self.payload(maximum=None),
                     self.payload(minimum="7.7"), self.payload(maximum=float("nan")),
                     self.payload(minimum=float("inf")), self.payload(maximum=True),
                     self.payload(unit="°F"), self.payload(unit=None),
                     self.only_today(), no_units,
                     {"daily": {}}, {"daily": []}, {}, [], None):
            with self.subTest(data=data):
                self.assertEqual(format_tomorrow(self.place, data),
                                 "Zürich, Schweiz, morgen: Vorhersage nicht verfügbar")
