import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "change-me-local-only")
DEBUG = os.getenv("DJANGO_DEBUG", "True").lower() in ("1", "true", "yes")

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# Installed apps (no extra apps required)
INSTALLED_APPS = [
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "taskhub.urls"

# Templates not needed for SPA; keep minimal
TEMPLATES = []

WSGI_APPLICATION = "taskhub.wsgi.application"

# Static files configuration
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"  # for collectstatic if needed

# MongoDB settings (used by our PyMongo service)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "task_manager_db")

# Default port for runserver convenience
PORT = int(os.getenv("PORT", "8000"))
