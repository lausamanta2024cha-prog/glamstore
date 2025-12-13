#!/bin/bash
set -o errexit

echo "=== Starting GlamStore Build Process ==="

# Run migrations first
echo "1. Running migrations..."
python manage.py migrate

# Initialize database with users
echo "2. Initializing database..."
python init_db.py

# Restore data from MySQL dump
echo "3. Restoring data from database dump..."
python ejecutar_en_render.py glamstoredb.sql || echo "Warning: Data restoration failed, continuing..."

# Collect static files
echo "4. Collecting static files..."
python manage.py collectstatic --noinput

echo "=== Build process completed successfully ==="
