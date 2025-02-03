from django import urls as django_urls

from testing.factories import data as data_factories


def test_can_optimise_menu_from_details_view(admin_client):
    menu = data_factories.Menu()
    data_factories.MenuRequirements(menu=menu)
    menu_item = data_factories.MenuItem(menu=menu, recipe_id=None)
    recipe = data_factories.Recipe(meal_times=[menu_item.meal_time])

    menu_details_url = django_urls.reverse("menu-details", kwargs={"menu_id": menu.id})
    menu_detail_view = admin_client.get(menu_details_url)

    optimise_form = menu_detail_view.forms["optimise-menu"]
    optimise_response = optimise_form.submit()

    assert optimise_response.status_code == 302
    assert optimise_response.location == menu_details_url

    menu_item.refresh_from_db()
    assert menu_item.recipe_id == recipe.id
