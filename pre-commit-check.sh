#!/bin/bash
# Pre-commit check script
# Run this before committing to catch issues early

set -e  # Exit on error

echo "🔍 Running pre-commit checks..."
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "fetch_flights.py" ]; then
    echo -e "${RED}❌ Error: fetch_flights.py not found. Run this script from the project root.${NC}"
    exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check dependencies
echo "📦 Checking dependencies..."
MISSING_DEPS=0

if ! command_exists black; then
    echo -e "${YELLOW}⚠️  black not found. Install with: pip install black${NC}"
    MISSING_DEPS=1
fi

if ! command_exists isort; then
    echo -e "${YELLOW}⚠️  isort not found. Install with: pip install isort${NC}"
    MISSING_DEPS=1
fi

if ! command_exists flake8; then
    echo -e "${YELLOW}⚠️  flake8 not found. Install with: pip install flake8${NC}"
    MISSING_DEPS=1
fi

if [ $MISSING_DEPS -eq 1 ]; then
    echo -e "${RED}❌ Missing dependencies. Install with: pip install -r requirements-dev.txt${NC}"
    exit 1
fi

echo -e "${GREEN}✅ All dependencies found${NC}"
echo ""

# Track failures
FAILED=0

# 1. Black formatting check
echo "1️⃣  Checking code formatting (Black)..."
if python -m black --check --diff *.py tests/*.py 2>&1; then
    echo -e "${GREEN}✅ Code formatting is correct${NC}"
else
    echo -e "${RED}❌ Code formatting failed${NC}"
    echo -e "${YELLOW}💡 Fix with: python -m black *.py tests/*.py${NC}"
    FAILED=1
fi
echo ""

# 2. Import sorting check
echo "2️⃣  Checking import sorting (isort)..."
if python -m isort --check-only --diff --profile=black --line-length=120 *.py tests/*.py 2>&1; then
    echo -e "${GREEN}✅ Import sorting is correct${NC}"
else
    echo -e "${RED}❌ Import sorting failed${NC}"
    echo -e "${YELLOW}💡 Fix with: python -m isort --profile=black --line-length=120 *.py tests/*.py${NC}"
    FAILED=1
fi
echo ""

# 3. Linting check
echo "3️⃣  Running linter (flake8)..."
if flake8 *.py tests/*.py --max-line-length=120 --extend-ignore=E203,W503 --statistics; then
    echo -e "${GREEN}✅ Linting passed${NC}"
else
    echo -e "${RED}❌ Linting failed${NC}"
    FAILED=1
fi
echo ""

# 4. Syntax validation
echo "4️⃣  Validating Python syntax..."
if python -m py_compile fetch_flights.py && python -c "import json; json.load(open('airlines_config.json'))"; then
    echo -e "${GREEN}✅ Syntax validation passed${NC}"
else
    echo -e "${RED}❌ Syntax validation failed${NC}"
    FAILED=1
fi
echo ""

# 5. Check for hardcoded secrets
echo "5️⃣  Checking for hardcoded secrets..."
if grep -r "AIRLABS_API_KEY.*=.*['\"][a-zA-Z0-9]\{20,\}" *.py 2>/dev/null; then
    echo -e "${RED}❌ Found potential hardcoded API key!${NC}"
    FAILED=1
else
    echo -e "${GREEN}✅ No hardcoded secrets found${NC}"
fi
echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All checks passed! Ready to commit.${NC}"
    exit 0
else
    echo -e "${RED}❌ Some checks failed. Please fix the issues above.${NC}"
    echo ""
    echo "Quick fix commands:"
    echo "  python -m black *.py tests/*.py          # Auto-format code"
    echo "  python -m isort --profile=black --line-length=120 *.py tests/*.py  # Auto-sort imports"
    echo "  flake8 *.py tests/*.py          # Show linting errors"
    exit 1
fi

