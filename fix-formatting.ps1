# Auto-fix formatting issues for Windows PowerShell
# Run this to automatically fix formatting and import sorting

Write-Host "🔧 Auto-fixing formatting issues..." -ForegroundColor Cyan
Write-Host ""

# Format code with Black
Write-Host "1️⃣  Formatting code with Black..." -ForegroundColor Yellow
python -m black *.py tests/*.py
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Code formatted" -ForegroundColor Green
} else {
    Write-Host "❌ Error formatting code" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Sort imports with isort
Write-Host "2️⃣  Sorting imports with isort..." -ForegroundColor Yellow
python -m isort --profile=black --line-length=120 *.py tests/*.py
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Imports sorted" -ForegroundColor Green
} else {
    Write-Host "❌ Error sorting imports" -ForegroundColor Red
    exit 1
}
Write-Host ""

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "✅ Formatting fixes complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Run pre-commit-check.ps1 to verify everything is correct." -ForegroundColor Yellow

