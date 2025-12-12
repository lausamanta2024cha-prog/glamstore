#!/bin/bash
set -o errexit

echo "=== Starting GlamStore Build Process ==="

# Run migrations first
echo "1. Running migrations..."
python manage.py migrate

# Initialize database with users
echo "2. Initializing database..."
python init_db.py

# Collect static files
echo "3. Collecting static files..."
python manage.py collectstatic --noinput

echo "=== Build process completed successfully ==="
