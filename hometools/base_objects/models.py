"""Base abstract models that all project models should inherit from."""

from django.db import models
from django.contrib.auth import get_user_model

from .managers import TimeTrackedModelManager, OwnedModelManager


User = get_user_model()


class TimeTrackedModel(models.Model):
    """Base abstract model adding time tracking."""

    objects = TimeTrackedModelManager()

    ## Basic time tracking for all models ##
    time_created = models.DateTimeField("created", auto_now_add=True, db_index=True)
    """Time when this model instance was created."""

    time_modified = models.DateTimeField("modified", auto_now=True, db_index=True)
    """Last time this model instance was modified."""

    class Meta:
        abstract = True


class OwnedModel(models.Model):
    """Base abstract model adding ownership."""

    objects = OwnedModelManager()

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    """User who owns this model instance."""

    class Meta:
        abstract = True
