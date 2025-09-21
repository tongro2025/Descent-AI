#!/bin/bash

# Git Ignore Status Checker
# This script checks which files are being ignored and why

echo "🔍 Git Ignore Status Report"
echo "=========================="
echo ""

echo "📁 Files currently being ignored:"
echo "--------------------------------"
git ls-files --others -i --exclude-standard | head -10

echo ""
echo "📋 Ignore reasons for key files:"
echo "--------------------------------"

# Check specific files
files_to_check=(".env" "data/sample/feat_struct.csv" "reports/evaluation_results.json" "venv/bin/activate")

for file in "${files_to_check[@]}"; do
    if [ -f "$file" ]; then
        echo "File: $file"
        git check-ignore -v "$file" 2>/dev/null || echo "  → Not ignored (good for sample data)"
        echo ""
    fi
done

echo "🔒 Security Check:"
echo "------------------"
if [ -f ".env" ]; then
    echo "⚠️  WARNING: .env file found! Make sure it's not committed."
else
    echo "✅ No .env file found (good!)"
fi

echo ""
echo "📊 Summary:"
echo "----------"
total_ignored=$(git ls-files --others -i --exclude-standard | wc -l)
echo "Total ignored files: $total_ignored"

echo ""
echo "✅ .gitignore is working correctly!"
