from django.contrib import admin

from reciply.data.ingredients import models as ingredient_models


class _IngredientNutritionalInformationInline(admin.TabularInline):
    model = ingredient_models.IngredientNutritionalInformation


@admin.register(ingredient_models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "units"]
    ordering = ["name_singular"]

    inlines = [
        _IngredientNutritionalInformationInline,
    ]

    @admin.display(description="Name")
    def name(self, ingredient: ingredient_models.Ingredient) -> str:
        return ingredient.name_singular

    @admin.display(description="Units")
    def units(self, ingredient: ingredient_models.Ingredient) -> str:
        return ingredient.units or "-"


@admin.register(ingredient_models.Nutrient)
class NutrientAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    ordering = ["name"]


@admin.register(ingredient_models.IngredientNutritionalInformation)
class IngredientNutritionalInformationAdmin(admin.ModelAdmin):
    list_display = ["id", "ingredient_name", "nutrient_name", "quantity_per_gram"]
    ordering = ["ingredient__name_singular"]

    @admin.display(description="Ingredient")
    def ingredient_name(
        self,
        nutritional_information: ingredient_models.IngredientNutritionalInformation,
    ) -> str:
        return nutritional_information.ingredient.name_singular

    @admin.display(description="Nutrient")
    def nutrient_name(
        self,
        nutritional_information: ingredient_models.IngredientNutritionalInformation,
    ) -> str:
        return nutritional_information.nutrient.name
