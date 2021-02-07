"""Custom managers for recipes models."""

from django.db import models

from base_objects.managers import TimeTrackedModelManager
from .querysets import IngredientSectionQueryset


class IngredientSectionManager(TimeTrackedModelManager):
    """Manager for IngredientSection model."""

    queryset_class = IngredientSectionQueryset

    def with_ingredients(self) -> models.QuerySet:
        return self.get_queryset().with_ingredients()
