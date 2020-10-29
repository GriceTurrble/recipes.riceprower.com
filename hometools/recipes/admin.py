"""Admin for `recipes` app."""

from django.contrib import admin

from adminsortable2.admin import SortableInlineAdminMixin

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


@admin.register(IngredientType)
class IngredientTypeAdmin(admin.ModelAdmin):
    search_fields = ["name"]


### EXAMPLE ###
# from .models import MyModel

# @admin.register(MyModel)
# class MyModelAdmin(admin.ModelAdmin):
#     """Admin for MyModel."""
#     ...
