import functools

import attrs

from nutrimise.domain import ingredients, menus, recipes


@attrs.frozen
class RecipeNotProvidedInLookup(Exception):
    recipe_id: int


@attrs.frozen
class IngredientNotProvidedInLookup(Exception):
    ingredient_id: int


@attrs.frozen
class OptimiserInputs:
    menu: menus.Menu

    # Note: `recipes_to_consider` also necessarily includes any pre-selected recipes.
    recipes_to_consider: tuple[recipes.Recipe, ...]

    # Ingredients are loaded to allow implementing the variety requirements.
    relevant_ingredients: tuple[ingredients.Ingredient, ...]

    def look_up_recipe(self, *, recipe_id: int) -> recipes.Recipe:
        for recipe in self.recipes_to_consider:
            if recipe.id == recipe_id:
                return recipe
        raise RecipeNotProvidedInLookup(recipe_id=recipe_id)

    def look_up_ingredient(self, *, ingredient_id: int) -> ingredients.Ingredient:
        for ingredient in self.relevant_ingredients:
            if ingredient.id == ingredient_id:
                return ingredient
        raise IngredientNotProvidedInLookup(ingredient_id=ingredient_id)

    @property
    def requirements(self) -> menus.MenuRequirements:
        assert self.menu.requirements  # Solver will reject menu without requirements.
        return self.menu.requirements

    @functools.cached_property
    def unoptimised_recipe_selections(self) -> tuple[recipes.Recipe, ...]:
        unique_recipe_ids = {
            menu_item.recipe_id
            for menu_item in self.menu.items
            if menu_item.recipe_id is not None
        }
        return tuple(
            self.look_up_recipe(recipe_id=recipe_id) for recipe_id in unique_recipe_ids
        )

    @functools.cached_property
    def unoptimised_ingredient_selections(self) -> tuple[ingredients.Ingredient, ...]:
        unique_ingredient_ids = {
            recipe_ingredient.ingredient_id
            for recipe in self.unoptimised_recipe_selections
            for recipe_ingredient in recipe.ingredients
        }
        return tuple(
            self.look_up_ingredient(ingredient_id=ingredient_id)
            for ingredient_id in unique_ingredient_ids
        )
