# Local application imports
from interfaces.rest_api.recipes import serializers
from tests import factories
from tests.helpers import storage as storage_helpers


class TestRecipeDetail:
    @storage_helpers.install_test_file_storage
    def test_serializes_recipe_with_images(self):
        recipe = factories.Recipe()
        hero_image = factories.RecipeImage(recipe=recipe, is_hero=True)
        extra_image = factories.RecipeImage(recipe=recipe, is_hero=False)

        serialized_recipe = serializers.RecipeDetail(instance=recipe).data

        assert serialized_recipe["id"] == recipe.id
        images = serialized_recipe["images"]
        assert images == [
            {
                "id": hero_image.id,
                "is_hero": True,
                "image_source": storage_helpers.PUBLIC_IMAGE_SOURCE,
            },
            {
                "id": extra_image.id,
                "is_hero": False,
                "image_source": storage_helpers.PUBLIC_IMAGE_SOURCE,
            },
        ]
