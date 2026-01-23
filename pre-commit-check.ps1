# Pre-commit check script for Windows PowerShell
# Run this before committing to catch issues early

$ErrorActionPreference = "Stop"

Write-Host "🔍 Running pre-commit checks..." -ForegroundColor Cyan
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "fetch_flights.py")) {
    Write-Host "❌ Error: fetch_flights.py not found. Run this script from the project root." -ForegroundColor Red
    exit 1
}

# Check dependencies
Write-Host "📦 Checking dependencies..." -ForegroundColor Yellow
$missingDeps = @()

try {
    $null = Get-Command black -ErrorAction Stop
} catch {
    $missingDeps += "black"
}

try {
    $null = Get-Command isort -ErrorAction Stop
} catch {
    $missingDeps += "isort"
}

try {
    $null = Get-Command flake8 -ErrorAction Stop
} catch {
    $missingDeps += "flake8"
}

if ($missingDeps.Count -gt 0) {
    Write-Host "❌ Missing dependencies: $($missingDeps -join ', ')" -ForegroundColor Red
    Write-Host "💡 Install with: pip install -r requirements-dev.txt" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ All dependencies found" -ForegroundColor Green
Write-Host ""

# Track failures
$failed = $false

# 1. Black formatting check
Write-Host "1️⃣  Checking code formatting (Black)..." -ForegroundColor Cyan
try {
    $output = python -m black --check --diff *.py tests/*.py 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Code formatting is correct" -ForegroundColor Green
    } else {
        Write-Host "❌ Code formatting failed" -ForegroundColor Red
        Write-Host "💡 Fix with: python -m black *.py tests/*.py" -ForegroundColor Yellow
        $failed = $true
    }
} catch {
    Write-Host "❌ Error running black: $_" -ForegroundColor Red
    $failed = $true
}
Write-Host ""

# 2. Import sorting check
Write-Host "2️⃣  Checking import sorting (isort)..." -ForegroundColor Cyan
try {
    $output = python -m isort --check-only --diff --profile=black --line-length=120 *.py tests/*.py 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Import sorting is correct" -ForegroundColor Green
    } else {
        Write-Host "❌ Import sorting failed" -ForegroundColor Red
        Write-Host "💡 Fix with: python -m isort --profile=black --line-length=120 *.py tests/*.py" -ForegroundColor Yellow
        $failed = $true
    }
} catch {
    Write-Host "❌ Error running isort: $_" -ForegroundColor Red
    $failed = $true
}
Write-Host ""

# 3. Linting check
Write-Host "3️⃣  Running linter (flake8)..." -ForegroundColor Cyan
try {
    $output = flake8 *.py tests/*.py --max-line-length=120 --extend-ignore=E203,W503 --statistics 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Linting passed" -ForegroundColor Green
    } else {
        Write-Host "❌ Linting failed" -ForegroundColor Red
        $failed = $true
    }
} catch {
    Write-Host "❌ Error running flake8: $_" -ForegroundColor Red
    $failed = $true
}
Write-Host ""

# 4. Syntax validation
Write-Host "4️⃣  Validating Python syntax..." -ForegroundColor Cyan
try {
    python -m py_compile fetch_flights.py
    python -c "import json; json.load(open('airlines_config.json'))"
    Write-Host "✅ Syntax validation passed" -ForegroundColor Green
} catch {
    Write-Host "❌ Syntax validation failed: $_" -ForegroundColor Red
    $failed = $true
}
Write-Host ""

# 5. Check for hardcoded secrets
Write-Host "5️⃣  Checking for hardcoded secrets..." -ForegroundColor Cyan
$secretsFound = $false
Get-ChildItem -Path *.py -Recurse | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    if ($content -match "AIRLABS_API_KEY.*=.*['`"][a-zA-Z0-9]{20,}") {
        Write-Host "❌ Found potential hardcoded API key in: $($_.Name)" -ForegroundColor Red
        $secretsFound = $true
    }
}
if (-not $secretsFound) {
    Write-Host "✅ No hardcoded secrets found" -ForegroundColor Green
} else {
    $failed = $true
}
Write-Host ""

# Summary
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
if (-not $failed) {
    Write-Host "✅ All checks passed! Ready to commit." -ForegroundColor Green
    exit 0
} else {
    Write-Host "❌ Some checks failed. Please fix the issues above." -ForegroundColor Red
    Write-Host ""
    Write-Host "Quick fix commands:" -ForegroundColor Yellow
    Write-Host "  python -m black *.py tests/*.py          # Auto-format code"
    Write-Host "  python -m isort --profile=black --line-length=120 *.py tests/*.py  # Auto-sort imports"
    Write-Host "  flake8 *.py tests/*.py          # Show linting errors"
    exit 1
}

