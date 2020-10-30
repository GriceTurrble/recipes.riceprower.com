"""
Django settings for hometools project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
)
env.read_env(str(BASE_DIR / ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# Application definition
INSTALLED_APPS = [
    # Django dependencies
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.humanize",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Flat pages requirements
    "django.contrib.sites",
    "django.contrib.flatpages",
    # Other dependencies
    "adminsortable2",
    "rest_framework",
    "djfractions",
    "tinymce",
    # Base objects app, required by downstream.
    "base_objects.apps.BaseObjectsConfig",
    # Put your new apps here!
    "invoices.apps.InvoicesConfig",
    "recipes.apps.RecipesConfig",
]

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [(BASE_DIR / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Required by adminsortable
# With this set, any use of CSRF token in AJAX must pull it from a form element:
# it will NOT be available in a cookie.
# (which is wonky anyhow)
CSRF_COOKIE_HTTPONLY = True

# Login/logout redirect links
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {"default": env.db_url()}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators
# fmt: off
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
# fmt: on


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = env("TIME_ZONE")
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_URL = "/static/"
STATICFILES_DIRS = [(BASE_DIR / "assets")]
STATIC_ROOT = BASE_DIR / "static"


# Media files (uploads and such)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# Logging.
# The main LOGGING config is stitched together in settings.__init__.
# We define segments of it here, as well as in other environments,
# then put the pieces together.
LOGS_ROOT = BASE_DIR / "logs"
LOGGING_FORMATTERS = {
    "verbose": {
        "format": "[{levelname}] [{asctime}] [{module}] {message}",
        "style": "{",
    },
    "simple": {
        "format": "[{levelname}] {message}",
        "style": "{",
    },
}
LOGGING_FILTERS = {
    "require_debug_true": {
        "()": "django.utils.log.RequireDebugTrue",
    },
    "require_debug_false": {
        "()": "django.utils.log.RequireDebugFalse",
    },
}
# Handlers and Loggers are defined and overwritten in the environments.
LOGGING_HANDLERS = {}
LOGGING_LOGGERS = {}