#!/usr/bin/env python3

import argparse
import sys
import json
from urllib.request import urlopen, Request
from urllib.error import URLError
from urllib.parse import quote


def fetch_weather(location, format_type="j1"):
    encoded_location = quote(location)
    encoded_format = quote(format_type, safe="")
    url = f"https://wttr.in/{encoded_location}?format={encoded_format}"

    try:
        req = Request(url, headers={"User-Agent": "curl"})
        response = urlopen(req)
        data = response.read().decode("utf-8")
        return data
    except URLError as e:
        print(f"Error fetching weather: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Fetch and display weather from wttr.in API"
    )
    parser.add_argument(
        "location",
        nargs="?",
        default="",
        help="Location (city, zip code, or coordinates)",
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format: text or json",
    )
    parser.add_argument(
        "-c",
        "--current",
        action="store_true",
        help="Show only current weather conditions",
    )

    args = parser.parse_args()

    if args.format == "json":
        format_type = "j1"
    elif args.current:
        format_type = "%C+%t+%f+%w+%h"
    else:
        format_type = "%l+%C+%t+%f+%w+%h+%p+%m"

    weather_data = fetch_weather(args.location, format_type)

    if args.format == "json":
        data = json.loads(weather_data)
        print(json.dumps(data, indent=2))
    else:
        print(weather_data.replace("+", "\n"))


if __name__ == "__main__":
    main()
