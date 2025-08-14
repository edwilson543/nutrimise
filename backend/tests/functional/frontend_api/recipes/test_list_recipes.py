import pytest

from testing.factories import data as data_factories


@pytest.mark.django_db(transaction=True)
def test_lists_all_recipes_when_no_filters_given(frontend_api_client):
    recipe = data_factories.Recipe(name="Apples")
    other_recipe = data_factories.Recipe(name="Bananas")

    response = frontend_api_client.get("/recipes")

    assert response.status_code == 200

    recipes = response.json()["recipes"]
    assert [recipe["id"] for recipe in recipes] == [recipe.id, other_recipe.id]

