import pydantic

from nutrimise.domain import constants


class Recipe(pydantic.BaseModel):
    name: str
    description: str
    number_of_servings: int
    meal_times: list[constants.MealTime]
