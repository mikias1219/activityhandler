"""
LifeOS production settings (Azure App Service).
"""
from .base import *  # noqa: F401, F403

DEBUG = False
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")  # Must be set in production
CORS_ALLOW_ALL_ORIGINS = False
# Configure CORS_ALLOWED_ORIGINS in production
