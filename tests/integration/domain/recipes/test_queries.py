# Local application imports
from domain.recipes import queries
from tests import factories


class TestGetRecipesAuthoredByUser:
    def test_gets_recipe_written_by_author(self):
        user = factories.User()
        recipe = factories.Recipe(author=user)

        other_user = factories.User()
        factories.Recipe(author=other_user)

        user_recipes = queries.get_recipes_authored_by_user(user)

        assert user_recipes.get() == recipe
