# Standard library imports
import dataclasses

# Local application imports
from reciply.data import constants


@dataclasses.dataclass(frozen=True)
class Recipe:
    id: int
    meal_times: list[constants.MealTime]
