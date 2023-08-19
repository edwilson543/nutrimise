# Local application imports
from data.ingredients import models as ingredient_models


def get_ingredient_display_name(
    *, ingredient: ingredient_models.Ingredient, quantity: float
) -> str:
    is_integer = quantity == int(quantity)
    if is_integer:
        quantity = int(quantity)
    else:
        quantity = round(quantity, 2)

    if ingredient.units:
        return f"{quantity} {ingredient.units} of {ingredient.name_singular}"
    else:
        if quantity == 1:
            return f"{quantity} {ingredient.name_singular}"
        else:
            return f"{quantity} {ingredient.name_plural}"
