#!/usr/bin/env python3
import argparse
import sys
from datetime import datetime

try:
    import requests
except ImportError:
    print("Error: requests library is required. Install it with: pip install requests")
    sys.exit(1)


def fetch_weather(city, units="metric"):
    base_url = "https://wttr.in"
    params = {
        "format": "j1",
    }
    
    try:
        response = requests.get(f"{base_url}/{city}", params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        sys.exit(1)


def display_weather(data, units="metric"):
    current = data["current_condition"][0]
    
    unit_symbol = "°C" if units == "metric" else "°F"
    speed_unit = "km/h" if units == "metric" else "mph"
    
    if units == "metric":
        temp_key = "temp_C"
        feels_like_key = "FeelsLikeC"
        windspeed_key = "windspeedKmph"
    else:
        temp_key = "temp_F"
        feels_like_key = "FeelsLikeF"
        windspeed_key = "windspeedMiles"
    
    print(f"\n{'='*50}")
    print(f"Weather for {data['nearest_area'][0]['areaName'][0]['value']}, {data['nearest_area'][0]['country'][0]['value']}")
    print(f"{'='*50}")
    print(f"Temperature: {current[temp_key]}{unit_symbol}")
    print(f"Feels Like: {current[feels_like_key]}{unit_symbol}")
    print(f"Condition: {current['weatherDesc'][0]['value']}")
    print(f"Humidity: {current['humidity']}%")
    print(f"Wind: {current[windspeed_key]} {speed_unit} {current['winddir16Point']}")
    print(f"Pressure: {current['pressure']} hPa")
    print(f"UV Index: {current['uvIndex']}")
    print(f"Visibility: {current['visibility']} km")
    print(f"Local Time: {current['observation_time']}")
    print(f"{'='*50}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Fetch and display weather information for a city",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s London
  %(prog)s "New York" --units imperial
  %(prog)s Tokyo --units metric
        """
    )
    
    parser.add_argument(
        "city",
        help="City name to fetch weather for"
    )
    
    parser.add_argument(
        "-u", "--units",
        choices=["metric", "imperial"],
        default="metric",
        help="Units for temperature (default: metric)"
    )
    
    args = parser.parse_args()
    
    print(f"Fetching weather for {args.city}...")
    weather_data = fetch_weather(args.city, args.units)
    display_weather(weather_data, args.units)


if __name__ == "__main__":
    main()
