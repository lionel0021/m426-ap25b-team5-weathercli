import io
import unittest
from http.client import IncompleteRead
from unittest.mock import patch
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlparse

from weathercli.errors import WeatherError, request_json, unique_location


PLACE = {"name": "Zürich", "country": "Schweiz", "latitude": 47.37, "longitude": 8.55}


class ErrorTests(unittest.TestCase):
    def test_unique_location_returns_resolved_data(self):
        self.assertEqual(unique_location({"results": [PLACE]}), PLACE)

    def test_no_match_requires_more_precise_input(self):
        for data in ({}, {"results": []}):
            with self.subTest(data=data), self.assertRaisesRegex(WeatherError, "genauere Ortsangabe"):
                unique_location(data)

    def test_ambiguous_location_is_not_selected(self):
        with self.assertRaisesRegex(WeatherError, "mehrdeutig.*genauere Ortsangabe"):
            unique_location({"results": [PLACE, PLACE]})

    def test_malformed_location_is_rejected(self):
        for data in (None, [], {"results": None}, {"results": [None]},
                     {"results": [{**PLACE, "country": ""}]},
                     {"results": [{**PLACE, "latitude": 100}]},
                     {"results": [{**PLACE, "longitude": True}]}):
            with self.subTest(data=data), self.assertRaises(WeatherError):
                unique_location(data)

    def test_http_dns_timeout_and_incomplete_response(self):
        for error in (HTTPError("https://example.test", 503, "Unavailable", {}, None),
                      URLError("DNS"), TimeoutError(), IncompleteRead(b"{")):
            with self.subTest(error=error), patch("weathercli.errors.urlopen", side_effect=error):
                with self.assertRaisesRegex(WeatherError, "nicht erreichbar"):
                    request_json("https://example.test", {})

    def test_invalid_json_encoding_and_api_errors(self):
        for content in (b"invalid", b"\xff", b"[]", b'{"error":true}'):
            with self.subTest(content=content):
                with patch("weathercli.errors.urlopen", return_value=io.BytesIO(content)):
                    with self.assertRaises(WeatherError):
                        request_json("https://example.test", {})

    def test_encoded_request_with_timeout(self):
        with patch("weathercli.errors.urlopen", return_value=io.BytesIO(b'{"results":[]}')) as request:
            self.assertEqual(request_json("https://example.test", {"name": "Zürich"}), {"results": []})
            self.assertEqual(parse_qs(urlparse(request.call_args.args[0]).query)["name"], ["Zürich"])
            self.assertEqual(request.call_args.kwargs["timeout"], 10)
