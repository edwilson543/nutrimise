# Django imports
from django import urls as django_urls

# Local application imports
from data import constants
from tests import factories


class TestGenerateShoppingList:
    def test_returns_serialized_shopping_list_for_menu(self, rest_api_client):
        user = factories.User()
        rest_api_client.authorize_user(user)

        menu = factories.Menu(author=user)
        apple = factories.Ingredient(
            name_singular="apple", name_plural="apples", category="Fruit", units=None
        )
        apple_recipe = factories.Recipe()
        factories.RecipeIngredient(recipe=apple_recipe, ingredient=apple, quantity=1)
        factories.MenuItem(recipe=apple_recipe, menu=menu, day=constants.Day.MONDAY)

        url = django_urls.reverse("shopping-list", kwargs={"id": menu.id})

        response = rest_api_client.get(url)

        assert response.data == {"Fruit": ["1 apple"]}
