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

    @classmethod
    def from_orm_model(cls, *, nutrient: ingredient_models.Nutrient) -> Nutrient:
        return Nutrient(id=nutrient.id, name=nutrient.name)


@attrs.frozen
class NutritionalInformation:
    """
    An absolute quantity of a nutrient.
    """

    nutrient: Nutrient
    nutrient_quantity: float
    units: constants.NutrientUnit

    def __add__(self, other: NutritionalInformation) -> NutritionalInformation:
        if self.nutrient == other.nutrient and self.units == other.units:
            nutrient_quantity = self.nutrient_quantity + other.nutrient_quantity
            return NutritionalInformation(
                nutrient=self.nutrient,
                nutrient_quantity=nutrient_quantity,
                units=self.units,
            )
        else:
            raise ValueError(
                "Cannot add nutritional information for different nutrients."
            )

    @classmethod
    def zero(
        cls,
        *,
        nutrient: Nutrient,
        units: constants.NutrientUnit = constants.NutrientUnit.GRAMS,
    ) -> NutritionalInformation:
        return cls(
            nutrient=nutrient,
            units=units,
            nutrient_quantity=0.0,
        )

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
