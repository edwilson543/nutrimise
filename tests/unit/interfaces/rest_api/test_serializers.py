# Django imports
from django.test import override_settings

# Local application imports
from interfaces.rest_api.recipes import serializers
from tests import factories


class TestRecipeImage:
    @override_settings(
        MEDIA_BASE_URL="http://somewhere.org", MEDIA_URL="/my-media-files/"
    )
    def test_serializes_image(self):
        image = factories.RecipeImage.build(is_hero=True)

        serialized_image = serializers.RecipeImage(instance=image).data

        assert serialized_image == {
            "is_hero": True,
            "image_source": f"http://somewhere.org/my-media-files/{image.image.name}",
        }
