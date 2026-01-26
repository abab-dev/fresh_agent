# Weather CLI

A Python command-line interface to fetch and display weather information.

## Features

- Get current weather for any city
- Support for metric and imperial units
- Displays temperature, feels like, condition, humidity, wind, pressure, and more
- Two API options available

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make the script executable (optional):
```bash
chmod +x weather_cli.py
```

## Usage

### Option 1: wttr.in API (Free, No API Key Required)

```bash
python weather_cli.py <city> [options]
```

**Examples:**
```bash
python weather_cli.py London
python weather_cli.py "New York" --units imperial
python weather_cli.py Tokyo --units metric
```

**Note:** wttr.in is a free public service that may occasionally experience:
- Connection timeouts
- Rate limiting
- Temporary outages

If you encounter connection errors, try again later or use the OpenWeatherMap version.

### Option 2: OpenWeatherMap API (More Reliable, Requires Free API Key)

```bash
python weather_cli_openweathermap.py <city> [options]
```

**Get API Key:**
1. Sign up at https://openweathermap.org/api
2. Get your free API key
3. Set it as environment variable OR pass it as argument

**Examples:**
```bash
# Using environment variable
export OPENWEATHER_API_KEY='your_api_key_here'
python weather_cli_openweathermap.py London

# Passing API key directly
python weather_cli_openweathermap.py "New York" --units imperial --api-key YOUR_API_KEY

# Using both options
python weather_cli_openweathermap.py Tokyo --units metric
```

### Options

**Common Options:**
- `city`: City name to fetch weather for (required)
- `-u, --units`: Units for temperature - choices: `metric`, `imperial` (default: metric)
- `-h, --help`: Show help message

**OpenWeatherMap Only:**
- `-k, --api-key`: OpenWeatherMap API key (or set OPENWEATHER_API_KEY env var)

## Troubleshooting

### Connection Reset / Timeout Errors

If you see errors like:
- `[Errno 104] Connection reset by peer`
- `HTTPSConnectionPool: Max retries exceeded`
- `Connection timeout`

**Try these solutions:**

1. **Wait and retry** - The wttr.in API is free and can be overloaded
2. **Switch to OpenWeatherMap** - Get a free API key and use `weather_cli_openweathermap.py`
3. **Check your network** - Ensure you have internet access and no firewall is blocking the connection

### Dependencies

If you get an error about the requests library:
```bash
pip install requests
```

## Requirements

- Python 3.7+
- requests library

## API Information

- **wttr.in**: Free public weather service, no API key required
- **OpenWeatherMap**: More reliable, requires free API key signup
