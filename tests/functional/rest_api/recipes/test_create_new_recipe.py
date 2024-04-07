# Third party imports
import pytest
from rest_framework import status as drf_status

# Django imports
from django import urls as django_urls

# Local application imports
from reciply.data.recipes import models as recipe_models
from tests import factories
from tests.helpers import storage as storage_helpers


class TestRecipeCreate:
    @storage_helpers.install_test_file_storage
    def test_creates_valid_new_recipe(self, rest_api_client):
        user = factories.User()
        rest_api_client.authorize_user(user)

        recipe_data = {
            "name": "sausage",
            "description": "sausage",
            "hero_image": factories.image(),
            "number_of_servings": 3,
        }

        url = django_urls.reverse("recipe-create")
        response = rest_api_client.post(url, data=recipe_data, format="multipart")

        # Ensure a recipe has been created in the db
        recipe = recipe_models.Recipe.objects.get()
        assert recipe.author == user
        assert recipe.name == "sausage"
        assert recipe.description == "sausage"
        assert recipe.number_of_servings == 3

        image = recipe.images.get()
        assert image.is_hero
        storage_helpers.assert_recipe_has_stored_images(recipe, n_images=1)

        assert response.status_code == drf_status.HTTP_201_CREATED
        assert response.data["id"] == recipe.id

    @pytest.mark.django_db(transaction=True)
    def test_cannot_create_new_recipe_with_non_unique_name(self, rest_api_client):
        user = factories.User()
        rest_api_client.authorize_user(user)

        recipe = factories.Recipe(author=user)

        recipe_data = {
            "name": recipe.name,
            "description": "something",
            "number_of_servings": 1,
        }

        url = django_urls.reverse("recipe-create")
        response = rest_api_client.post(url, data=recipe_data)

        assert response.status_code == drf_status.HTTP_400_BAD_REQUEST
        assert response.data["name"] == ["You already have a recipe with this name!"]

        # Ensure no new recipe was created
        assert recipe_models.Recipe.objects.count() == 1

    def test_cannot_create_recipe_from_invalid_payload(self, rest_api_client):
        user = factories.User()
        rest_api_client.authorize_user(user)

        recipe_data = {
            "description": "something",
            "number_of_servings": 2,
        }

        url = django_urls.reverse("recipe-create")
        response = rest_api_client.post(url, data=recipe_data)

        assert response.status_code == drf_status.HTTP_400_BAD_REQUEST
        assert response.data["name"]  # Error on the `name` field

        # Ensure no recipe was created
        assert not recipe_models.Recipe.objects.exists()
