from __future__ import annotations

import pydantic

from nutrimise.domain import ingredients, recipes


class Ingredient(pydantic.BaseModel):
    name: str
    category_name: str
    units: str | None
    grams_per_unit: float

    @classmethod
    def from_domain_model(cls, ingredient: ingredients.Ingredient) -> Ingredient:
        return cls(
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
    number_of_servings: int
    meal_times: list[recipes.MealTime]
    ingredients: list[RecipeIngredient]
