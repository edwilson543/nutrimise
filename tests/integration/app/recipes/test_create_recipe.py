# Third party imports
import pytest

# Local application imports
from app.recipes import _create_recipe
from tests import factories


class TestCreateRecipe:
    def test_creates_valid_recipe_for_user(self):
        author = factories.User()

        recipe = _create_recipe.create_recipe(
            author=author, name="Beef", description="Beef beef"
        )

        assert recipe.author == author
        assert recipe.name == "Beef"
        assert recipe.description == "Beef beef"

    def test_raises_if_user_already_has_recipe_with_name(self):
        author = factories.User()
        recipe = factories.Recipe(author=author)

        with pytest.raises(_create_recipe.RecipeNameNotUniqueForAuthor):
            _create_recipe.create_recipe(
                author=author, name=recipe.name, description=""
            )
