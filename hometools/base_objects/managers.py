"""Custom querysets and managers for base abstract models."""
from django.db import models

from .typing import DTType
from .querysets import HTBaseQuerySet


class HTBaseManager(models.Manager):
    """Manager for HTBaseModel."""

    queryset_class = HTBaseQuerySet

    def get_queryset(self):
        return self.queryset_class(self.model, using=self._db)

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
