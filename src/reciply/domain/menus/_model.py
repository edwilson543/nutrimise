from __future__ import annotations

# Standard library imports
import dataclasses

# Local application imports
from reciply.data import constants


@dataclasses.dataclass(frozen=True)
class Menu:
    id: int
    menu_items: list[MenuItem]


@dataclasses.dataclass(frozen=True)
class MenuItem:
    id: int
    recipe_id: int | None
    day: constants.Day
    meal_time: constants.MealTime
