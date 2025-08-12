from django import urls as django_urls
from django.test import override_settings

from nutrimise.domain import embeddings
from testing.factories import data as data_factories


@override_settings(EMBEDDING_VENDOR="FAKE")
def test_returns_recipes_ordered_by_embedding_proximity_to_search_term(admin_client):
    recipe = data_factories.Recipe(name="A")
    other_recipe = data_factories.Recipe(name="B")

    url = django_urls.reverse("admin:recipes_recipe_changelist")
    recipe_changelist_response = admin_client.get(url)

    assert recipe_changelist_response.status_code == 200
    expected_ordering = [recipe, other_recipe]
    assert list(recipe_changelist_response.context["cl"].queryset) == expected_ordering

    # Embed the two recipes. Note the search text will be embedded to `[1, 1, ..., 1]` by the
    # fake embedding service, so `other_recipe` will have the least L2 distance.
    padding = [0] * (embeddings.EMBEDDING_DIMENSIONS - 2)
    data_factories.RecipeEmbedding(recipe=recipe, vector=[0, 0] + padding)
    data_factories.RecipeEmbedding(recipe=other_recipe, vector=[1, 1] + padding)

    search_form = recipe_changelist_response.forms["changelist-search"]
    search_form["q"] = "Some text"
    search_changelist_response = search_form.submit()

    assert search_changelist_response.status_code == 200
    new_expected_ordering = [other_recipe, recipe]
    assert (
        list(search_changelist_response.context["cl"].queryset) == new_expected_ordering
    )
