# Local application imports
from data.ingredients import models as ingredient_models


def get_ingredient_display_name(
    *, ingredient: ingredient_models.Ingredient, quantity: float
) -> str:
    if ingredient.units:
        return f"{round(quantity, 2)} {ingredient.units} of {ingredient.name_singular}"
    else:
        if quantity == 1:
            return f"1 {ingredient.name_singular}"
        else:
            return f"{round(quantity, 2)} {ingredient.name_plural}"
