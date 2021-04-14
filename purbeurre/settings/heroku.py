from os import environ as os_environ
import django_heroku
import dj_database_url
from .base import *

DEBUG = False

ALLOWED_HOSTS = ["nutella-pur-beurre.herokuapp.com"]

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

db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES["default"].update(db_from_env)

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

django_heroku.settings(locals())
