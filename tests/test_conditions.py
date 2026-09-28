"""Tests für den Wetterzustand (WEA-19, WEA-20) mit gekürzten echten Open-Meteo-Antworten."""

import unittest

from weathercli.conditions import WMO_CONDITIONS, condition_from_response


def response(code, temperature=15.5):
    return {"current_units": {"temperature_2m": "°C", "weather_code": "wmo code"},
            "current": {"time": "2026-09-28T07:15", "temperature_2m": temperature,
                        "weather_code": code}}


class ConditionTests(unittest.TestCase):
    def test_known_codes_are_written_out_in_german(self):
        for code, expected in ((0, "Klar"), (2, "Teilweise bewölkt"), (51, "Leichter Sprühregen"),
                               (63, "Regen"), (75, "Starker Schneefall"), (95, "Gewitter")):
            with self.subTest(code=code):
                self.assertEqual(condition_from_response(response(code)), expected)

    def test_every_mapped_condition_is_a_word_not_a_number(self):
        for code, text in WMO_CONDITIONS.items():
            with self.subTest(code=code):
                self.assertTrue(text and not text.isdigit(), code)

    def test_unknown_or_missing_code_has_no_condition(self):
        broken = [response(4), response(123), response(None), response("63"), response(True),
                  response(2.5), response(float("nan")), {"current": {"temperature_2m": 15.5}},
                  {"current": []}, {}, None]
        for data in broken:
            with self.subTest(data=data):
                self.assertIsNone(condition_from_response(data))

    def test_temperature_stays_readable_without_condition(self):
        data = {"current": {"temperature_2m": 15.5}, "current_units": {"temperature_2m": "°C"}}
        self.assertIsNone(condition_from_response(data))
        self.assertEqual(data["current"]["temperature_2m"], 15.5)


if __name__ == "__main__":
    unittest.main()
