# LifeOS — production Dockerfile (Azure App Service compatible)
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    DJANGO_SETTINGS_MODULE=lifeos.settings \
    LIFEOS_ENV=docker

WORKDIR /app

# System deps for psycopg
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements/base.txt requirements/base.txt
RUN pip install --no-cache-dir -r requirements/base.txt

COPY . .

EXPOSE 8000

RUN pip install --no-cache-dir gunicorn
RUN chmod +x scripts/start.sh 2>/dev/null || true
# Use ; so gunicorn starts even if migrate fails (you'll see errors in logs). /app is writable for SQLite.
CMD ["/bin/bash", "-c", "python manage.py migrate --noinput; python manage.py collectstatic --noinput --clear || true; exec gunicorn --bind 0.0.0.0:8000 --workers 2 --timeout 120 lifeos.wsgi:application"]
