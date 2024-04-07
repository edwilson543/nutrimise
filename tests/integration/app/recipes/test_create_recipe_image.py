# Third party imports
import pytest

# Local application imports
from reciply.app.recipes import _create_recipe_image
from tests import factories
from tests.helpers import storage as storage_helpers


class TestCreateRecipeImage:
    @pytest.mark.parametrize("is_hero", [True, False])
    @storage_helpers.install_test_file_storage
    def test_creates_recipe_image_and_uploads(self, is_hero: bool):
        recipe = factories.Recipe()
        image = factories.image_buffer()

        _create_recipe_image.create_recipe_image(
            recipe=recipe, is_hero=is_hero, file=image
        )

        recipe.refresh_from_db()
        image = recipe.images.get()
        assert image.is_hero is is_hero
        assert f"recipe-{recipe.id}" in image.storage_context["key"]

        storage_helpers.assert_recipe_has_stored_images(recipe=recipe, n_images=1)

    @storage_helpers.install_test_file_storage
    def test_cannot_create_hero_image_when_already_exists(self):
        recipe = factories.Recipe()
        factories.RecipeImage(recipe=recipe, is_hero=True)

        image = factories.image_buffer()

        with pytest.raises(_create_recipe_image.RecipeAlreadyHasHeroImage):
            _create_recipe_image.create_recipe_image(
                recipe=recipe, is_hero=True, file=image
            )

        storage_helpers.assert_recipe_has_stored_images(recipe=recipe, n_images=0)
