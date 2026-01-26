# Weather CLI

A Python command-line tool that fetches weather from the wttr.in API and displays it.

## Usage

```bash
python3 weather_cli.py [location] [options]
```

### Examples

Get weather for a specific location:
```bash
python3 weather_cli.py "New York"
```

Get weather in JSON format:
```bash
python3 weather_cli.py "London" -f json
```

Show only current weather conditions:
```bash
python3 weather_cli.py "Tokyo" -c
```

Use default location (detected by IP):
```bash
python3 weather_cli.py
```

### Options

- `location` - Location (city, zip code, or coordinates). Optional - will use IP-based detection if not provided.
- `-f, --format` - Output format: `text` or `json` (default: text)
- `-c, --current` - Show only current weather conditions (reduces output)
- `-h, --help` - Show help message

## Requirements

- Python 3.6+
- No external dependencies required (uses standard library only)
