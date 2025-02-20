from src.env import app

from .apps import INSTALLED_APPS as INSTALLED_APPS
from .caches import CACHES as CACHES
from .logger import LOGGING as LOGGING
from .databases import DATABASES as DATABASES
from .templates import TEMPLATES as TEMPLATES
from .middleware import MIDDLEWARE as MIDDLEWARE
from .rest_framework import REST_FRAMEWORK as REST_FRAMEWORK

SECRET_KEY = app["secret_key"]
DEBUG = app["debug"]
ALLOWED_HOSTS = app["allowed_hosts"]

ROOT_URLCONF = "src.config.urls"
WSGI_APPLICATION = "src.config.wsgi.application"


STATIC_URL = "static/"
MEDIA_URL = "media/"
