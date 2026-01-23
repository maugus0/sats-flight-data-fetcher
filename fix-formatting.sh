#!/bin/bash
# Auto-fix formatting issues
# Run this to automatically fix formatting and import sorting

echo "🔧 Auto-fixing formatting issues..."
echo ""

# Format code with Black
echo "1️⃣  Formatting code with Black..."
python -m black *.py tests/*.py
echo "✅ Code formatted"
echo ""

# Sort imports with isort
echo "2️⃣  Sorting imports with isort..."
python -m isort --profile=black --line-length=120 *.py tests/*.py
echo "✅ Imports sorted"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Formatting fixes complete!"
echo ""
echo "Run pre-commit-check.sh to verify everything is correct."

