from django import urls as django_urls

from tests.factories import data as data_factories


def test_can_view_menu_details(admin_client):
    menu = data_factories.Menu()
    data_factories.MenuItem(menu=menu)
    data_factories.MenuItem()

    url = django_urls.reverse("menu-details", kwargs={"menu_id": menu.id})
    response = admin_client.get(url)

    assert response.status_code == 200
    assert response.context["menu"]
    assert response.context["meal_schedule"]
    assert response.context["days"]
