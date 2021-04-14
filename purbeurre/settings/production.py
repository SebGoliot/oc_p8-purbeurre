from os import environ as os_environ
import dj_database_url
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from dotenv import load_dotenv
from .base import *

load_dotenv("../.env")

sentry_sdk.init(
    dsn=os_environ.get("SENTRY_DSN"),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
)

DEBUG = False

ALLOWED_HOSTS = ["purbeurre.sebgoliot.com"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os_environ.get("POSTGRES_NAME"),
        "USER": os_environ.get("POSTGRES_USER"),
        "PASSWORD": os_environ.get("POSTGRES_PASS"),
        "HOST": "127.0.0.1",
        "PORT": 5432,
    }
}


STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_SECONDS = 2592000  # 30 days
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
