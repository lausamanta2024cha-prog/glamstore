#!/bin/bash
set -o errexit

echo "=== Starting GlamStore Build Process ==="

# Download media files from GitHub (continue even if it fails)
echo "1. Downloading media files..."
python download_media.py || echo "Warning: Media download failed, continuing..."

# Run migrations first
echo "2. Running migrations..."
python manage.py migrate

# Initialize database with users
echo "3. Initializing database..."
python init_db.py

# Collect static files
echo "4. Collecting static files..."
python manage.py collectstatic --noinput

echo "=== Build process completed successfully ==="
