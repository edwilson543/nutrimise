# Standard library imports
import dataclasses


@dataclasses.dataclass(frozen=True)
class Nutrition:
    id: int
    name: str


@dataclasses.dataclass(frozen=True)
class NutritionalInformation:
    nutrient: Nutrition
    nutrient_quantity_grams: float
