# Third party imports
from rest_framework import status as drf_status

# Django imports
from django import urls as django_urls

# Local application imports
from tests import factories


class TestDeleteMenuItem:
    def test_removes_item_from_menu(self, rest_api_client):
        user = factories.User()
        rest_api_client.authorize_user(user)

        menu = factories.Menu(author=user)
        menu_item = factories.MenuItem(menu=menu)

        url = django_urls.reverse("menu-item", kwargs={"id": menu_item.id})
        response = rest_api_client.delete(url)

        # Ensure the item was removed from the menu
        menu.refresh_from_db()
        assert not menu.items.exists()

        assert response.status_code == drf_status.HTTP_200_OK

    def test_response_not_found_if_menu_item_does_not_exists(self, rest_api_client):
        user = factories.User()
        rest_api_client.authorize_user(user)

        url = django_urls.reverse("menu-item", kwargs={"id": 1000})
        response = rest_api_client.delete(url)

        # Ensure the item was added to the menu
        assert response.status_code == drf_status.HTTP_404_NOT_FOUND
