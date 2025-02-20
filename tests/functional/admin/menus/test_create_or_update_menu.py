from django import urls as django_urls
from django.test import override_settings

from nutrimise.data.menus import models as menu_models
from testing.factories import data as data_factories


@override_settings(EMBEDDING_VENDOR="FAKE")
def test_creates_menu_menu_items_menu_requirements_and_embeddings_using_create_form(
    admin_client,
):
    author = data_factories.User()

    url = django_urls.reverse("admin:menus_menu_add")
    response = admin_client.get(url)

    assert response.status_code == 200

    create_form = response.forms["menu_form"]
    # Basic recipe details.
    create_form["author"] = author.id
    create_form["name"] = "My new meal plan"
    create_form["number_of_days"] = 7
    create_form["meal_times"] = ["LUNCH", "DINNER"]
    # Requirements.
    create_form["requirements-0-optimisation_mode"] = "SEMANTIC"
    create_form["requirements-0-maximum_occurrences_per_recipe"] = 2
    create_response = create_form.submit()

    assert create_response.status_code == 302
    assert create_response.location == django_urls.reverse(
        "admin:menus_menu_changelist"
    )

    menu = menu_models.Menu.objects.get()
    assert menu.author_id == author.id
    assert menu.name == "My new meal plan"

    assert menu.items.count() == 14
    for day in [1, 2, 3, 4, 5, 6, 7]:
        for meal_time in ["LUNCH", "DINNER"]:
            assert menu.items.get(day=day, meal_time=meal_time)

    assert menu.requirements.optimisation_mode == "SEMANTIC"
    assert menu.requirements.maximum_occurrences_per_recipe == 2

    menu_embedding = menu.embeddings.get()
    assert menu_embedding.vendor == "FAKE"
    assert menu_embedding.model == "fake"
    assert len(menu_embedding.vector) > 0
    assert menu_embedding.prompt_hash == "69e1a0eaddcf12c7be156c1a8b1e680b"
