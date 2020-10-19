"""Models for `recipes` app."""

### WARNING ###
# DO NOT use `django.contrib.auth.models.User` directly.
# Instead, use `get_user_model`.
# https://learndjango.com/tutorials/django-best-practices-referencing-user-model
###############

import datetime
from fractions import Fraction

from django.contrib.auth import get_user_model
from django.db import models

from djfractions.models import DecimalFractionField
from djfractions import get_fraction_parts
from tinymce.models import HTMLField

from base_objects.models import HTBaseModel

User = get_user_model()


class IngredientType(HTBaseModel):
    """A type of an ingredient, used to hold common details about the
    ingredients of a recipe.
    """

    name = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        help_text="Name of this type of ingredient",
    )

    def __str__(self) -> str:
        return self.name


class Recipe(HTBaseModel):
    """A full recipe.

    Contains info about ingredients, directions, etc.
    """

    title = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        help_text=(
            "Title of this recipe. Give it a snappy name to remember it by! "
            "(must be unique!)"
        ),
    )
    subtitle = models.CharField(
        max_length=255,
        blank=True,
        help_text="Short description for this recipe.",
    )
    description = HTMLField()
    time_to_prep = models.DurationField(
        blank=True,
        default=datetime.timedelta(0),
        help_text="Estimated time to prepare this recipe (not including cook time).",
    )
    time_to_cook = models.DurationField(
        blank=True,
        default=datetime.timedelta(0),
        help_text="Estimated time to cook this recipe (not including prep time).",
    )

    def __str__(self) -> str:
        return self.title

    @property
    def total_time(self) -> datetime.timedelta:
        return self.time_to_prep + self.time_to_cook


class RecipeIngredient(HTBaseModel):
    """A specific ingredient for a given recipe.

    Links to an IngredientType to get that information,
    while including
    """

    recipe = models.ForeignKey(
        "recipes.Recipe",
        on_delete=models.CASCADE,
        related_name="ingredients",
        help_text="The Recipe this ingredient goes in.",
    )
    ingredient_type = models.ForeignKey(
        "recipes.IngredientType",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="The type of this ingredient. Please avoid duplicates!",
    )
    order = models.PositiveIntegerField(
        default=1,
        help_text=(
            "Order in which this ingredient appears in "
            "the list of ingredients for a recipe."
        ),
    )
    amount = DecimalFractionField(
        decimal_places=2,
        max_digits=5,
        help_text=(
            "Amount of this ingredient per the 'amount unit-of-measure'. "
            "Accepts fractions."
        ),
    )
    # Should be able to accept instances of `fractions.Fraction`

    # TODO create unit-of-measure choices for this option
    amount_uom = models.CharField(
        max_length=5, help_text="Unit of measure for 'amount'."
    )

    def amount_fraction_str(self):
        whole, numerator, denominator = get_fraction_parts(self.amount)
        fraction = Fraction(numerator, denominator)
        output = ""
        if whole:
            output += f"{whole} "
        output += f"{fraction}"
        return output

    def __str__(self) -> str:
        return f'"{self.recipe}" - {self.amount_fraction_str()} {self.amount_uom} {self.ingredient_type}'


class RecipeDirection(HTBaseModel):
    """A direction provided for a Recipe.

    Includes an ordering and text for the direction,
    """

    recipe = models.ForeignKey(
        "recipes.Recipe", on_delete=models.CASCADE, related_name="directions"
    )
    order = models.PositiveIntegerField(default=1)
    content = HTMLField()

    def __str__(self) -> str:
        return f'"{self.recipe}" - #{self.order} - {self.content}'


# TODO:
# RecipeDirection
# - recipe FK
# - content TextField
# - order (int)
