"""
Django settings for recipesite project.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path

import environ

env = environ.Env(
    DJ_DEBUG=(bool, False),
    DJ_SECRET_KEY=(str, "Tot4llyInsecur3SecretKey-DO-NOT-USE-IN-PRODUCTION"),
    DJ_ALLOWED_HOSTS=(list, []),
    DJ_DB_URL=(str, ""),
    DJ_TIMEZONE=(str, "US/Eastern"),
)

DEBUG = env("DJ_DEBUG")


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parents[2]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJ_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
ALLOWED_HOSTS = env("DJ_ALLOWED_HOSTS")

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
    # Security headers added to requests
    "core.securemiddleware.set_secure_headers",
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
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = {
    "default": env.db_url("DJ_DB_URL"),
}


# Authentication
AUTH_USER_MODEL = "accounts.CustomUser"
AUTHENTICATION_BACKENDS = ["accounts.backends.EmailBackend"]

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators
# fmt: off
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
# fmt: on


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = env("DJ_TIMEZONE")
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
# STATIC_ROOT = BASE_DIR / "static"


# Media files (uploads and such)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


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

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
