# Third party imports
import pytest
from rest_framework import status as drf_status

# Django imports
from django import urls as django_urls

# Local application imports
from data import constants
from tests import factories


class TestAddItemsToMenu:
    def test_adds_item_to_menu(self, rest_api_client):
        user = factories.User()
        rest_api_client.authorize_user(user)

        menu = factories.Menu(author=user)
        recipe = factories.Recipe()

        menu_items = [{"recipe_id": recipe.id, "day": 1, "meal_time": "LUNCH"}]

        url = django_urls.reverse("menu-add-items", kwargs={"id": menu.id})
        response = rest_api_client.post(url, data=menu_items)

        # Ensure the item was added to the menu
        menu.refresh_from_db()
        new_item = menu.items.get()
        assert new_item.recipe == recipe
        assert new_item.day == constants.Day.MONDAY
        assert new_item.meal_time == constants.MealTime.LUNCH

        assert response.status_code == drf_status.HTTP_201_CREATED
        assert len(response.data) == 1
        assert response.data[0]["id"] == new_item.id

    @pytest.mark.django_db(transaction=True)
    def test_cannot_add_items_to_menu_at_same_meal_time(self, rest_api_client):
        user = factories.User()
        rest_api_client.authorize_user(user)

        menu = factories.Menu(author=user)

        menu_items = [
            {"recipe_id": factories.Recipe().id, "day": 1, "meal_time": "LUNCH"},
            {"recipe_id": factories.Recipe().id, "day": 1, "meal_time": "LUNCH"},
        ]

        url = django_urls.reverse("menu-add-items", kwargs={"id": menu.id})
        response = rest_api_client.post(url, data=menu_items)

        assert response.status_code == drf_status.HTTP_400_BAD_REQUEST
        assert response.data["items"] == [
            "You cannot select more than one recipe per meal time!"
        ]
