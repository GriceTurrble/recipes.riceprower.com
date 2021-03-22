"""
Django settings for recipesite project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("HT_SECRET_KEY", "insecure-please-change-this")

# SECURITY WARNING: don't run with debug turned on in production!
ALLOWED_HOSTS = os.environ.get("HT_ALLOWED_HOSTS", "").split()

# Application definition
INSTALLED_APPS = [
    # Django dependencies
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.postgres",
    "django.contrib.humanize",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # Other dependencies
    "adminsortable2",
    "djfractions",
    "tinymce",
    # Accounts app, for custom user authentication
    "accounts.apps.AccountsConfig",
    # Base objects app, required by downstream.
    "base_objects.apps.BaseObjectsConfig",
    # Put your new apps here!
    "recipes.apps.RecipesConfig",
]

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    # CSP middleware: https://django-csp.readthedocs.io/en/latest/installation.html
    "csp.middleware.CSPMiddleware",
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
DATABASES = {
    "default": {
        "ENGINE": os.environ.get("HT_DB_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("DB_NAME", "db.sqlite3"),
        "USER": os.environ.get("DB_USER", ""),
        "PASSWORD": os.environ.get("DB_PASSWORD", ""),
        "HOST": os.environ.get("DB_HOST", None),
        "PORT": os.environ.get("DB_PORT", None),
        "CONN_MAX_AGE": 600,
    }
}


# Authentication
AUTH_USER_MODEL = "accounts.CustomUser"
AUTHENTICATION_BACKENDS = ["accounts.backends.EmailBackend"]

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
TIME_ZONE = os.environ.get("HT_TIME_ZONE", "US/Eastern")
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_URL = "/static/"
STATICFILES_DIRS = [(BASE_DIR / "assets" / "dist")]
STATIC_ROOT = BASE_DIR / "static"


# Media files (uploads and such)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# Logging.
# The main LOGGING config is stitched together in settings.__init__.
# We define segments of it here, as well as in other environments,
# then put the pieces together.
LOGS_DIR = BASE_DIR / "logs"
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {},
    "formatters": {
        "verbose": {
            "format": "[{levelname}] [{asctime}] [{module}] {message}",
            "style": "{",
        },
        "simple": {
            "format": "[{levelname}] {message}",
            "style": "{",
        },
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "handlers": {},
    "loggers": {},
}


# DRF settings
# REST_FRAMEWORK = {
#     "DEFAULT_PERMISSION_CLASSES": [
#         "rest_framework.permissions.IsAuthenticatedOrReadOnly",
#     ],
#     "DEFAULT_AUTHENTICATION_CLASSES": [
#         "rest_framework.authentication.TokenAuthentication",
#         "rest_framework.authentication.SessionAuthentication",
#     ],
#     "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
#     "PAGE_SIZE": 10,
# }


# TinyMCE adjustments
# The real default is:
# TINYMCE_DEFAULT_CONFIG = {
#     "theme": "silver",
#     "height": 500,
#     "menubar": False,
#     "plugins": (
#         "advlist,autolink,lists,link,image,charmap,print,preview,anchor,"
#         "searchreplace,visualblocks,code,fullscreen,insertdatetime,media,table,paste,"
#         "code,help,wordcount"
#     ),
#     "toolbar": (
#         "undo redo | formatselect | "
#         "bold italic backcolor | alignleft aligncenter "
#         "alignright alignjustify | bullist numlist outdent indent | "
#         "removeformat | help"
#     ),
# }
# More details can be found here: https://www.tiny.cloud/docs-4x/
TINYMCE_DEFAULT_CONFIG = {
    "theme": "silver",
    "height": 500,
    "menubar": False,
    "plugins": (
        "advlist,autolink,lists,link,image,charmap,print,preview,anchor,"
        "searchreplace,visualblocks,code,fullscreen,insertdatetime,media,table,paste,"
        "code,help,wordcount"
    ),
    "toolbar": (
        "code | undo redo | formatselect | "
        "bold italic backcolor | alignleft aligncenter "
        "alignright alignjustify | bullist numlist outdent indent | "
        "removeformat | help"
    ),
}


## CSP policies via django-csp
# See: https://django-csp.readthedocs.io/en/latest/configuration.html

# Enabled by the MIDDLEWARE "csp.middleware.CSPMiddleware"

# Details on CSP via Google Web Fundamentals, which is great reading material:
# https://developers.google.com/web/fundamentals/security/csp

# Spec from W3:
# https://www.w3.org/TR/CSP3/

# Set default to self domain and https: only
CSP_DEFAULT_SRC = [
    "'self'",
    "'unsafe-inline'",
    "'unsafe-eval'",
]
CSP_SCRIPT_SRC = [
    "'self'",
    "https:",
    "'sha256-wO9diDJWQhgGNe7+ZOCTsjDauLCvQkD2rE0AIBOHE7I='",
    "'sha256-eB8zFOmMMFp7pQaAQ9h2C1RxNPAUVRUQdUd5E1pXghc='",
    "'unsafe-eval'",
]
# Allow unsafe-eval and unsafe-inline scripting
# Note: CSP directives do not inherit, but we can approximate it
# by combining lists:
CSP_STYLE_SRC = [
    "'self'",
    "'unsafe-inline'",
    "https://kit.fontawesome.com",
]
CSP_IMG_SRC = [
    "'self'",
    "https:",
    "data:",
]
CSP_CONNECT_SRC = [
    "'self'",
    "https://ka-f.fontawesome.com",
]
CSP_FONT_SRC = [
    "'self'",
    "https://ka-f.fontawesome.com",
]
