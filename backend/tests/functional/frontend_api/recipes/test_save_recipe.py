import pytest

from testing.factories import data as data_factories


@pytest.mark.django_db(transaction=True)
def test_user_can_save_and_then_unsave_recipe(frontend_api_client):
    user = data_factories.User()
    frontend_api_client.set_authenticated_user(user)
    recipe = data_factories.Recipe()

    save_response = frontend_api_client.put(f"/recipes/{recipe.id}/save")

    assert save_response.status_code == 200
    assert recipe.saves.get().user_id == user.id

    unsave_response = frontend_api_client.put(f"/recipes/{recipe.id}/unsave")

    assert unsave_response.status_code == 200
    assert not recipe.saves.exists()


@pytest.mark.django_db(transaction=True)
def test_cannot_save_recipe_that_does_not_exist(frontend_api_client):
    user = data_factories.User()
    frontend_api_client.set_authenticated_user(user)
    recipe_id = 123

    save_response = frontend_api_client.put(f"/recipes/{recipe_id}/save")

    assert save_response.status_code == 404
