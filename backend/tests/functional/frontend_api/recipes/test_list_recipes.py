import pytest
from fastapi import routing

from testing.factories import data as data_factories


recipe_router = routing.APIRouter()


@pytest.mark.django_db(transaction=True)
def test_lists_all_recipes_when_no_filters_given(frontend_api_client):
    user = data_factories.User()
    frontend_api_client.set_authenticated_user(user)

    recipe = data_factories.Recipe()
    data_factories.SavedRecipe(recipe=recipe, user=user)
    other_recipe = data_factories.Recipe()

    response = frontend_api_client.get("/recipes")

    assert response.status_code == 200

    all_recipes = {recipe["id"]: recipe for recipe in response.json()["recipes"]}
    assert len(all_recipes) == 2
    assert set(all_recipes.keys()) == {recipe.id, other_recipe.id}

    assert all_recipes[recipe.id]["is_saved"]
    assert not all_recipes[other_recipe.id]["is_saved"]
