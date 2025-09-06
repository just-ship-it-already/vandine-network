#!/bin/bash
# Simple test script for CI/CD

echo "Running tests..."

# Check main files exist
[ -f vandine-showcase.html ] && echo "✅ Main HTML exists" || exit 1
[ -f README.md ] && echo "✅ README exists" || exit 1
[ -f .gitignore ] && echo "✅ .gitignore exists" || exit 1

# Validate HTML
grep -q "<!DOCTYPE html>" vandine-showcase.html && echo "✅ Valid HTML" || exit 1

# Check for secrets (excluding venv and common dirs)
if grep -r "password=\|token=" --include="*.html" --exclude-dir="venv" --exclude-dir=".git" --exclude-dir="node_modules" . 2>/dev/null | grep -v "example\|your\|django\|template"; then
  echo "❌ Exposed secrets found"
  exit 1
else
  echo "✅ No exposed secrets"
fi

echo "✅ All tests passed!"
