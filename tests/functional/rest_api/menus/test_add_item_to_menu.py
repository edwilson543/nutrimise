# Third party imports
from rest_framework import status as drf_status

# Django imports
from django import urls as django_urls

# Local application imports
from data import constants
from tests import factories


class TestAddItemToMenu:
    def test_add_item_to_menu(self, rest_api_client):
        user = factories.User()
        rest_api_client.authorize_user(user)

        menu = factories.Menu(author=user)
        recipe = factories.Recipe()

        data = {"recipe_id": recipe.id, "day": 1, "meal_time": "LUNCH"}

        url = django_urls.reverse("menu-add-item", kwargs={"id": menu.id})
        response = rest_api_client.post(url, data=data)

        # Ensure the item was added to the menu
        menu.refresh_from_db()
        new_item = menu.items.get()
        assert new_item.recipe == recipe
        assert new_item.day == constants.Day.MONDAY
        assert new_item.meal_time == constants.MealTime.LUNCH

        assert response.status_code == drf_status.HTTP_201_CREATED
        assert response.data["id"] == new_item.id
