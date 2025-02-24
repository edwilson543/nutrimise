from __future__ import annotations

import pydantic

from nutrimise.domain import ingredients, recipes


class Ingredient(pydantic.BaseModel):
    id: int | None
    name: str
    category_name: str
    units: str
    grams_per_unit: float

    @classmethod
    def from_domain_model(cls, ingredient: ingredients.Ingredient) -> Ingredient:
        return cls(
            id=ingredient.id,
            name=ingredient.name,
            category_name=ingredient.category.name,
            units=ingredient.units,
            grams_per_unit=ingredient.grams_per_unit,
        )


class RecipeIngredient(pydantic.BaseModel):
    ingredient: Ingredient
    quantity: float

    @classmethod
    def from_domain_model(
        cls, recipe_ingredient: recipes.RecipeIngredient
    ) -> RecipeIngredient:
        ingredient = Ingredient.from_domain_model(recipe_ingredient.ingredient)
        return RecipeIngredient(
            ingredient=ingredient, quantity=recipe_ingredient.quantity
        )


class Recipe(pydantic.BaseModel):
    name: str
    description: str
    methodology: str
    number_of_servings: int
    meal_times: list[recipes.MealTime]
    ingredients: list[RecipeIngredient]


# Nutritional information.


class Nutrient(pydantic.BaseModel):
    id: int
    name: str
    category: ingredients.NutrientCategory
    units: ingredients.NutrientUnit

    @classmethod
    def from_domain_model(cls, nutrient: ingredients.Nutrient) -> Nutrient:
        return cls(
            id=nutrient.id,
            name=nutrient.name,
            category=nutrient.category,
            units=nutrient.units,
        )


class IngredientNutritionalInformation(pydantic.BaseModel):
    ingredient_id: int
    nutrient_id: int
    nutrient_quantity_per_gram_of_ingredient: float


# Seems can't specify an array as the response format, hence this wrapper.
class IngredientNutritionalInformationList(pydantic.BaseModel):
    data: list[IngredientNutritionalInformation]
