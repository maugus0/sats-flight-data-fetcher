# ✈️ Airlines Flight Data Fetcher

[![CI/CD Pipeline](https://github.com/maugus0/sats-flight-data-fetcher/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/maugus0/sats-flight-data-fetcher/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
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
- **Automatic Checkpoints** - Raw JSON data saved for each day (recovery & backup)
- **Retry Logic** - Automatic retries with exponential backoff (up to 3 attempts)
- **Summary Statistics** - On-time performance, delays, top routes, status breakdown
- **CI/CD Pipeline** - Automated testing (94.84% coverage), formatting, and security checks
- **Pre-commit Hooks** - Catch issues before pushing to GitHub
- **59 Comprehensive Tests** - Full test suite covering all functionality

## 📋 Quick Start

### For Non-Technical Users

1. **Download** this project and extract it to a folder
2. **Install Python** from [python.org](https://python.org) (version 3.11 or higher)
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
- On-time percentage (< 15 min delay)
- Delayed flights (≥ 15 min)
- Cancelled flights
- Flights by status (landed, scheduled, cancelled, etc.)
- Top 10 routes

### CSV Output

Simple flat file with all flight data, easy to import into Excel or databases.

### JSON Output

Complete data structure with:
- `flights`: Array of all flight records
- `summary`: Statistics object with all metrics

### Checkpoint Files

Raw JSON responses are automatically saved as `checkpoint_AIRLINE_DATE.json` in the `outputs/` folder. These can be used for:
- Data recovery if export fails
- Re-processing data without API calls
- Debugging API responses

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
├── .flake8                  # Flake8 linting config
├── .coveragerc              # Coverage reporting config
├── .pre-commit-config.yaml  # Pre-commit hooks config
├── pre-commit-check.ps1    # Pre-commit checks (Windows)
├── pre-commit-check.sh     # Pre-commit checks (Linux/macOS)
├── fix-formatting.ps1      # Auto-fix formatting (Windows)
├── fix-formatting.sh       # Auto-fix formatting (Linux/macOS)
├── tests/                  # Test suite (59 tests)
│   ├── __init__.py
│   ├── conftest.py         # Pytest fixtures
│   ├── test_fetch_flights.py  # Main test file
│   └── test_config.py      # Config validation tests
├── .github/
│   ├── workflows/
│   │   └── ci.yml          # CI/CD pipeline
│   ├── ISSUE_TEMPLATE/     # Issue templates
│   └── PULL_REQUEST_TEMPLATE.md
└── outputs/                # Generated files (auto-created)
```

## ❓ FAQ

**Q: How many API calls do I need?**
A: 1 API call per day of data. A week needs 7 calls, a month needs ~30 calls.

**Q: Is the free tier enough?**
A: Yes! 1,000 requests/month = 33 days of data daily, or one full month for 30+ airlines.

**Q: Can I add more airlines?**
A: Yes! Edit `airlines_config.json` and add any airline with their IATA code.

**Q: What if I get rate limited or timeout?**
A: The script automatically retries up to 3 times with exponential backoff. Rate limits are handled gracefully with automatic waiting.

**Q: Where are my files saved?**
A: In the `outputs/` folder with timestamps (e.g., `SQ_2025-01-20_143052.xlsx`). Checkpoint files (raw JSON) are also saved as `checkpoint_AIRLINE_DATE.json` for data recovery.

**Q: My CI/CD pipeline failed. What should I do?**
A: Run `.\pre-commit-check.ps1` (or `./pre-commit-check.sh`) locally to see the same errors. Fix them with `.\fix-formatting.ps1` if needed, then commit and push again.

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| "API key not found" | Create `.env` file with `AIRLABS_API_KEY=your_key` |
| "Unknown airline" | Run `--list-airlines` to see valid codes |
| "Invalid date" | Use format `YYYY-MM-DD` (e.g., 2025-01-20) |
| "No flights found" | Check if airline operated on that date |
| Timeout errors | Check internet connection, retry in a few minutes |
| CI/CD badge shows "no status" | The workflow needs to complete at least once. Push your code, wait for the workflow to finish, then the badge will update. Check the [Actions tab](https://github.com/maugus0/sats-flight-data-fetcher/actions) |

## 🚀 CI/CD Pipeline

This project includes a complete CI/CD pipeline that runs automatically on every push and pull request:

- **Code Formatting** - Ensures consistent code style with Black
- **Linting** - Catches code quality issues with flake8 and pylint
- **Unit Tests** - Runs comprehensive test suite (59 tests) with 94.84% code coverage
- **Security Scanning** - Checks for vulnerabilities with Bandit and Safety
- **Config Validation** - Validates JSON configs and requirements files
- **Integration Tests** - Verifies script imports and CLI commands work

View the pipeline status in the badge at the top of this README, or check the [Actions tab](https://github.com/maugus0/sats-flight-data-fetcher/actions) on GitHub.

## 🧪 Development

### Run Tests

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run all tests (59 tests)
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=fetch_flights --cov-report=html --cov-report=term

# Check coverage threshold (must be >= 70%)
coverage report --fail-under=70
```

**Current Test Coverage: 94.84%** ✅

### Code Quality

```bash
# Format code (Black)
python -m black fetch_flights.py tests/

# Sort imports (isort with Black profile)
python -m isort --profile=black --line-length=120 fetch_flights.py tests/

# Lint (flake8)
python -m flake8 fetch_flights.py tests/ --max-line-length=120 --extend-ignore=E203,W503

# Code quality (pylint)
pylint fetch_flights.py --max-line-length=120 --disable=C0111,R0903,W0212,C0103
```

### Pre-commit Checks

**Always run pre-commit checks before pushing to GitHub!** This prevents CI/CD pipeline failures.

#### Run Pre-commit Checks

**Windows (PowerShell):**
```powershell
.\pre-commit-check.ps1
```

**Linux/macOS:**
```bash
chmod +x pre-commit-check.sh
./pre-commit-check.sh
```

The script checks:
- ✅ Code formatting (Black)
- ✅ Import sorting (isort)
- ✅ Linting (flake8)
- ✅ Python syntax validation
- ✅ JSON config validation
- ✅ Security (no hardcoded API keys)

#### Auto-fix Formatting Issues

If formatting issues are found, auto-fix them:

**Windows:**
```powershell
.\fix-formatting.ps1
```

**Linux/macOS:**
```bash
chmod +x fix-formatting.sh
./fix-formatting.sh
```

Then run the pre-commit check again to verify everything passes.

#### Workflow

```bash
# 1. Make your changes
# 2. Run pre-commit check
.\pre-commit-check.ps1  # or ./pre-commit-check.sh

# 3. If issues found, auto-fix
.\fix-formatting.ps1  # or ./fix-formatting.sh

# 4. Run check again to verify
.\pre-commit-check.ps1

# 5. Commit and push
git add .
git commit -m "your message"
git push
```

> **Tip:** Add these scripts to your git workflow to catch issues early and keep your CI/CD pipeline green! 🟢

## 📝 License

MIT License - feel free to use, modify, and distribute.

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Quick Contribution Guide

1. **Fork the repo** and clone your fork
2. **Create a feature branch**: `git checkout -b feature/your-feature`
3. **Install dev dependencies**: `pip install -r requirements-dev.txt`
4. **Make your changes**
5. **Run pre-commit checks**: `.\pre-commit-check.ps1` (or `./pre-commit-check.sh`)
6. **Run tests**: `pytest tests/ -v`
7. **Commit and push**: `git push origin feature/your-feature`
8. **Create a Pull Request**

> **Important:** All PRs must pass pre-commit checks and tests. The CI/CD pipeline will verify this automatically.

---

**Happy Flight Tracking! ✈️**
