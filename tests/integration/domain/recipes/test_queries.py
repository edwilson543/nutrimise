# Third party imports
import pytest

# Local application imports
from reciply.domain import recipes
from tests import factories


class TestGetRecipe:
    def test_gets_recipe_when_exists(self):
        recipe = factories.Recipe()

        result = recipes.get_recipe(recipe_id=recipe.id)

        assert isinstance(result, recipes.Recipe)
        assert result.id == recipe.id

    def test_raises_when_recipe_does_not_exist(self):
        with pytest.raises(recipes.RecipeDoesNotExist) as exc:
            recipes.get_recipe(recipe_id=123)

        assert exc.value.recipe_id == 123


class TestGetRecipes:
    def test_gets_all_recipes(self):
        factories.Recipe()
        factories.Recipe()

        result = recipes.get_recipes()

        assert len(result) == 2

    def test_gets_empty_tuple_when_there_are_no_recipes(self):
        result = recipes.get_recipes()

        assert result == ()


class TestGetRecipesAuthoredByUser:
    def test_gets_recipe_authored_by_user(self):
        user = factories.User()
        recipe = factories.Recipe(author=user)

        other_user = factories.User()
        factories.Recipe(author=other_user)

        user_recipes = recipes.get_recipes_authored_by_user(user)

        assert user_recipes.get() == recipe


class TestGetHeroImage:
    def test_gets_hero_image_when_exists(self):
        hero_image = factories.RecipeImage(is_hero=True)

        result = recipes.get_hero_image(hero_image.recipe)

        assert result == hero_image

    def test_gets_none_when_no_hero_image(self):
        recipe = factories.Recipe()

        result = recipes.get_hero_image(recipe)

        assert result is None
