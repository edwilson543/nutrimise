import attrs

from nutrimise.domain import menus, recipes


@attrs.frozen
class RecipeNotProvidedInLookup(Exception):
    recipe_id: int


@attrs.frozen
class OptimiserInputs:
    menu: menus.Menu
    recipes_to_consider: tuple[recipes.Recipe, ...]

    def look_up_recipe(self, *, recipe_id: int) -> recipes.Recipe:
        for recipe in self.recipes_to_consider:
            if recipe.id == recipe_id:
                return recipe
        raise RecipeNotProvidedInLookup(recipe_id=recipe_id)

    @property
    def requirements(self) -> menus.MenuRequirements:
        assert self.menu.requirements  # Solver will reject menu without requirements.
        return self.menu.requirements
