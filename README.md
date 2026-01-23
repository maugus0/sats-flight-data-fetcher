# ✈️ Airlines Flight Data Fetcher

[![CI/CD Pipeline](https://github.com/maugus0/sats-flight-data-fetcher/actions/workflows/ci.yml/badge.svg)](https://github.com/maugus0/sats-flight-data-fetcher/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![API](https://img.shields.io/badge/API-AirLabs-orange.svg)
![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)

A simple, user-friendly Python tool to fetch flight data for any major airline. Perfect for data analysis, research, or operational tracking.

## 🎯 Features

- **15+ Airlines Supported** - Singapore Airlines, Emirates, Qatar Airways, British Airways, and more
- **Multiple Output Formats** - Excel (with summary), CSV, or JSON
- **Date Range Support** - Fetch single day or multiple days at once
- **Interactive Mode** - No command line knowledge needed
- **Progress Tracking** - Visual progress bar for multi-day fetches
- **Automatic Checkpoints** - Raw data saved for recovery
- **Summary Statistics** - On-time performance, delays, top routes

## 📋 Quick Start

### For Non-Technical Users

1. **Download** this project and extract it to a folder
2. **Install Python** from [python.org](https://python.org) (version 3.10+)
3. **Get an API Key** from [AirLabs](https://airlabs.co) (free tier available)
4. **Open Terminal/Command Prompt** in the project folder
5. **Run these commands:**

```bash
pip install -r requirements.txt
python fetch_flights.py
```

6. **Follow the prompts** - the script will guide you through selecting an airline and dates

### For Technical Users

```bash
# Clone and setup
git clone https://github.com/maugus0/sats-flight-data-fetcher.git
cd sats-flight-data-fetcher
pip install -r requirements.txt

# Add your API key
echo "AIRLABS_API_KEY=your_key_here" > .env

# Fetch yesterday's Singapore Airlines flights
python fetch_flights.py --airline SQ --yesterday

# Fetch date range for Emirates in CSV format
python fetch_flights.py --airline EK --start-date 2025-01-01 --end-date 2025-01-07 --format csv
```

## 🔑 API Key Setup

1. Go to [AirLabs.co](https://airlabs.co) and create a free account
2. Navigate to your Dashboard → API Key
3. Create a `.env` file in the project folder:

```
AIRLABS_API_KEY=your_actual_api_key_here
```

> **Free Tier:** 1,000 requests/month (1 request = 1 day of data)

## 📖 Usage Examples

### Interactive Mode (Easiest)

```bash
python fetch_flights.py
```

The script will ask you:
- Which airline? (type `list` to see all options)
- Start date?
- End date?
- Output format?

### Command Line Mode

```bash
# Fetch yesterday's flights
python fetch_flights.py --airline SQ --yesterday

# Fetch last week
python fetch_flights.py --airline EK --last-week

# Fetch last month
python fetch_flights.py --airline QR --last-month

# Fetch specific date range
python fetch_flights.py --airline BA --start-date 2025-01-01 --end-date 2025-01-31

# Output as CSV instead of Excel
python fetch_flights.py --airline LH --yesterday --format csv

# Output as JSON
python fetch_flights.py --airline AF --yesterday --format json

# List all available airlines
python fetch_flights.py --list-airlines
```

## ✈️ Supported Airlines

| Code | Airline | Country |
|------|---------|---------|
| SQ | Singapore Airlines | Singapore |
| EK | Emirates | UAE |
| QR | Qatar Airways | Qatar |
| BA | British Airways | UK |
| LH | Lufthansa | Germany |
| AF | Air France | France |
| AA | American Airlines | USA |
| UA | United Airlines | USA |
| DL | Delta Air Lines | USA |
| CX | Cathay Pacific | Hong Kong |
| NH | All Nippon Airways | Japan |
| JL | Japan Airlines | Japan |
| QF | Qantas | Australia |
| TK | Turkish Airlines | Turkey |
| KE | Korean Air | South Korea |

Run `python fetch_flights.py --list-airlines` for the full list.

## 📊 Output Files

### Excel Output (Default)

Creates a `.xlsx` file with two sheets:

**Sheet 1: Flight Data**
| Flight | From | To | Sched. Dep | Actual Dep | Sched. Arr | Actual Arr | Delay | Status |
|--------|------|----|-----------:|-----------:|------------|------------|------:|--------|
| SQ123 | SIN | LHR | 08:00 | 08:15 | 15:30 | 15:45 | 15 | landed |

**Sheet 2: Summary**
- Total flights
- Average delay (minutes)
- On-time percentage
- Top 10 routes
- Flights by status

### CSV Output

Simple flat file, easy to import into Excel or databases.

### JSON Output

Complete data with summary statistics, good for developers.

## 📁 Project Structure

```
sats-flight-data-fetcher/
├── .env                    # Your API key (create this)
├── .env.example            # API key template
├── .gitignore              # Files to ignore in git
├── README.md               # This file
├── CONTRIBUTING.md         # Contributor guidelines
├── requirements.txt        # Python dependencies
├── requirements-dev.txt    # Dev/test dependencies
├── airlines_config.json    # Airline definitions
├── fetch_flights.py        # Main script
├── pytest.ini              # Test configuration
├── tests/                  # Test suite
│   ├── conftest.py
│   ├── test_fetch_flights.py
│   └── test_config.py
├── .github/
│   └── workflows/
│       └── ci.yml          # CI/CD pipeline
└── outputs/                # Generated files (auto-created)
```

## ❓ FAQ

**Q: How many API calls do I need?**
A: 1 API call per day of data. A week needs 7 calls, a month needs ~30 calls.

**Q: Is the free tier enough?**
A: Yes! 1,000 requests/month = 33 days of data daily, or one full month for 30+ airlines.

**Q: Can I add more airlines?**
A: Yes! Edit `airlines_config.json` and add any airline with their IATA code.

**Q: What if I get rate limited?**
A: The script automatically waits and retries. If issues persist, wait a few minutes.

**Q: Where are my files saved?**
A: In the `outputs/` folder with timestamps (e.g., `SQ_2025-01-20_143052.xlsx`).

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| "API key not found" | Create `.env` file with `AIRLABS_API_KEY=your_key` |
| "Unknown airline" | Run `--list-airlines` to see valid codes |
| "Invalid date" | Use format `YYYY-MM-DD` (e.g., 2025-01-20) |
| "No flights found" | Check if airline operated on that date |
| Timeout errors | Check internet connection, retry in a few minutes |

## 🧪 Development

### Run Tests

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

### Code Quality

```bash
# Format code
black fetch_flights.py tests/
isort fetch_flights.py tests/

# Lint
flake8 fetch_flights.py tests/
```

## 📝 License

MIT License - feel free to use, modify, and distribute.

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

- Fork the repo
- Create a feature branch
- Run tests: `pytest tests/ -v`
- Submit a pull request

---

**Happy Flight Tracking! ✈️**
