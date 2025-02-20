from __future__ import annotations

import attrs
from django.db import models as django_models


@attrs.frozen
class IngredientCategory:
    id: int
    name: str


@attrs.frozen
class Ingredient:
    id: int
    name: str
    category: IngredientCategory
    units: str
    grams_per_unit: float


class NutrientUnit(django_models.TextChoices):
    GRAMS = "GRAMS", "Grams"
    KCAL = "KCAL", "kcal"


@attrs.frozen
class Nutrient:
    id: int
    name: str
    units: NutrientUnit


@attrs.frozen
class NutritionalInformation:
    """
    An absolute quantity of a nutrient.
    """

    nutrient: Nutrient
    nutrient_quantity: float

    def __add__(self, other: NutritionalInformation) -> NutritionalInformation:
        if self.nutrient == other.nutrient:
            nutrient_quantity = self.nutrient_quantity + other.nutrient_quantity
            return NutritionalInformation(
                nutrient=self.nutrient,
                nutrient_quantity=nutrient_quantity,
            )
        else:
            raise ValueError(
                "Cannot add nutritional information for different nutrients."
            )

    @classmethod
    def zero(cls, *, nutrient: Nutrient) -> NutritionalInformation:
        return cls(nutrient=nutrient, nutrient_quantity=0.0)

    @classmethod
    def sum_by_nutrient(
        cls,
        *,
        nutritional_information: list[NutritionalInformation],
        nutrients: list[Nutrient],
    ) -> list[NutritionalInformation]:
        """
        Aggregate a list of nutritional information into a list where each nutrient is unique.
        """
        aggregated_nutritional_information = {
            nutrient: cls.zero(nutrient=nutrient) for nutrient in nutrients
        }
        for information in nutritional_information:
            if information.nutrient in nutrients:
                aggregated_nutritional_information[information.nutrient] += information

        return list(aggregated_nutritional_information.values())
