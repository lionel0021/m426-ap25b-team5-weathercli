"""Ein Aufruf, eine Stadt, eine aktuelle Temperatur."""

import argparse
import sys

from .client import WeatherError, current_weather, resolve_city
from .output import format_weather


class WeatherParser(argparse.ArgumentParser):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._positionals.title = "Argumente"
        self._optionals.title = "Optionen"

    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(2, f'Fehler: {message}\nBeispiel: weather "Zürich". Hilfe: weather --help\n')


def allow_unmappable_characters():
    """Ortsnamen sollen die Ausgabe nicht abbrechen lassen.

    Kennt die Konsole oder die Zieldatei einer Umleitung ein Zeichen nicht
    (unter Windows z. B. das Ł von Łódź in cp1252), wird es ersetzt statt einen
    UnicodeEncodeError auszuloesen.
    """
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(errors="replace")


def main(argv=None):
    allow_unmappable_characters()
    parser = WeatherParser(
        prog="weather", usage='weather "STADT"', add_help=False,
        description="Zeigt die aktuelle Temperatur einer Stadt.",
        epilog='Beispiele: weather "Zürich" | weather "New York"',
    )
    parser.add_argument("-h", "--help", action="help", help="Hilfe anzeigen und beenden")
    parser.add_argument("city", nargs="*", metavar="STADT", help="genau eine Stadt")
    args = parser.parse_args(argv)
    if not args.city or (len(args.city) == 1 and not args.city[0].strip()):
        parser.error("Die Stadt fehlt.")
    if len(args.city) != 1:
        parser.error("Genau eine Stadt angeben; mehrteilige Namen in Anführungszeichen setzen.")
    try:
        location = resolve_city(args.city[0].strip())
        result = format_weather(location, current_weather(location))
    except WeatherError as error:
        print(f"Fehler: {error}", file=sys.stderr)
        return 1
    print(result)
    return 0
