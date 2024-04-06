# Third party imports
from rest_framework import status as drf_status

# Django imports
from django import urls as django_urls

# Local application imports
from tests import factories
from tests.helpers import storage as storage_helpers


class TestRecipeDetail:
    @storage_helpers.install_test_file_storage
    def test_returns_serialized_recipe(self, rest_api_client):
        user = factories.User()
        rest_api_client.authorize_user(user)

        recipe = factories.Recipe(author=user)
        image = factories.RecipeImage(recipe=recipe, is_hero=True)
        factories.RecipeIngredient(recipe=recipe)

        url = django_urls.reverse("recipe-detail", kwargs={"id": recipe.id})
        response = rest_api_client.get(url)

        assert response.status_code == drf_status.HTTP_200_OK
        assert response.data["id"] == recipe.id

        images = response.data["images"]
        assert len(images) == 1
        assert images[0]["id"] == image.id
        assert images[0]["image_source"] == storage_helpers.PUBLIC_IMAGE_SOURCE

        ingredients = response.data["ingredients"]
        assert len(ingredients) == 1

        nutritional_information = response.data["nutritional_information"]
        assert nutritional_information["protein"] > 0
        assert nutritional_information["carbohydrates"] > 0

    def test_not_found_when_user_is_not_author(self, rest_api_client):
        user = factories.User()
        rest_api_client.authorize_user(user)

        other_user = factories.User()
        recipe = factories.Recipe(author=other_user)

        url = django_urls.reverse("recipe-detail", kwargs={"id": recipe.id})
        response = rest_api_client.get(url)

        assert response.status_code == drf_status.HTTP_404_NOT_FOUND
