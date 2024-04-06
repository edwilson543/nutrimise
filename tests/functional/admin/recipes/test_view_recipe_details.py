# Django imports
from django import urls as django_urls

# Local application imports
from tests import factories


def test_can_view_recipe_details(admin_client):
    recipe = factories.Recipe()
    nutritional_information = factories.IngredientNutritionalInformation()
    factories.RecipeIngredient(
        recipe=recipe, ingredient=nutritional_information.ingredient
    )

    url = django_urls.reverse("recipe-details", kwargs={"recipe_id": recipe.id})
    response = admin_client.get(url)

    assert response.status_code == 200
    assert len(response.context["nutritional_information"]) > 0
    assert len(response.context["recipe_ingredients"]) > 0
