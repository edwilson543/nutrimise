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
