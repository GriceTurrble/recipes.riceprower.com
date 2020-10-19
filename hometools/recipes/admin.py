"""Admin for `recipes` app."""

from django.contrib import admin

from .models import Recipe, RecipeDirection, RecipeIngredient, IngredientType


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    pass


@admin.register(RecipeDirection)
class RecipeDirectionAdmin(admin.ModelAdmin):
    pass


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    pass


@admin.register(IngredientType)
class IngredientTypeAdmin(admin.ModelAdmin):
    pass


### EXAMPLE ###
# from .models import MyModel

# @admin.register(MyModel)
# class MyModelAdmin(admin.ModelAdmin):
#     """Admin for MyModel."""
#     ...
