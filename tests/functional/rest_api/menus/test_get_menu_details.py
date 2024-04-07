# Standard library imports
from unittest import mock

# Third party imports
from rest_framework import status as drf_status

# Django imports
from django import urls as django_urls

# Local application imports
from reciply.data import constants
from tests import factories


class TestMenuDetail:
    def test_returns_serialized_menu_with_items(self, rest_api_client):
        user = factories.User()
        rest_api_client.authorize_user(user)

        menu = factories.Menu(author=user)
        monday_lunch = factories.MenuItem(
            menu=menu, day=constants.Day.MONDAY, meal_time=constants.MealTime.LUNCH
        )
        tuesday_lunch = factories.MenuItem(
            menu=menu, day=constants.Day.TUESDAY, meal_time=constants.MealTime.LUNCH
        )

        url = django_urls.reverse("menu-detail", kwargs={"id": menu.id})
        response = rest_api_client.get(url)

        assert response.status_code == drf_status.HTTP_200_OK
        assert response.data["id"] == menu.id
        items = response.data["items"]
        assert items == [
            {
                "id": monday_lunch.id,
                "recipe": mock.ANY,
                "day": 1,
                "meal_time": "LUNCH",
            },
            {
                "id": tuesday_lunch.id,
                "recipe": mock.ANY,
                "day": 2,
                "meal_time": "LUNCH",
            },
        ]

    def test_not_found_when_user_is_not_author(self, rest_api_client):
        user = factories.User()
        rest_api_client.authorize_user(user)

        other_user = factories.User()
        menu = factories.Menu(author=other_user)

        url = django_urls.reverse("menu-detail", kwargs={"id": menu.id})
        response = rest_api_client.get(url)

        assert response.status_code == drf_status.HTTP_404_NOT_FOUND
