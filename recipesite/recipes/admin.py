"""Admin for `recipes` app."""

from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin
from django.contrib import admin
from django.db import models
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from .models import IngredientSection, IngredientType, Recipe, RecipeIngredient


class RecipeIngredientInline(SortableInlineAdminMixin, admin.TabularInline):
    """Inline model for Ingredients attached to a Recipe."""

    model = RecipeIngredient
    extra = 0
    autocomplete_fields = ["ingredient_type", "section"]
    fields = [
        "order",
        "section",
        "ingredient_type",
        "amount",
        "amount_uom",
        "preparation",
    ]

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).select_related("ingredient_type")


@admin.register(Recipe)
class RecipeAdmin(SortableAdminBase, admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    inlines = [
        RecipeIngredientInline,
    ]
    list_display = [
        "title",
        "subtitle",
        "is_private",
    ]
    search_fields = ["title", "subtitle"]
    # fmt: off
    fieldsets = (
        (
            None, {
                "fields": (
                    ("title", "slug"),
                    "subtitle",
                    "is_private",
                ),
            },
        ),
        (
            "Description", {
                "classes": ("collapse",),
                "fields": ("description",),
            },
        ),
        (
            "Directions", {
                "classes": ("collapse", "open"),
                "fields": ("directions",),
            },
        ),
        (
            "Footnotes", {
                "classes": ("collapse",),
                "fields": ("footnotes",),
            },
        ),
        (
            "Stats", {
                "fields": (
                    ("time_to_prep", "time_to_cook"),
                    "num_servings",
                    "num_servings_text",
                    "num_servings_text_plural",
                    "nutrition_label",
                ),
            },
        ),
    )
    # fmt: on

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        qs = super().get_queryset(request)
        prefetch = models.Prefetch(
            "ingredients",
            queryset=RecipeIngredient.objects.select_related("ingredient_type"),
        )
        return qs.prefetch_related(prefetch)


@admin.register(IngredientType)
class IngredientTypeAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name", "plural_name"]


@admin.register(IngredientSection)
class IngredientSectionAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    autocomplete_fields = ["recipe"]


### EXAMPLE ###
# from .models import MyModel

# @admin.register(MyModel)
# class MyModelAdmin(admin.ModelAdmin):
#     """Admin for MyModel."""
#     ...
