# Third party imports
from rest_framework import status as drf_status

# Django imports
from django import urls as django_urls

# Local application imports
from tests import factories


class TestRecipeDetail:
    def test_returns_serialized_recipe(self, rest_api_client):
        user = factories.User()
        rest_api_client.authorize_user(user)

        recipe = factories.Recipe(author=user)

        url = django_urls.reverse("recipe-detail", kwargs={"id": recipe.id})
        response = rest_api_client.get(url)

        assert response.data["id"] == recipe.id

    def test_not_found_when_user_is_not_author(self, rest_api_client):
        user = factories.User()
        rest_api_client.authorize_user(user)

        other_user = factories.User()
        recipe = factories.Recipe(author=other_user)

        url = django_urls.reverse("recipe-detail", kwargs={"id": recipe.id})
        response = rest_api_client.get(url)

        assert response.status_code == drf_status.HTTP_404_NOT_FOUND
