"""Admin for `recipes` app."""

from django.contrib import admin
from django.db import models

from adminsortable2.admin import SortableInlineAdminMixin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from .models import Recipe, RecipeIngredient, IngredientType


class RecipeIngredientInline(SortableInlineAdminMixin, admin.TabularInline):
    """Inline model for Ingredients attached to a Recipe."""

    model = RecipeIngredient
    extra = 0
    autocomplete_fields = ["ingredient_type"]
    fields = [
        "order",
        "ingredient_type",
        "amount",
        "amount_uom",
        "preparation",
    ]

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).select_related("ingredient_type")


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    inlines = [
        RecipeIngredientInline,
    ]
    list_display = [
        "title",
        "subtitle",
    ]

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


### EXAMPLE ###
# from .models import MyModel

# @admin.register(MyModel)
# class MyModelAdmin(admin.ModelAdmin):
#     """Admin for MyModel."""
#     ...
