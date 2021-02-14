"""Models for `hunnydo` app."""

### WARNING ###
# DO NOT use `django.contrib.auth.models.User` directly.
# Instead, use `get_user_model`.
# https://learndjango.com/tutorials/django-best-practices-referencing-user-model
###############


from django.contrib.auth import get_user_model
from django.db import models

from tinymce.models import HTMLField

from base_objects.models import OwnedTimeTrackedModel

User = get_user_model()


### EXAMPLE ###

# class MyModel(TimeTrackedModel):
#     """My model that does some things."""
#     ...


class TaskList(OwnedTimeTrackedModel):
    """Container for a set of Tasks."""

    name = models.CharField(max_length=255)


class Task(OwnedTimeTrackedModel):
    """To-dos. Literally, just a to-do task."""

    description = models.CharField(
        max_length=255,
    )
    long_description = HTMLField(
        blank=True,
    )
    completed_on = models.DateTimeField(
        blank=True,
        null=True,
    )
    task_list = models.ForeignKey(
        TaskList,
        on_delete=models.CASCADE,
        related_name="tasks",
        blank=True,
        null=True,
    )
    order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )

    class Meta:
        ordering = ["order"]

    @property
    def is_complete(self) -> bool:
        return self.completed_on is not None
