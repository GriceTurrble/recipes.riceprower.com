"""
WSGI config for recipesite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Remove when django-fractions updates for Django 4.0 compatibility
from .monkeypatching import patch_lazy_translation

patch_lazy_translation()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

application = get_wsgi_application()
