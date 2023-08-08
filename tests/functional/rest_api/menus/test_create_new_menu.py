# Third party imports
import pytest
from rest_framework import status as drf_status

# Django imports
from django import urls as django_urls

# Local application imports
from data.menus import models as menu_models
from tests import factories


class TestMenuCreate:
    def test_creates_valid_new_menu_without_suggestions(self, rest_api_client):
        user = factories.User()
        rest_api_client.authorize_user(user)

        menu_data = {
            "name": "my menu for this week",
            "description": "some description",
        }

        url = django_urls.reverse("menu-create")
        response = rest_api_client.post(url, data=menu_data)

        # Ensure a menu has been created in the db
        menu = menu_models.Menu.objects.get()
        assert menu.author == user
        assert menu.name == "my menu for this week"
        assert menu.description == "some description"

        assert response.status_code == drf_status.HTTP_201_CREATED
        assert response.data["id"] == menu.id

    def test_creates_valid_new_menu_with_suggestions(self, rest_api_client):
        user = factories.User()
        rest_api_client.authorize_user(user)

        recipe = factories.Recipe(author=user)

        menu_data = {
            "name": "my menu for this week",
            "description": "some description",
            "add_suggestions": True,
        }

        url = django_urls.reverse("menu-create")
        response = rest_api_client.post(url, data=menu_data)

        # Ensure a menu has been created in the db
        menu = menu_models.Menu.objects.get()
        assert menu.author == user
        assert menu.name == "my menu for this week"
        assert menu.description == "some description"

        # Ensure suggestions have been added to the menu
        assert menu.items.get().recipe == recipe

        assert response.status_code == drf_status.HTTP_201_CREATED
        assert response.data["id"] == menu.id

    @pytest.mark.django_db(transaction=True)
    def test_cannot_create_new_menu_with_non_unique_name(self, rest_api_client):
        user = factories.User()
        rest_api_client.authorize_user(user)

        menu = factories.Menu(author=user)

        menu_data = {
            "name": menu.name,
            "description": "something",
        }

        url = django_urls.reverse("menu-create")
        response = rest_api_client.post(url, data=menu_data)

        assert response.status_code == drf_status.HTTP_400_BAD_REQUEST
        assert response.data["name"] == ["You already have a menu with this name!"]

        # Ensure no new menu was created
        assert menu_models.Menu.objects.count() == 1

    def test_cannot_create_menu_from_invalid_payload(self, rest_api_client):
        user = factories.User()
        rest_api_client.authorize_user(user)

        menu_data = {
            "description": "something",
        }

        url = django_urls.reverse("menu-create")
        response = rest_api_client.post(url, data=menu_data)

        assert response.status_code == drf_status.HTTP_400_BAD_REQUEST
        assert response.data["name"]  # Error on the `name` field

        # Ensure no menu was created
        assert not menu_models.Menu.objects.exists()
