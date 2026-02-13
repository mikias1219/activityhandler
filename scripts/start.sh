#!/usr/bin/env bash
# Run migrations then gunicorn (for Docker / Azure)
set -e
cd /app
python manage.py migrate --noinput
python manage.py collectstatic --noinput --clear 2>/dev/null || true
exec gunicorn --bind 0.0.0.0:8000 --workers 2 lifeos.wsgi:application
