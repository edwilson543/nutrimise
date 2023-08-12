# Django imports
from django import urls as django_urls

# Local application imports
from tests import factories
from tests.helpers import storage as storage_helpers


class TestMyRecipeList:
    @storage_helpers.install_test_file_storage
    def test_returns_serialized_recipes_authored_by_user(self, rest_api_client):
        user = factories.User()
        rest_api_client.authorize_user(user)

        apple_recipe = factories.Recipe(author=user, name="apples")
        factories.RecipeImage(recipe=apple_recipe, is_hero=True)
        banana_recipe = factories.Recipe(author=user, name="bananas")

        # Make a user whose recipe we don't expect in the returned payload
        other_user = factories.User()
        factories.Recipe(author=other_user)

        url = django_urls.reverse("my-recipe-list")
        response = rest_api_client.get(url)

        serialized_apple_recipe = response.data[0]
        assert serialized_apple_recipe["id"] == apple_recipe.id
        assert (
            serialized_apple_recipe["hero_image_source"]
            == storage_helpers.PUBLIC_IMAGE_SOURCE
        )

        serialized_banana_recipe = response.data[1]
        assert serialized_banana_recipe["id"] == banana_recipe.id
        assert serialized_banana_recipe["hero_image_source"] is None
