from django import urls as django_urls
from django.contrib import admin
from django.utils import safestring

from nutrimise.data.recipes import models as recipe_models


class _RecipeIngredientInline(admin.TabularInline):
    model = recipe_models.RecipeIngredient
    extra = 10


@admin.register(recipe_models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "author", "user_actions"]
    ordering = ["name"]
    search_fields = ["name"]

    inlines = [
        _RecipeIngredientInline,
    ]

    @admin.display(description="Actions")
    def user_actions(self, recipe: recipe_models.Recipe) -> safestring.SafeString:
        detail_url = django_urls.reverse(
            "recipe-details", kwargs={"recipe_id": recipe.id}
        )
        edit_url = django_urls.reverse(
            "admin:recipes_recipe_change", kwargs={"object_id": recipe.id}
        )
        return safestring.mark_safe(
            f'<a href="{detail_url}"><b>View</b></a> | <a href="{edit_url}"><b>Edit</b></a>'
        )


@admin.register(recipe_models.RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ["id", "recipe_name", "ingredient_name", "quantity", "units"]
    ordering = ["recipe__name", "ingredient__name"]

    @admin.display(description="Recipe name")
    def recipe_name(self, ingredient: recipe_models.RecipeIngredient) -> str:
        return ingredient.recipe.name

    @admin.display(description="Ingredient name")
    def ingredient_name(self, ingredient: recipe_models.RecipeIngredient) -> str:
        return ingredient.ingredient.name

    @admin.display(description="Units")
    def units(self, ingredient: recipe_models.RecipeIngredient) -> str:
        return ingredient.ingredient.units or "No units"
