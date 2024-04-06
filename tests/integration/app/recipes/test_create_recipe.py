# Third party imports
import pytest

# Local application imports
from app.recipes import _create_recipe
from tests import factories
from tests.helpers import storage as storage_helpers


class TestCreateRecipe:
    def test_creates_valid_recipe_for_user_without_hero_image(self):
        author = factories.User()

        recipe = _create_recipe.create_recipe(
            author=author,
            name="Beef",
            description="Beef beef",
            number_of_servings=3,
            hero_image=None,
        )

        assert recipe.author == author
        assert recipe.name == "Beef"
        assert recipe.description == "Beef beef"
        assert recipe.number_of_servings == 3

    @storage_helpers.install_test_file_storage
    def test_creates_valid_recipe_for_user_with_hero_image(self):
        author = factories.User()
        hero_image = factories.image()

        recipe = _create_recipe.create_recipe(
            author=author,
            name="Beef",
            description="Beef beef",
            number_of_servings=1,
            hero_image=hero_image,
        )

        assert recipe.author == author
        assert recipe.name == "Beef"
        assert recipe.description == "Beef beef"
        assert recipe.number_of_servings == 1

        image = recipe.images.get()
        assert image.is_hero
        storage_helpers.assert_recipe_has_stored_images(recipe, n_images=1)

    @pytest.mark.parametrize("name", ["new recipe", "NEW Recipe"])
    def test_raises_if_user_already_has_recipe_with_name(self, name: str):
        author = factories.User()
        factories.Recipe(author=author, name="new recipe")

        with pytest.raises(_create_recipe.RecipeNameNotUniqueForAuthor):
            _create_recipe.create_recipe(
                author=author,
                name=name,
                description="",
                number_of_servings=1,
                hero_image=None,
            )
