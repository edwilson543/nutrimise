from django import urls as django_urls

from tests.factories import data as data_factories


def test_can_set_menu_item_status(admin_client):
    menu = data_factories.Menu()
    data_factories.MenuRequirements(menu=menu)
    recipe = data_factories.Recipe()
    menu_item = data_factories.MenuItem(
        menu=menu, recipe=recipe, optimiser_generated=False
    )

    menu_details_url = django_urls.reverse("menu-details", kwargs={"menu_id": menu.id})
    menu_detail_view = admin_client.get(menu_details_url)

    unlock_form = menu_detail_view.forms[f"unlock-menu-item-{menu_item.id}"]
    refreshed_detail_view = unlock_form.submit().follow()

    menu_item.refresh_from_db()
    assert menu_item.optimiser_generated is True

    lock_form = refreshed_detail_view.forms[f"lock-menu-item-{menu_item.id}"]
    lock_response = lock_form.submit()

    assert lock_response.status_code == 302
    assert lock_response.location == menu_details_url
    menu_item.refresh_from_db()
    assert menu_item.optimiser_generated is False
