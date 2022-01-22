"""Custom querysets recipes models."""

from core.querysets import TimeTrackedModelQuerySet
from django.db import models


class IngredientSectionQueryset(TimeTrackedModelQuerySet):
    def with_ingredients(self) -> models.QuerySet:
        return self.filter(sectioned_ingredients__isnull=False).distinct()
