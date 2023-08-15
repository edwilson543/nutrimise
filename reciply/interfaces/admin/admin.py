# Django imports
from django.contrib import admin

# Local application imports
from data import constants
from data.ingredients import models as ingredient_models
from data.menus import models as menu_models
from data.recipes import models as recipe_models

admin.site.site_header = "Reciply admin"

# ----------
# Recipes
# ----------


@admin.register(recipe_models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ["id", "author", "name"]
    ordering = ["name"]
    search_fields = ["name", "author"]


@admin.register(recipe_models.RecipeImage)
class RecipeImageAdmin(admin.ModelAdmin):
    list_display = ["id", "recipe"]
    ordering = ["recipe__name"]


@admin.register(recipe_models.RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ["id", "recipe_name", "ingredient_name"]
    ordering = ["recipe__name", "ingredient__name_singular"]

    @admin.display(description="Recipe name")
    def recipe_name(self, ingredient: recipe_models.RecipeIngredient) -> str:
        return ingredient.recipe.name

    @admin.display(description="Ingredient name")
    def ingredient_name(self, ingredient: recipe_models.RecipeIngredient) -> str:
        return ingredient.ingredient.name_singular


# ----------
# Menus
# ----------


@admin.register(menu_models.Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ["id", "author", "name", "number_of_items"]
    ordering = ["name"]

    @admin.display()
    def number_of_items(self, menu: menu_models.Menu) -> int:
        return menu.items.count()


@admin.register(menu_models.MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ["id", "menu", "recipe", "format_day", "meal_time"]
    ordering = ["menu", "day", "meal_time"]
    search_fields = ["menu"]

    @admin.display()
    def format_day(self, menu_item: menu_models.MenuItem) -> str:
        return constants.Day(int(menu_item.day)).label.title()


# ----------
# Ingredients
# ----------


@admin.register(ingredient_models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "units"]
    ordering = ["name_singular"]

    @admin.display(description="Name")
    def name(self, ingredient: ingredient_models.Ingredient) -> str:
        return ingredient.name_singular

    @admin.display(description="Units")
    def units(self, ingredient: ingredient_models.Ingredient) -> str:
        return ingredient.displayed_units_plural or "-"
