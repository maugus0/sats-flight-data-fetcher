# Contributing to Airlines Flight Fetcher

Thank you for your interest in contributing! This guide will help you get started.

## 🚀 Quick Start

### 1. Fork and Clone

```bash
# Fork the repo on GitHub, then:
git clone https://github.com/maugus0/sats-flight-data-fetcher.git
cd sats-flight-data-fetcher
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 3. Install Pre-commit Hooks

```bash
# Install pre-commit hooks (auto-formatting before commits)
pre-commit install

# Test it works
pre-commit run --all-files
```

## 🧪 Running Tests

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Test File

```bash
pytest tests/test_fetch_flights.py -v
```

### Run with Coverage

```bash
pytest tests/ --cov=. --cov-report=html

# View coverage report
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
xdg-open htmlcov/index.html  # Linux
```

## 📝 Code Style

We use automated formatting tools:

- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting

### Auto-format Your Code

```bash
# Format code
black fetch_flights.py tests/

# Sort imports
isort fetch_flights.py tests/

# Check linting
flake8 fetch_flights.py tests/
```

**Good news:** Pre-commit hooks will auto-format on every commit! 🎉

## 🔒 Security

### Before Committing

- Never commit API keys or secrets
- Check for hardcoded credentials
- Run security scan:

```bash
bandit -r fetch_flights.py
```

## 📋 Pull Request Process

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Your Changes

- Write clear, commented code
- Add tests for new functionality
- Update documentation if needed

### 3. Test Your Changes

```bash
# Run all tests
pytest tests/ -v

# Check formatting
black --check fetch_flights.py tests/
isort --check-only fetch_flights.py tests/
flake8 fetch_flights.py tests/

# Or just commit - pre-commit will check everything!
```

### 4. Commit Your Changes

```bash
git add .
git commit -m "feat: add support for multiple date formats"

# Pre-commit hooks will run automatically
```

### 5. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## 📐 Commit Message Format

Use conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Adding tests
- `refactor:` Code refactoring
- `style:` Formatting changes
- `chore:` Maintenance tasks

Examples:
```
feat: add Excel export with summary sheet
fix: handle API timeout errors gracefully
docs: update installation instructions
test: add tests for date range validation
```

## 🐛 Reporting Bugs

Open an issue with:

1. **Description** of the bug
2. **Steps to reproduce**
3. **Expected behavior**
4. **Actual behavior**
5. **System info** (OS, Python version)
6. **Log files** if available

## 💡 Suggesting Features

Open an issue with:

1. **Use case** - What problem does it solve?
2. **Proposed solution**
3. **Alternatives considered**
4. **Additional context**

## ❓ Questions?

- Check existing issues
- Read the main [README.md](README.md)
- Open a discussion on GitHub

## 📜 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow

## ✅ Checklist Before Submitting PR

- [ ] Code follows project style (Black, isort, flake8)
- [ ] All tests pass locally
- [ ] Added tests for new functionality
- [ ] Updated documentation if needed
- [ ] Commit messages follow conventional format
- [ ] No secrets or API keys in code
- [ ] Pre-commit hooks are passing

## 🎯 Development Tips

### Testing with Mock Data

Always use mock data in tests - no real API calls:

```python
@patch('requests.get')
def test_my_function(mock_get):
    mock_get.return_value.json.return_value = {"response": []}
    # Your test here
```

### Adding New Airlines

Edit `airlines_config.json`:

```json
{
  "airlines": {
    "XX": {
      "name": "Example Airlines",
      "iata": "XX",
      "icao": "EXA",
      "country": "Example Country"
    }
  }
}
```

### Debugging

Use verbose logging:

```bash
python fetch_flights.py --verbose
```

## 🙏 Thank You!

Your contributions make this project better for everyone!

