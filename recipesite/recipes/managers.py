"""Custom managers for recipes models."""

from core.managers import TimeTrackedModelManager
from django.db import models

from .querysets import IngredientSectionQueryset


class IngredientSectionManager(TimeTrackedModelManager):
    """Manager for IngredientSection model."""

    queryset_class = IngredientSectionQueryset

    def with_ingredients(self) -> models.QuerySet:
        return self.get_queryset().with_ingredients()
