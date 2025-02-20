from typing import Any

from django import forms, http
from django.contrib import admin

from nutrimise.data.ingredients import models as ingredient_models
from nutrimise.domain import ingredients


@admin.register(ingredient_models.DietaryRequirement)
class DietaryRequirementAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_display_links = ["name"]


@admin.register(ingredient_models.IngredientCategory)
class IngredientCategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "number_of_ingredients"]
    list_display_links = ["name"]

    @admin.display(description="Number of ingredients")
    def number_of_ingredients(
        self, category: ingredient_models.IngredientCategory
    ) -> int:
        return category.ingredients.count()


class _IngredientNutritionalInformationInline(admin.TabularInline):
    class _FormSet(forms.BaseInlineFormSet):
        def __init__(self, *args: Any, **kwargs: Any):
            nutrients = ingredient_models.Nutrient.objects.order_by("name")
            kwargs["initial"] = [
                {"nutrient": nutrient, "units": ingredients.NutrientUnit.GRAMS.value}
                for nutrient in nutrients
            ]
            super().__init__(*args, **kwargs)

    model = ingredient_models.IngredientNutritionalInformation
    formset = _FormSet

    def get_extra(
        self, request: http.HttpRequest, obj: Any | None = None, **kwargs: object
    ) -> int:
        return ingredient_models.Nutrient.objects.count()


@admin.register(ingredient_models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "category_name", "units"]
    list_display_links = ["name"]
    ordering = ["name"]
    search_fields = ["name"]

    inlines = [
        _IngredientNutritionalInformationInline,
    ]

    @admin.display(description="Category")
    def category_name(self, ingredient: ingredient_models.Ingredient) -> str:
        return ingredient.category.name

    @admin.display(description="Units")
    def units(self, ingredient: ingredient_models.Ingredient) -> str:
        return ingredient.units or "-"


@admin.register(ingredient_models.Nutrient)
class NutrientAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "units"]
    list_display_links = ["name"]
    ordering = ["name"]


@admin.register(ingredient_models.IngredientNutritionalInformation)
class IngredientNutritionalInformationAdmin(admin.ModelAdmin):
    list_display = ["id", "ingredient_name", "nutrient_name", "nutrient_quantity"]
    list_display_links = ["ingredient_name"]
    ordering = ["ingredient__name"]

    @admin.display(description="Ingredient")
    def ingredient_name(
        self,
        nutritional_information: ingredient_models.IngredientNutritionalInformation,
    ) -> str:
        return nutritional_information.ingredient.name

    @admin.display(description="Nutrient")
    def nutrient_name(
        self,
        nutritional_information: ingredient_models.IngredientNutritionalInformation,
    ) -> str:
        return nutritional_information.nutrient.name

    @admin.display(description="Nutrient")
    def nutrient_quantity(
        self,
        nutritional_information: ingredient_models.IngredientNutritionalInformation,
    ) -> str:
        nutrient_units = ingredients.NutrientUnit(
            nutritional_information.nutrient.units
        )
        return f"{nutritional_information.quantity_per_gram} {nutrient_units}"
