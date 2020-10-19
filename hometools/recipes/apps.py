"""App config for `recipes` app.

https://docs.djangoproject.com/en/3.0/ref/applications/
"""

# Install this app by adding the following to `INSTALLED_APPS`:
#     "recipes.apps.RecipesConfig",

# NOTE:
# Django docs include a mention of `default_app_config` in the app's `__init__.py` module,
# but this is actually discouraged outside some backwards-compatibility use-cases.
# Using a dotted path to this `AppConfig` subclass is a better practice.

from django.apps import AppConfig


class RecipesConfig(AppConfig):
    """App config for recipes."""

    name = "recipes"

    def ready(self):
        """Ready method for `recipes` app startup."""
        # Import signals module to wire up our signal receivers.
        # https://docs.djangoproject.com/en/3.0/topics/signals/#connecting-receiver-functions
        from . import signals
