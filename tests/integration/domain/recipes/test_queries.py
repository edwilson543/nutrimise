import pytest
from nutrimise.domain import recipes

from tests.factories import data as data_factories


class TestGetRecipe:
    def test_gets_recipe_when_exists(self):
        recipe = data_factories.Recipe()

        result = recipes.get_recipe(recipe_id=recipe.id)

        assert isinstance(result, recipes.Recipe)
        assert result.id == recipe.id

    def test_raises_when_recipe_does_not_exist(self):
        with pytest.raises(recipes.RecipeDoesNotExist) as exc:
            recipes.get_recipe(recipe_id=123)

        assert exc.value.recipe_id == 123


class TestGetRecipes:
    def test_gets_all_recipes(self):
        data_factories.Recipe()
        data_factories.Recipe()

        result = recipes.get_recipes()

        assert len(result) == 2

    def test_gets_empty_tuple_when_there_are_no_recipes(self):
        result = recipes.get_recipes()

        assert result == ()
