#!/bin/bash
set -e

# Wait a bit (optional small delay). Railway often handles start ordering; remove or adjust if unnecessary.
# echo "Sleeping for 1s to let DB boot..." && sleep 1

# Run Django migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn binding to PORT (Railway exposes $PORT)
: "${PORT:=8000}"
echo "Starting gunicorn on 0.0.0.0:${PORT}..."
exec gunicorn Todolist.wsgi:application \
    --bind 0.0.0.0:${PORT} \
    --workers 3 \
    --log-level info
