# Third party imports
from rest_framework import status as drf_status

# Django imports
from django import urls as django_urls

# Local application imports
from tests import factories


class TestGetSuggestedRecipesForMenu:
    def test_returns_only_recipe_authored_by_user(self, rest_api_client):
        user = factories.User()
        rest_api_client.authorize_user(user)

        recipe = factories.Recipe(author=user)
        menu = factories.Menu(author=user)

        # Make a user whose recipe we don't expect in the returned payload
        other_user = factories.User()
        factories.Recipe(author=other_user)

        url = django_urls.reverse("suggest-recipes-for-menu", kwargs={"id": menu.id})
        response = rest_api_client.get(url)

        assert response.status_code == drf_status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["id"] == recipe.id
