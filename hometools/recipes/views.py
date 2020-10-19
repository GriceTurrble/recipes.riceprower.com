"""Views for `recipes` app."""
# TODO: fill in template details for best-practice with Class-Based Views.
# Starter: https://spapas.github.io/2018/03/19/comprehensive-django-cbv-guide/

# Reference for all CBV classes available:
# https://docs.djangoproject.com/en/3.1/ref/class-based-views/

from django.views.generic import ListView

from .models import Recipe


class RecipeListView(ListView):
    """List view for Recipe instances."""

    model = Recipe
    context_object_name = "recipes"
