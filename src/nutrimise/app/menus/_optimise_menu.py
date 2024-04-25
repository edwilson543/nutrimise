import attrs

from django.db import transaction

from nutrimise.domain import ingredients, menus, recipes


MenuDoesNotExist = menus.MenuDoesNotExist

UnableToOptimiseMenu = menus.UnableToOptimiseMenu


@attrs.frozen
class MenuHasNoRequirements(Exception):
    menu_id: int


def optimise_menu(*, menu_id: int) -> None:
    """
    Find the optimal recipes for a menu.

    :raises MenuDoesNotExist: When `menu_id` is invalid.
    :raises MenuHasNoRequirements: When the menu has no optimisation requirements.
    :raises UnableToOptimiseMenu: When the optimiser could not find any menus
        meeting the requirements.
    """

    menu = menus.get_menu(menu_id=menu_id)
    if menu.requirements is None:
        raise MenuHasNoRequirements(menu_id=menu_id)

    recipes_to_consider = recipes.get_recipes(
        dietary_requirement_ids=menu.requirements.dietary_requirement_ids
    )
    # Only bother loading the ingredients if the menu has variety requirements.
    if len(menu.requirements.variety_requirements) > 0:
        relevant_ingredients = _get_relevant_ingredients(recipes_to_consider)
    else:
        relevant_ingredients = ()

    solution = menus.optimise_recipes_for_menu(
        menu=menu,
        recipes_to_consider=recipes_to_consider,
        relevant_ingredients=relevant_ingredients,
    )

    with transaction.atomic():
        for menu_item in solution:
            # For mypy. The solver will raise if a menu item couldn't be solved.
            assert menu_item.recipe_id
            if menu_item.optimiser_generated:
                menus.update_menu_item_recipe(
                    menu_item_id=menu_item.id, recipe_id=menu_item.recipe_id
                )


def _get_relevant_ingredients(
    recipes_to_consider: tuple[recipes.Recipe, ...],
) -> tuple[ingredients.Ingredient, ...]:
    ingredient_ids: set[int] = set()
    for recipe in recipes_to_consider:
        for ingredient in recipe.ingredients:
            ingredient_ids.add(ingredient.ingredient_id)
    return ingredients.get_ingredients(ingredient_ids=ingredient_ids)
