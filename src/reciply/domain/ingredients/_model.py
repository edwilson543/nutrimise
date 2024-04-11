from __future__ import annotations

# Third party imports
import attrs


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
    nutrient_quantity_grams: float
