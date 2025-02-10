from __future__ import annotations

import attrs
from django.db import models as django_models

from nutrimise.domain import constants, embeddings, ingredients, recipes


@attrs.frozen
class Menu:
    id: int
    name: str
    description: str
    items: tuple[MenuItem, ...]
    requirements: MenuRequirements | None
    embeddings: tuple[embeddings.Embedding, ...]

    @property
    def days(self) -> tuple[int, ...]:
        return tuple(sorted(set(item.day for item in self.items)))

    @property
    def meal_schedule(self) -> dict[recipes.MealTime, dict[int, MenuItem]]:
        schedule: dict[recipes.MealTime, dict[int, MenuItem]] = {}
        for item in self.items:
            schedule[item.meal_time][item.day] = item
        return schedule


@attrs.define
class MenuItem:
    id: int
    recipe_id: int | None
    day: int
    meal_time: recipes.MealTime
    optimiser_generated: bool

    # Mutators

    def update_recipe_id(self, *, recipe_id: int) -> None:
        self.recipe_id = recipe_id


class OptimisationMode(django_models.TextChoices):
    RANDOM = "RANDOM", "Random"
    SEMANTIC = "SEMANTIC", "Semantic"
    NUTRIENT = "NUTRIENT", "Nutrient"
    VARIETY = "VARIETY", "Ingredient variety"
    EVERYTHING = "EVERYTHING", "Everything"


@attrs.frozen
class MenuRequirements:
    optimisation_mode: OptimisationMode
    nutrient_requirements: tuple[NutrientRequirement, ...]
    variety_requirements: tuple[VarietyRequirement, ...]
    maximum_occurrences_per_recipe: int
    dietary_requirement_ids: tuple[int, ...]


@attrs.frozen
class NutrientRequirement:
    nutrient_id: int
    minimum_quantity: float | None
    maximum_quantity: float | None
    target_quantity: float | None
    units: ingredients.NutrientUnit
    enforcement_interval: constants.NutrientRequirementEnforcementInterval


@attrs.frozen
class VarietyRequirement:
    ingredient_category_id: int
    minimum: int | None
    maximum: int | None
    target: int | None
