from __future__ import annotations

# Standard library imports
import dataclasses


@dataclasses.dataclass(frozen=True)
class Nutrient:
    id: int
    name: str


@dataclasses.dataclass(frozen=True)
class NutritionalInformation:
    nutrient: Nutrient
    nutrient_quantity_grams: float
