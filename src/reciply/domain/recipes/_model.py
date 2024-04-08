# Standard library imports
import dataclasses

# Local application imports
from reciply.data import constants
from reciply.domain import ingredients


@dataclasses.dataclass(frozen=True)
class Recipe:
    id: int
    meal_times: list[constants.MealTime]
    nutritional_information: list[ingredients.NutritionalInformation]
