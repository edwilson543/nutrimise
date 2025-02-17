from django import urls as django_urls
from django.test import override_settings

from nutrimise.domain import menus
from testing.factories import data as data_factories


def test_can_optimise_menu_from_details_view(admin_client):
    menu = data_factories.Menu()
    data_factories.MenuRequirements(
        menu=menu, optimisation_mode=menus.OptimisationMode.RANDOM.value
    )
    menu_item = data_factories.MenuItem(menu=menu, recipe=None)
    recipe = data_factories.Recipe(meal_times=[menu_item.meal_time])

    menu_details_url = django_urls.reverse("menu-details", kwargs={"menu_id": menu.id})
    menu_detail_view = admin_client.get(menu_details_url)

    optimise_form = menu_detail_view.forms["optimise-menu"]
    # The optimisation mode should be pre-populated from the menu requirements.
    assert optimise_form["optimisation_mode"].value == "RANDOM"
    optimise_response = optimise_form.submit()

    assert optimise_response.status_code == 302
    assert optimise_response.location == menu_details_url

    menu_item.refresh_from_db()
    assert menu_item.recipe_id == recipe.id


@override_settings(EMBEDDING_VENDOR="FAKE")
def test_can_optimise_menu_and_provide_prompt_from_details_view(admin_client):
    menu = data_factories.Menu(name="My menu")
    menu_requirements = data_factories.MenuRequirements(
        menu=menu, optimisation_mode=menus.OptimisationMode.RANDOM.value
    )
    menu_item = data_factories.MenuItem(menu=menu, recipe=None)

    recipe = data_factories.Recipe(meal_times=[menu_item.meal_time])
    data_factories.RecipeEmbedding(recipe=recipe)

    menu_details_url = django_urls.reverse("menu-details", kwargs={"menu_id": menu.id})
    menu_detail_view = admin_client.get(menu_details_url)

    optimise_form = menu_detail_view.forms["optimise-menu"]
    optimise_form["optimisation_mode"] = "SEMANTIC"
    optimise_form["prompt"] = "Pick me the lean and mean recipes!"
    optimise_response = optimise_form.submit()

    assert optimise_response.status_code == 302
    assert optimise_response.location == menu_details_url

    menu_item.refresh_from_db()
    assert menu_item.recipe_id == recipe.id

    # The menu and prompt should also have been embedded along the way.
    embedding = menu.embeddings.get()
    assert embedding.prompt_hash == "7e4708214bb86ae0a68c052390b29ea6"

    # The menu requirements should have been updated.
    menu_requirements.refresh_from_db()
    assert menu_requirements.optimisation_mode == menus.OptimisationMode.SEMANTIC.value
