# Django imports
from django import urls as django_urls

# Local application imports
from tests import factories


class TestMyRecipeList:
    def test_returns_serialized_recipes_authored_by_user(self, rest_api_client):
        user = factories.User()
        rest_api_client.authorize_user(user)

        recipe = factories.Recipe(author=user)
        other_recipe = factories.Recipe(author=user)

        # Make a user whose recipe we don't expect in the returned payload
        other_user = factories.User()
        factories.Recipe(author=other_user)

        url = django_urls.reverse("my-recipe-list")
        response = rest_api_client.get(url)

        assert {recipe["id"] for recipe in response.data} == {
            recipe.id,
            other_recipe.id,
        }
