# Standard library imports
from collections import defaultdict

# Local application imports
from reciply.data.ingredients import models as ingredient_models
from reciply.data.menus import models as menu_models
from reciply.domain import ingredients


def generate_shopping_list(*, menu: menu_models.Menu) -> dict[str, list[str]]:
    aggregated_ingredients: dict[int, float] = defaultdict(lambda: 0)
    ingredient_lookup: dict[int, ingredient_models.Ingredient] = {}

    # Aggregate the quantity of each ingredient that is required
    for menu_item in menu.items.prefetch_related("recipe__ingredients__ingredient"):
        if not menu_item.recipe:
            continue
        for recipe_ingredient in menu_item.recipe.ingredients.all():
            aggregated_ingredients[
                recipe_ingredient.ingredient.id
            ] += recipe_ingredient.quantity
            ingredient_lookup[recipe_ingredient.ingredient.id] = (
                recipe_ingredient.ingredient
            )

    # Organize the ingredients by category and generate suitable display names
    shopping_list: dict[str, list[str]] = defaultdict(lambda: [])
    for ingredient_id, quantity in aggregated_ingredients.items():
        ingredient = ingredient_lookup[ingredient_id]
        shopping_list[ingredient.category].append(
            ingredients.get_ingredient_display_name(
                ingredient=ingredient, quantity=quantity
            )
        )

    return {
        category: sorted(category_list)
        for category, category_list in shopping_list.items()
    }
