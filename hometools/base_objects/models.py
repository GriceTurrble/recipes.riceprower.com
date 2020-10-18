"""Base abstract models that all project models should inherit from."""

from django.db import models

from .managers import HTBaseManager


class HTBaseModel(models.Model):
    """Base abstract model for all models used throughout the project."""

    objects = HTBaseManager()

    ## Basic time tracking for all models ##
    time_created = models.DateTimeField("created", auto_now_add=True, db_index=True)
    time_modified = models.DateTimeField("modified", auto_now=True, db_index=True)

    class Meta:
        abstract = True
