"""Tests für Lionels CLI; Nicos API wird an der Schnittstelle simuliert."""

import io
import subprocess
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import patch

from weathercli.cli import main
from weathercli.client import Location, WeatherError


PLACE = Location("Zürich", "Schweiz", 47.37, 8.55)
TOMORROW = {"daily_units": {"weather_code": "wmo code", "temperature_2m_max": "°C",
                            "temperature_2m_min": "°C"},
            "daily": {"time": ["2026-10-26", "2026-10-27"], "weather_code": [3, 45],
                      "temperature_2m_max": [11.7, 16.8], "temperature_2m_min": [6.8, 7.7]}}


class CliTests(unittest.TestCase):
    def run_cli(self, args, temperature=21.5, error=None):
        out, err = io.StringIO(), io.StringIO()
        with patch("weathercli.cli.resolve_city", return_value=PLACE, side_effect=error) as resolve:
            with patch("weathercli.cli.current_weather", return_value={"current": {"temperature_2m": temperature, "weather_code": 3, "wind_speed_10m": 9}, "current_units": {"temperature_2m": "°C", "weather_code": "wmo code", "wind_speed_10m": "km/h"}}) as weather:
                with redirect_stdout(out), redirect_stderr(err):
                    try:
                        code = main(args)
                    except SystemExit as result:
                        code = result.code
        return code, out.getvalue(), err.getvalue(), resolve, weather

    def test_formats_place_country_and_temperature(self):
        for value in [21.5, 0, -7.2]:
            with self.subTest(value=value):
                code, out, err, resolve, weather = self.run_cli([" Zürich "], value)
                self.assertEqual(code, 0)
                self.assertEqual(out, f"Zürich, Schweiz: {value:g} °C, Bewölkt, Wind: 9 km/h\n")
                self.assertEqual(err, "")
                resolve.assert_called_once_with("Zürich")
                weather.assert_called_once_with(PLACE)

    def test_missing_city_and_unquoted_words(self):
        for args, message in [([], "Stadt fehlt"), (["  "], "Stadt fehlt"),
                              (["New", "York"], "Anführungszeichen")]:
            with self.subTest(args=args):
                code, out, err, resolve, weather = self.run_cli(args)
                self.assertEqual(code, 2)
                self.assertIn(message, err)
                self.assertIn('weather "Zürich"', err)
                self.assertEqual(out, "")
                resolve.assert_not_called()
                weather.assert_not_called()

    def test_service_error_is_displayed_without_temperature(self):
        code, out, err, _, weather = self.run_cli(["Zürich"], error=WeatherError("Testfehler"))
        self.assertEqual(code, 1)
        self.assertEqual(out, "")
        self.assertIn("Testfehler", err)
        weather.assert_not_called()

    def test_temperature_error_is_displayed(self):
        with patch("weathercli.cli.current_weather", side_effect=WeatherError("Keine Temperatur")):
            with patch("weathercli.cli.resolve_city", return_value=PLACE):
                out, err = io.StringIO(), io.StringIO()
                with redirect_stdout(out), redirect_stderr(err):
                    self.assertEqual(main(["Zürich"]), 1)
                self.assertEqual(out.getvalue(), "")
                self.assertIn("Keine Temperatur", err.getvalue())

    def test_help_does_not_call_service(self):
        code, out, err, resolve, weather = self.run_cli(["--help"])
        self.assertEqual(code, 0)
        self.assertIn("New York", out)
        self.assertEqual(err, "")
        resolve.assert_not_called()
        weather.assert_not_called()

    def test_multiword_city_is_passed_whole_and_trimmed(self):
        for city in ["New York", "  New York  "]:
            with self.subTest(city=city):
                code, _, _, resolve, _ = self.run_cli([city])
                self.assertEqual(code, 0)
                resolve.assert_called_once_with("New York")

    def test_unknown_option_names_option_and_help_without_request(self):
        code, out, err, resolve, weather = self.run_cli(["--unbekannt"])
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertIn("--unbekannt", err)
        self.assertIn("weather --help", err)
        resolve.assert_not_called()
        weather.assert_not_called()

    def test_help_process_without_network(self):
        result = subprocess.run([sys.executable, "-m", "weathercli", "--help"], capture_output=True)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stderr, b"")
        self.assertIn(b'weather "STADT"', result.stdout)
        self.assertIn(b'New York', result.stdout)

    def test_temperature_uses_single_weather_response(self):
        with patch("weathercli.cli.resolve_city", return_value=PLACE):
            with patch("weathercli.cli.current_weather", return_value={
                "current": {"temperature_2m": 18, "weather_code": 61, "wind_speed_10m": 0},
                "current_units": {"temperature_2m": "°C", "weather_code": "wmo code",
                                  "wind_speed_10m": "km/h"},
            }) as weather:
                out = io.StringIO()
                with redirect_stdout(out):
                    self.assertEqual(main(["Zürich"]), 0)
                self.assertEqual(out.getvalue(),
                                 "Zürich, Schweiz: 18 °C, Leichter Regen, Wind: 0 km/h\n")
                weather.assert_called_once_with(PLACE)

    def test_output_survives_characters_the_target_cannot_encode(self):
        lodz = Location("Łódź", "Polen", 51.77, 19.46)
        stream = io.TextIOWrapper(io.BytesIO(), encoding="cp1252")
        with patch("weathercli.cli.resolve_city", return_value=lodz):
            with patch("weathercli.cli.current_weather", return_value={
                "current": {"temperature_2m": 11},
                "current_units": {"temperature_2m": "°C"},
            }):
                with redirect_stdout(stream):
                    self.assertEqual(main(["Łódź"]), 0)
                stream.flush()
        self.assertIn(b"Polen: 11 ", stream.buffer.getvalue())

    def run_tomorrow(self, args, data=TOMORROW):
        out, err = io.StringIO(), io.StringIO()
        with patch("weathercli.cli.resolve_city", return_value=PLACE):
            with patch("weathercli.cli.tomorrow_forecast", return_value=data) as forecast:
                with patch("weathercli.cli.current_weather") as current:
                    with redirect_stdout(out), redirect_stderr(err):
                        try:
                            code = main(args)
                        except SystemExit as result:
                            code = result.code
        return code, out.getvalue(), err.getvalue(), forecast, current

    def test_morgen_shows_condition_and_range_without_current_weather(self):
        for args in (["Zürich", "--morgen"], ["--morgen", "Zürich"]):
            with self.subTest(args=args):
                code, out, err, forecast, current = self.run_tomorrow(args)
                self.assertEqual(code, 0)
                self.assertEqual(out, "Zürich, Schweiz, morgen: Nebel, 7.7 bis 16.8 °C\n")
                self.assertEqual(err, "")
                forecast.assert_called_once_with(PLACE)
                current.assert_not_called()

    def test_missing_forecast_is_no_crash_and_exit_zero(self):
        code, out, err, _, _ = self.run_tomorrow(["Zürich", "--morgen"], {"daily": {}})
        self.assertEqual(code, 0)
        self.assertEqual(out, "Zürich, Schweiz, morgen: Vorhersage nicht verfügbar\n")
        self.assertEqual(err, "")

    def test_without_morgen_the_output_stays_unchanged(self):
        with patch("weathercli.cli.tomorrow_forecast") as forecast:
            code, out, _, _, weather = self.run_cli(["Zürich"])
        self.assertEqual(code, 0)
        self.assertEqual(out, "Zürich, Schweiz: 21.5 °C, Bewölkt, Wind: 9 km/h\n")
        forecast.assert_not_called()
        weather.assert_called_once_with(PLACE)

    def test_morgen_without_city_is_an_input_error(self):
        code, out, err, forecast, current = self.run_tomorrow(["--morgen"])
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertIn("Stadt fehlt", err)
        forecast.assert_not_called()
        current.assert_not_called()

    def test_help_names_the_morgen_option_with_an_example(self):
        code, out, _, _, _ = self.run_tomorrow(["--help"])
        self.assertEqual(code, 0)
        self.assertIn("--morgen", out)
        self.assertIn('weather "Zürich" --morgen', out)

    def test_service_error_with_morgen_is_displayed(self):
        with patch("weathercli.cli.resolve_city", return_value=PLACE):
            with patch("weathercli.cli.tomorrow_forecast",
                       side_effect=WeatherError("Wetterdienst nicht erreichbar")):
                out, err = io.StringIO(), io.StringIO()
                with redirect_stdout(out), redirect_stderr(err):
                    self.assertEqual(main(["Zürich", "--morgen"]), 1)
                self.assertEqual(out.getvalue(), "")
                self.assertIn("nicht erreichbar", err.getvalue())

    def test_module_process_exit_code(self):
        result = subprocess.run([sys.executable, "-m", "weathercli"], capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, b"")
        self.assertIn(b"weather", result.stderr)


if __name__ == "__main__":
    unittest.main()
