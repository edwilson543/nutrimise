# Django imports
from django.test import override_settings

# Local application imports
from interfaces.rest_api.recipes import serializers
from tests import factories


class TestRecipeDetail:
    @override_settings(
        MEDIA_BASE_URL="http://somewhere.org", MEDIA_URL="/my-media-files/"
    )
    def test_serializes_recipe_with_images_image(self):
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
                "image_source": f"http://somewhere.org/my-media-files/{hero_image.image.name}",
            },
            {
                "id": extra_image.id,
                "is_hero": False,
                "image_source": f"http://somewhere.org/my-media-files/{extra_image.image.name}",
            },
        ]
