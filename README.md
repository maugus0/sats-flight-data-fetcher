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

### Excel Output (Default) ✨ **Two Sheets Included!**

Creates a `.xlsx` file with **two separate sheets**:

#### **Sheet 1: "Flight Data"** 📊
Contains all individual flight records with complete details:

| Flight | From | To | Sched. Dep | Actual Dep | Sched. Arr | Actual Arr | Delay (min) | Status |
|--------|------|----|-----------:|-----------:|------------|------------|------------:|--------|
| SQ123 | SIN | LHR | 08:00 | 08:15 | 15:30 | 15:45 | 15 | landed |
| SQ317 | SIN | LHR | 23:30 | 23:42 | 06:15 | 06:25 | 12 | landed |

**Features:**
- All flight records in one table
- Styled headers (blue background, white text)
- Auto-adjusted column widths
- Easy to filter, sort, and analyze

#### **Sheet 2: "Summary"** 📈
Contains aggregated statistics and insights:

**Key Metrics:**
- Total Flights
- Average Delay (minutes)
- On-Time Performance (%)
- Delayed Flights (≥15 min)
- Cancelled Flights

**Breakdowns:**
- **Flights by Status**: Count of flights by status (landed, scheduled, cancelled, etc.)
- **Top 10 Routes**: Most frequent routes with flight counts

**Features:**
- Formatted title with airline name
- Clear sections with bold labels
- Easy-to-read layout for reporting

### CSV Output

**Note:** CSV is a single flat file format - it does NOT support multiple sheets. If you need two sheets (flight data + summary), use Excel format instead.

**CSV contains:**
- All flight records in a simple comma-separated format
- Easy to import into Excel, databases, or other tools
- One row per flight with all details

**To get summary statistics with CSV:**
- Use JSON format which includes both flights and summary
- Or use Excel format (default) which has both sheets

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

# 🚀 How to Run the Flight Data Fetcher

## Prerequisites

1. **Python 3.11+** installed
2. **API Key** from [AirLabs.co](https://airlabs.co) (free tier available)
3. **Dependencies** installed

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `requests` - For API calls
- `python-dotenv` - For loading API key from .env file
- `openpyxl` - For Excel export
- `tqdm` - For progress bars

## Step 2: Set Up API Key

### Option A: Using .env file (Recommended)

1. Create a `.env` file in the project root:
   ```bash
   # Windows (PowerShell)
   echo "AIRLABS_API_KEY=your_actual_api_key_here" > .env
   
   # Linux/macOS
   echo "AIRLABS_API_KEY=your_actual_api_key_here" > .env
   ```

2. Replace `your_actual_api_key_here` with your actual AirLabs API key

### Option B: Enter when prompted

If no `.env` file exists, the script will prompt you to enter the API key.

## Step 3: Run the Script

### Method 1: Interactive Mode (Easiest) ⭐

Just run the script without any arguments:

```bash
python fetch_flights.py
```

The script will guide you through:
- Selecting an airline (type `list` to see all options)
- Entering start date (YYYY-MM-DD)
- Entering end date (or press Enter for same as start)
- Choosing output format (csv, excel, json)

**Example Interactive Session:**
```
==================================================
AIRLINES FLIGHT DATA FETCHER
Interactive Mode
==================================================

Enter airline IATA code (e.g., SQ, EK, BA)
Type 'list' to see all available airlines
Airline [SQ]: SQ

Enter start date (YYYY-MM-DD)
Start date [2026-01-22]: 2026-01-20

Enter end date (YYYY-MM-DD) [same as start]:
End date [2026-01-20]: 

Output format options: csv, excel, json
Format [excel]: excel
```

### Method 2: Command Line Mode

#### List Available Airlines

```bash
python fetch_flights.py --list-airlines
```

#### Fetch Yesterday's Flights

```bash
# Singapore Airlines (default)
python fetch_flights.py --yesterday

# Specific airline
python fetch_flights.py --airline SQ --yesterday
python fetch_flights.py --airline EK --yesterday
```

#### Fetch Last Week

```bash
python fetch_flights.py --airline SQ --last-week
```

#### Fetch Last Month

```bash
python fetch_flights.py --airline EK --last-month
```

#### Fetch Specific Date Range

```bash
# Single day
python fetch_flights.py --airline SQ --start-date 2026-01-20

# Date range
python fetch_flights.py --airline EK --start-date 2026-01-01 --end-date 2026-01-07
```

#### Choose Output Format

```bash
# CSV format
python fetch_flights.py --airline SQ --yesterday --format csv

# JSON format
python fetch_flights.py --airline EK --yesterday --format json

# Excel format (default)
python fetch_flights.py --airline QR --yesterday --format excel
```

## Complete Command Reference

```bash
# Basic usage
python fetch_flights.py [OPTIONS]

# Options:
  --airline, -a          Airline IATA code (e.g., SQ, EK, BA)
  --start-date, -s       Start date (YYYY-MM-DD)
  --end-date, -e         End date (YYYY-MM-DD)
  --yesterday            Fetch yesterday's flights
  --last-week            Fetch last 7 days
  --last-month           Fetch last 30 days
  --format, -f           Output format: csv, excel, json (default: excel)
  --list-airlines        List all available airlines
  --verbose, -v          Verbose output
  --help, -h             Show help message
```

## Example Commands

```bash
# Quick examples
python fetch_flights.py --airline SQ --yesterday
python fetch_flights.py --airline EK --start-date 2026-01-01 --end-date 2026-01-07
python fetch_flights.py --airline BA --last-week --format csv
python fetch_flights.py --list-airlines

# Interactive mode (no arguments)
python fetch_flights.py
```

## Output Files

All output files are saved in the `outputs/` folder:

- **Excel**: `AIRLINE_YYYY-MM-DD_HHMMSS.xlsx`
- **CSV**: `AIRLINE_YYYY-MM-DD_HHMMSS.csv`
- **JSON**: `AIRLINE_YYYY-MM-DD_HHMMSS.json`
- **Checkpoints**: `checkpoint_AIRLINE_DATE.json` (raw API responses)

## What Happens When You Run It

1. **Configuration Check**: Validates airline code and dates
2. **Confirmation**: Shows what will be fetched and asks for confirmation
3. **API Key**: Loads from `.env` or prompts for input
4. **Fetching**: Makes API calls with progress bar (1 second between calls)
5. **Processing**: Extracts and normalizes flight data
6. **Export**: Creates output file in chosen format
7. **Summary**: Displays statistics (total flights, delays, etc.)

## Troubleshooting

### "API key not found"
- Create `.env` file with `AIRLABS_API_KEY=your_key`
- Or enter key when prompted

### "Unknown airline"
- Run `python fetch_flights.py --list-airlines` to see valid codes
- Use IATA codes (e.g., SQ, EK, BA) not ICAO codes

### "Invalid date format"
- Use format: `YYYY-MM-DD` (e.g., 2026-01-20)
- Not: `01/20/2026` or `20-01-2026`

### "No flights found"
- Check if airline operated on that date
- Try a different date or airline

### Timeout errors
- Check internet connection
- Wait a few minutes and retry
- Script automatically retries up to 3 times

## Quick Start Checklist

- [ ] Python 3.11+ installed
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] API key obtained from [AirLabs.co](https://airlabs.co)
- [ ] `.env` file created with API key
- [ ] Run: `python fetch_flights.py --list-airlines` to verify setup
- [ ] Run: `python fetch_flights.py --airline SQ --yesterday` for a test

## Need Help?

- Check the [README.md](README.md) for more details
- See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup
- Review the script's help: `python fetch_flights.py --help`