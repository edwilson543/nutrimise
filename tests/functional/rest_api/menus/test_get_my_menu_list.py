# Django imports
from django import urls as django_urls

# Local application imports
from tests import factories


class TestMyMenuList:
    def test_returns_serialized_menus_authored_by_user(self, rest_api_client):
        user = factories.User()
        rest_api_client.authorize_user(user)

        first_menu = factories.Menu(author=user, name="AAA")
        second_menu = factories.Menu(author=user, name="BBB")
        factories.MenuItem(menu=second_menu)

        # Make a user whose menu we don't expect in the returned payload
        other_user = factories.User()
        factories.Menu(author=other_user)

        url = django_urls.reverse("my-menu-list")
        response = rest_api_client.get(url)

        assert response.data == [
            {
                "id": first_menu.id,
                "name": first_menu.name,
                "description": first_menu.description,
                "number_of_items": 0,
            },
            {
                "id": second_menu.id,
                "name": second_menu.name,
                "description": second_menu.description,
                "number_of_items": 1,
            },
        ]
