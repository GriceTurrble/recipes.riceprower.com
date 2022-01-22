"""Custom querysets and managers for base abstract models."""

from core.typing import DTType
from django.contrib.auth import get_user_model
from django.db import models

from .querysets import (
    OwnedModelQuerySet,
    OwnedTimeTrackedModelQuerySet,
    TimeTrackedModelQuerySet,
)

User = get_user_model()


class SiteBaseManager(models.Manager):
    """Base manager for other managers used within the site. Handles some common uses."""

    queryset_class = None

    def get_queryset(self):
        return self.queryset_class(self.model, using=self._db)


class TimeTrackedModelManager(SiteBaseManager):
    """Manager for TimeTrackedModel."""

    queryset_class = TimeTrackedModelQuerySet

    ## `time_created` command-style filtering ##
    def created_before(self, dt_: DTType) -> models.QuerySet:
        """Returns instances created before the given date/datetime."""
        return self.get_queryset().created_before(dt_)

    def created_after(self, dt_: DTType) -> models.QuerySet:
        """Returns instances created after the given date/datetime."""
        return self.get_queryset().created_after(dt_)

    def created_on_date(self, dt_: DTType) -> models.QuerySet:
        """Returns instances created on the date of the given date/datetime."""
        return self.get_queryset().created_on_date(dt_)

    def created_between(self, dt_one: DTType, dt_two: DTType) -> models.QuerySet:
        """Returns instances created within the range (dt_one, dt_two)."""
        return self.get_queryset().created_between(dt_one, dt_two)

    ## `time_modified` command-style filtering ##
    def modified_before(self, dt_: DTType) -> models.QuerySet:
        """Returns instances modified before the given date/datetime."""
        return self.get_queryset().modified_before(dt_)

    def modified_after(self, dt_: DTType) -> models.QuerySet:
        """Returns instances modified after the given date/datetime."""
        return self.get_queryset().modified_after(dt_)

    def modified_on_date(self, dt_: DTType) -> models.QuerySet:
        """Returns instances modified on the date of the given date/datetime."""
        return self.get_queryset().modified_on_date(dt_)

    def modified_between(self, dt_one: DTType, dt_two: DTType) -> models.QuerySet:
        """Returns instances modified within the range (dt_one, dt_two)."""
        return self.get_queryset().modified_between(dt_one, dt_two)


class OwnedModelManager(SiteBaseManager):
    """Manager for OwnedModel."""

    queryset_class = OwnedModelQuerySet

    def owned_by(self, user: User) -> models.QuerySet:
        """Returns instances owned by the designated user."""
        return self.filter(owner=user)


### Combo classes ###
# Add as needed in downstream apps.


class OwnedTimeTrackedModelManager(OwnedModelManager, TimeTrackedModelManager):
    """Manager for OwnedTimeTrackedModel."""

    queryset_class = OwnedTimeTrackedModelQuerySet
