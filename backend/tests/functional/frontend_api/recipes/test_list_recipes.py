import pytest
from fastapi import routing

from testing.factories import data as data_factories


recipe_router = routing.APIRouter()


@pytest.mark.django_db(transaction=True)
def test_lists_all_recipes_when_no_filters_given(frontend_api_client):
    recipe = data_factories.Recipe()
    other_recipe = data_factories.Recipe()

    response = frontend_api_client.get("/recipes")

    assert response.status_code == 200
    all_recipes = response.json()["recipes"]
    assert len(all_recipes) == 2
    assert {recipe["id"] for recipe in all_recipes} == {recipe.id, other_recipe.id}
