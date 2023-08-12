# Third party imports
import pytest

# Django imports
from django.test import override_settings

# Local application imports
from app.recipes import _create_recipe
from tests import factories


class TestCreateRecipe:
    def test_creates_valid_recipe_for_user_without_hero_image(self):
        author = factories.User()

        recipe = _create_recipe.create_recipe(
            author=author, name="Beef", description="Beef beef", hero_image=None
        )

        assert recipe.author == author
        assert recipe.name == "Beef"
        assert recipe.description == "Beef beef"

    @override_settings(FILE_STORAGE_CLASS="tests.helpers.storage.TestFileStorage")
    def test_creates_valid_recipe_for_user_with_hero_image(self):
        author = factories.User()
        hero_image = factories.image()

        recipe = _create_recipe.create_recipe(
            author=author, name="Beef", description="Beef beef", hero_image=hero_image
        )

        assert recipe.author == author
        assert recipe.name == "Beef"
        assert recipe.description == "Beef beef"

        image = recipe.images.get()
        assert image.is_hero

    @pytest.mark.parametrize("name", ["new recipe", "NEW Recipe"])
    def test_raises_if_user_already_has_recipe_with_name(self, name: str):
        author = factories.User()
        factories.Recipe(author=author, name="new recipe")

        with pytest.raises(_create_recipe.RecipeNameNotUniqueForAuthor):
            _create_recipe.create_recipe(
                author=author, name=name, description="", hero_image=None
            )
