from __future__ import annotations

import attrs

from nutrimise.data import constants
from nutrimise.data.ingredients import models as ingredient_models


@attrs.frozen
class Ingredient:
    id: int
    name: str
    category_id: int

    @classmethod
    def from_orm_model(cls, *, ingredient: ingredient_models.Ingredient) -> Ingredient:
        return cls(
            id=ingredient.id,
            name=ingredient.name,
            category_id=ingredient.category_id,
        )


@attrs.frozen
class Nutrient:
    id: int
    name: str


@attrs.frozen
class NutritionalInformation:
    """
    An absolute quantity of a nutrient.
    """

    nutrient: Nutrient
    nutrient_quantity: float
    units: constants.NutrientUnit
