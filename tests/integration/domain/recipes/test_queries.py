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

    def test_only_gets_recipes_meeting_single_dietary_requirement(self):
        dietary_requirement = data_factories.DietaryRequirement()
        matching_recipe = data_factories.Recipe.create_to_satisfy_dietary_requirements(
            dietary_requirements=(dietary_requirement,)
        )

        # Some non-matching recipes.
        data_factories.Recipe()
        data_factories.Recipe.create_to_satisfy_dietary_requirements(
            dietary_requirements=(data_factories.DietaryRequirement(),)
        )

        result = recipes.get_recipes(dietary_requirement_ids=(dietary_requirement.id,))

        assert len(result) == 1
        assert result[0].id == matching_recipe.id

    def test_only_gets_recipes_meeting_multiple_dietary_requirements(self):
        veggie = data_factories.DietaryRequirement()
        gluten_free = data_factories.DietaryRequirement()

        matching_recipe = data_factories.Recipe.create_to_satisfy_dietary_requirements(
            dietary_requirements=(veggie, gluten_free)
        )
        # Make some recipes that are just veggie / gluten-free.
        data_factories.Recipe.create_to_satisfy_dietary_requirements(
            dietary_requirements=(veggie,)
        )
        data_factories.Recipe.create_to_satisfy_dietary_requirements(
            dietary_requirements=(gluten_free,)
        )

        result = recipes.get_recipes(
            dietary_requirement_ids=(veggie.id, gluten_free.id)
        )
        data_factories.Recipe()

        assert len(result) == 1
        assert result[0].id == matching_recipe.id

    def test_gets_empty_tuple_when_there_are_no_recipes(self):
        result = recipes.get_recipes()

        assert result == ()
