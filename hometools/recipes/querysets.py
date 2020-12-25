"""Custom querysets recipes models."""

from django.db import models
from base_objects.querysets import HTBaseQuerySet


class IngredientSectionQueryset(HTBaseQuerySet):
    def with_ingredients(self) -> models.QuerySet:
        return self.filter(sectioned_ingredients__isnull=False).distinct()
