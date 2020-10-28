"""Admin for `recipes` app."""

from django.contrib import admin

from .models import Recipe, RecipeIngredient, IngredientType


class RecipeIngredientInline(admin.TabularInline):
    """Inline model for Ingredients attached to a Recipe."""

    model = RecipeIngredient
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    inlines = [
        RecipeIngredientInline,
    ]


@admin.register(IngredientType)
class IngredientTypeAdmin(admin.ModelAdmin):
    pass


### EXAMPLE ###
# from .models import MyModel

# @admin.register(MyModel)
# class MyModelAdmin(admin.ModelAdmin):
#     """Admin for MyModel."""
#     ...
