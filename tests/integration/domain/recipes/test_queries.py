# Local application imports
from domain.recipes import queries
from tests import factories


class TestGetRecipesAuthoredByUser:
    def test_gets_recipe_authored_by_user(self):
        user = factories.User()
        recipe = factories.Recipe(author=user)

        other_user = factories.User()
        factories.Recipe(author=other_user)

        user_recipes = queries.get_recipes_authored_by_user(user)

        assert user_recipes.get() == recipe


class TestGetHeroImage:
    def test_gets_hero_image_when_exists(self):
        hero_image = factories.RecipeImage(is_hero=True)

        result = queries.get_hero_image(hero_image.recipe)

        assert result == hero_image

    def test_gets_none_when_no_hero_image(self):
        recipe = factories.Recipe()

        result = queries.get_hero_image(recipe)

        assert result is None
