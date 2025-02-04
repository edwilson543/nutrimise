from django import urls as django_urls

from testing.factories import data as data_factories


def test_can_view_recipe_details(admin_client):
    recipe = data_factories.Recipe()
    nutritional_information = data_factories.IngredientNutritionalInformation()
    data_factories.RecipeIngredient(
        recipe=recipe, ingredient=nutritional_information.ingredient
    )

    url = django_urls.reverse("recipe-details", kwargs={"recipe_id": recipe.id})
    response = admin_client.get(url)

    assert response.status_code == 200
    assert len(response.context["nutritional_information"]) > 0
    assert len(response.context["recipe_ingredients"]) > 0
