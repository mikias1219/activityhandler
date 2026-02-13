"""
LifeOS settings when running in Docker (Azure App Service or compose).
"""

from .base import *  # noqa: F401, F403

DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])

# In container, use SQLite in /app (writable). Azure App Service custom container often has no /home/site.
_db_url = env("DATABASE_URL", default="")
if not _db_url or _db_url.startswith("sqlite"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "/app/db.sqlite3",
        }
    }

# Optional: use dummy cache in container if no Redis (avoids connection errors)
_cache_url = env("CACHE_URL", default="")
if _cache_url.startswith("redis") or _cache_url.startswith("memcache"):
    pass  # use default from base
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        }
    }
