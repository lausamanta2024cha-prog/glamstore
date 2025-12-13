#!/bin/bash
set -o errexit

echo "=== Starting GlamStore Build Process ==="

# Run migrations first
echo "1. Running migrations..."
python manage.py migrate

# Fix email column size
echo "2. Fixing email column size..."
python manage.py fix_email_column || echo "Warning: Email column fix failed, continuing..."

# Initialize database with users
echo "3. Initializing database..."
python init_db.py

# Collect static files
echo "4. Collecting static files..."
python manage.py collectstatic --noinput

echo "=== Build process completed successfully ==="
