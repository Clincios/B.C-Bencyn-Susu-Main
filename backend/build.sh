#!/bin/bash
# Build script for Render deployment
# This ensures pip, setuptools, and wheel are up-to-date before installing requirements

set -e  # Exit on any error

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR" || exit 1

echo "=== Current directory: $(pwd) ==="
echo "=== Python version: $(python --version) ==="

echo "=== Upgrading pip, setuptools, and wheel ==="
pip install --upgrade pip setuptools wheel

echo "=== Installing requirements ==="
pip install -r requirements.txt

echo "=== Collecting static files ==="
python manage.py collectstatic --noinput || echo "Static files collection skipped (this is OK if no static files)"

echo "=== Build completed successfully ==="

