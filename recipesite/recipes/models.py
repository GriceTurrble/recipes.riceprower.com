"""Models for `recipes` app."""

### WARNING ###
# DO NOT use `django.contrib.auth.models.User` directly.
# Instead, use `get_user_model`.
# https://learndjango.com/tutorials/django-best-practices-referencing-user-model
###############

import datetime
from fractions import Fraction
from typing import Tuple

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.fields import related
from django.urls import reverse as reverse_url

from djfractions.models import DecimalFractionField
from djfractions import get_fraction_parts
from tinymce.models import HTMLField

from base_objects.models import TimeTrackedModel

from .managers import IngredientSectionManager

User = get_user_model()


class IngredientType(TimeTrackedModel):
    """A type of an ingredient, used to hold common details about the
    ingredients of a recipe.
    """

    # TODO Look more in depth at the Spoonacular API:
    # https://spoonacular.com/food-api
    # Particularly for ingredient searching (to standardize ingredient types)
    # and recipe nutrition searching

    name = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        help_text="Name of this type of ingredient",
    )
    plural_name = models.CharField(
        max_length=255,
        blank=True,
        help_text="Plural name of this type of ingredient",
    )

    def __str__(self) -> str:
        return self.name

    # @property
    # def plural_name(self) -> str:
    #     if self._plural_name:
    #         return self._plural_name
    #     return f"{self.name}s"


class Recipe(TimeTrackedModel):
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
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
    )
    subtitle = models.CharField(
        max_length=255,
        blank=True,
        help_text="Short description for this recipe.",
    )
    description = HTMLField(blank=True)
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
    directions = HTMLField(blank=True)
    footnotes = HTMLField(blank=True)
    nutrition_label = models.ImageField(
        upload_to="nutrition_labels/", blank=True, default=""
    )

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse_url("recipes:recipe-detail", kwargs={"slug": self.slug})

    @staticmethod
    def delta_hours_minutes(delta: datetime.timedelta) -> Tuple[int, int]:
        """Return hours and minutes within a timedelta object as integers."""
        seconds = delta.total_seconds()
        hours = int(seconds // 3600)
        minutes = int((seconds // 60) - (hours * 60))
        return hours, minutes

    @classmethod
    def delta_to_str(cls, delta: datetime.timedelta) -> str:
        """Converts a timedelta object to a string output of hours / minutes.

        Possible formats:
        - "15 minutes"
        - "1 hour"
        - "2 hours 1 minute"
        """
        hours, minutes = cls.delta_hours_minutes(delta)
        output = ""
        if hours:
            output += f"{hours} hour{'' if hours == 1 else 's'}{' ' if minutes else ''}"
        if minutes:
            output += f"{minutes} minute{'' if minutes == 1 else 's'}"
        return output

    @property
    def time_to_prep_str(self) -> str:
        """Return a string of hours and minutes for the prep time."""
        return self.delta_to_str(self.time_to_prep)

    @property
    def time_to_cook_str(self) -> str:
        """Return a string of hours and minutes for the cook time."""
        return self.delta_to_str(self.time_to_cook)

    @property
    def total_time(self) -> datetime.timedelta:
        """Return a timedelta combining the prep and cook times."""
        return self.time_to_prep + self.time_to_cook

    @property
    def total_time_str(self) -> str:
        """Return a string of hours and minutes for the total time."""
        return self.delta_to_str(self.total_time)


class IngredientSection(TimeTrackedModel):
    """Most times, a recipe will have one set of ingredients.
    Others, the ingredients may be split into multiple sections,
    each one pertaining to a different subset of the recipe
    (like a sauce).

    This model is a target for RecipeIngredient instances to combine them
    into a section.

    Sections have a title and are orderable.

    If an Ingredient has no Section assignment, then it is part of the main
    ingredient list, even if other ingredients in the recipe are assigned to sections.
    """

    objects = IngredientSectionManager()

    recipe = models.ForeignKey(
        "recipes.Recipe",
        on_delete=models.CASCADE,
        related_name="ingredient_sections",
        help_text="The Recipe this section of Ingredients belongs to",
    )
    name = models.CharField(
        max_length=255,
        db_index=True,
        help_text=(
            "Name of this section of Ingredients, "
            "used as the section title when displayed on the frontend."
        ),
    )
    order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )

    class Meta:
        ordering = ["order"]
        verbose_name = "Ingredient Section"

    def __str__(self) -> str:
        return f"RecipeID={self.recipe.id} Section='{self.name}'"


class RecipeIngredient(TimeTrackedModel):
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
    section = models.ForeignKey(
        "recipes.IngredientSection",
        on_delete=models.SET_NULL,
        related_name="sectioned_ingredients",
        null=True,
        blank=True,
        help_text="Section of ingredients that this Ingredient falls under.",
    )
    ingredient_type = models.ForeignKey(
        "recipes.IngredientType",
        on_delete=models.CASCADE,
        related_name="+",
        help_text="The type of this ingredient. Please avoid duplicates!",
    )
    order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
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
    UOM_BLANK = "blank"
    UOM_CUP = "cup"
    UOM_DASH = "dash"
    UOM_FLUID_OUNCE = "fluid-ounce"
    UOM_FUCKTON = "fuckton"
    UOM_GALLON = "gallon"
    UOM_GRAM = "gram"
    UOM_KILOGRAM = "kilogram"
    UOM_LITER = "liter"
    UOM_MILLILITER = "ml"
    UOM_PACKAGE = "package"
    UOM_PACKET = "packet"
    UOM_PINCH = "pinch"
    UOM_PINT = "pint"
    UOM_POUND = "pound"
    UOM_QUART = "quart"
    UOM_TABLESPOON = "tbsp"
    UOM_TEASPOON = "tsp"
    UOM_WEIGHT_OUNCE = "weight-ounce"
    UOM_CHOICES = (
        (UOM_BLANK, "(blank)"),
        (UOM_CUP, "cup"),
        (UOM_DASH, "dash"),
        (UOM_FLUID_OUNCE, "fluid ounce"),
        (UOM_FUCKTON, "fuckton"),
        (UOM_GALLON, "gallon"),
        (UOM_GRAM, "gram"),
        (UOM_KILOGRAM, "kilogram"),
        (UOM_LITER, "liter"),
        (UOM_MILLILITER, "ml"),
        (UOM_PACKAGE, "package"),
        (UOM_PACKET, "packet"),
        (UOM_PINCH, "pinch"),
        (UOM_PINT, "pint"),
        (UOM_POUND, "pound"),
        (UOM_QUART, "quart"),
        (UOM_TABLESPOON, "tablespoon"),
        (UOM_TEASPOON, "teaspoon"),
        (UOM_WEIGHT_OUNCE, "ounce"),
    )
    amount_uom = models.CharField(
        max_length=20,
        help_text="Unit of measure for 'amount'.",
        choices=UOM_CHOICES,
        default=UOM_BLANK,
    )
    preparation = models.CharField(max_length=255, default="", blank=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Ingredient"

    @property
    def type(self):
        return self.ingredient_type

    def amount_fraction_str(self):
        whole, numerator, denominator = get_fraction_parts(self.amount)
        fraction = Fraction(numerator, denominator)
        output = ""
        if whole:
            output += f"{whole} "
        if fraction:
            output += f"{fraction}"
        if not output:
            output = "0"
        return output

    def __str__(self) -> str:
        return f'"{self.recipe}" - {self.amount_fraction_str()} {self.amount_uom} {self.ingredient_type}'
