#!/usr/bin/env python3
import argparse
import os
import sys

try:
    import requests
except ImportError:
    print("Error: requests library is required. Install it with: pip install requests")
    sys.exit(1)


def fetch_weather_openweathermap(city, units="metric", api_key=None):
    if not api_key:
        api_key = os.environ.get("OPENWEATHER_API_KEY")
    
    if not api_key:
        print("Error: OpenWeatherMap API key is required.")
        print("\nGet a free API key at: https://openweathermap.org/api")
        print("Set it as an environment variable:")
        print("  export OPENWEATHER_API_KEY='your_api_key_here'")
        print("\nOr pass it with --api-key option")
        sys.exit(1)
    
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": units
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        sys.exit(1)


def display_weather_openweathermap(data):
    unit_symbol = "°C" if data["units"] == "metric" else "°F"
    speed_unit = "m/s" if data["units"] == "metric" else "mph"
    
    print(f"\n{'='*50}")
    print(f"Weather for {data['name']}, {data['sys']['country']}")
    print(f"{'='*50}")
    print(f"Temperature: {data['main']['temp']}{unit_symbol}")
    print(f"Feels Like: {data['main']['feels_like']}{unit_symbol}")
    print(f"Condition: {data['weather'][0]['description'].title()}")
    print(f"Humidity: {data['main']['humidity']}%")
    print(f"Wind: {data['wind']['speed']} {speed_unit}")
    if 'deg' in data['wind']:
        print(f"Wind Direction: {data['wind']['deg']}°")
    print(f"Pressure: {data['main']['pressure']} hPa")
    print(f"Visibility: {data.get('visibility', 'N/A')/1000:.1f} km" if 'visibility' in data else f"Visibility: N/A")
    print(f"Cloudiness: {data['clouds']['all']}%")
    print(f"{'='*50}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Fetch and display weather information using OpenWeatherMap API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s London
  %(prog)s "New York" --units imperial
  %(prog)s Tokyo --units metric --api-key YOUR_API_KEY

Get a free API key at: https://openweathermap.org/api
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
    
    parser.add_argument(
        "-k", "--api-key",
        help="OpenWeatherMap API key (or set OPENWEATHER_API_KEY env var)"
    )
    
    args = parser.parse_args()
    
    print(f"Fetching weather for {args.city}...")
    weather_data = fetch_weather_openweathermap(args.city, args.units, args.api_key)
    weather_data["units"] = args.units  # Add units to data for display function
    display_weather_openweathermap(weather_data)


if __name__ == "__main__":
    main()
