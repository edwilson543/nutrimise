from django import urls as django_urls

from testing.factories import data as data_factories
from tests.functional.admin import helpers


def test_can_lock_menu_item(admin_client):
    menu = data_factories.Menu()
    data_factories.MenuRequirements(menu=menu)
    recipe = data_factories.Recipe()
    menu_item = data_factories.MenuItem(
        menu=menu, recipe=recipe, optimiser_generated=False
    )

    menu_details_url = django_urls.reverse("menu-details", kwargs={"menu_id": menu.id})
    menu_detail_view = admin_client.get(menu_details_url)

    form_id = f"unlock-menu-item-{menu_item.id}"
    locked_menu_item_partial = helpers.hx_post_form(menu_detail_view, form_id=form_id)

    assert locked_menu_item_partial.status_code == 200
    assert locked_menu_item_partial.html.find(id=f"menu-item-{menu_item.id}")

    menu_item.refresh_from_db()
    assert menu_item.optimiser_generated is True


def test_can_unlock_menu_item(admin_client):
    menu = data_factories.Menu()
    data_factories.MenuRequirements(menu=menu)
    recipe = data_factories.Recipe()
    menu_item = data_factories.MenuItem(
        menu=menu, recipe=recipe, optimiser_generated=True
    )

    menu_details_url = django_urls.reverse("menu-details", kwargs={"menu_id": menu.id})
    menu_detail_view = admin_client.get(menu_details_url)

    form_id = f"lock-menu-item-{menu_item.id}"
    unlocked_menu_item_partial = helpers.hx_post_form(menu_detail_view, form_id=form_id)

    assert unlocked_menu_item_partial.status_code == 200
    assert unlocked_menu_item_partial.html.find(id=f"menu-item-{menu_item.id}")

    menu_item.refresh_from_db()
    assert menu_item.optimiser_generated is False
