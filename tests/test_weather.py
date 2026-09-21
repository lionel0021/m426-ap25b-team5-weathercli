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


class CliTests(unittest.TestCase):
    def run_cli(self, args, temperature=21.5, error=None):
        out, err = io.StringIO(), io.StringIO()
        with patch("weathercli.cli.resolve_city", return_value=PLACE, side_effect=error) as resolve:
            with patch("weathercli.cli.current_weather", return_value={"current": {"temperature_2m": temperature}, "current_units": {"temperature_2m": "°C"}}) as weather:
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
                self.assertEqual(out, f"Zürich, Schweiz: {value:g} °C\n")
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
                "current": {"temperature_2m": 18},
                "current_units": {"temperature_2m": "°C"},
            }) as weather:
                out = io.StringIO()
                with redirect_stdout(out):
                    self.assertEqual(main(["Zürich"]), 0)
                self.assertEqual(out.getvalue(), "Zürich, Schweiz: 18 °C\n")
                weather.assert_called_once_with(PLACE)

    def test_module_process_exit_code(self):
        result = subprocess.run([sys.executable, "-m", "weathercli"], capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, b"")
        self.assertIn(b"weather", result.stderr)


if __name__ == "__main__":
    unittest.main()
