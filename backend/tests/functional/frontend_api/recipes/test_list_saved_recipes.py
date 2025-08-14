import pytest

from testing.factories import data as data_factories


@pytest.mark.django_db(transaction=True)
def test_lists_saved_recipes_for_user(frontend_api_client):
    user = data_factories.User()
    frontend_api_client.set_authenticated_user(user)

    recipe = data_factories.Recipe()
    data_factories.SavedRecipe(recipe=recipe, user=user)

    other_recipe = data_factories.Recipe()
    other_user = data_factories.User()
    data_factories.SavedRecipe(recipe=other_recipe, user=other_user)

    response = frontend_api_client.get("/recipes/saved")

    assert response.status_code == 200
    assert response.json() == [recipe.id]
