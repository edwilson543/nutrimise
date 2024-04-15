from __future__ import annotations

import attrs

from nutrimise.data import constants


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
