# Django imports
from django.contrib import admin

# Local application imports
from data.recipes import models as recipe_models


@admin.register(recipe_models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "author",
        "name",
    ]
    ordering = ["-name"]
    list_filter = ["author"]


@admin.register(recipe_models.RecipeImage)
class RecipeImageAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "recipe",
        "image",
    ]
    ordering = ["recipe"]
    list_filter = ["recipe", "recipe__author"]
