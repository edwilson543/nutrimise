from django import urls as django_urls
from django.test import override_settings

from nutrimise.data.recipes import models as recipe_models
from testing.factories import data as data_factories


@override_settings(EMBEDDING_VENDOR="FAKE")
def test_creates_recipe_using_create_form(admin_client):
    author = data_factories.RecipeAuthor()

    url = django_urls.reverse("admin:recipes_recipe_add")
    response = admin_client.get(url)

    assert response.status_code == 200

    create_form = response.forms["recipe_form"]
    create_form["author"] = author.id
    create_form["name"] = "Chicken pasta"
    create_form["meal_times"] = "DINNER"
    create_form["number_of_servings"] = 3
    create_response = create_form.submit()

    assert create_response.status_code == 302
    assert create_response.location == django_urls.reverse(
        "admin:recipes_recipe_changelist"
    )

    recipe = recipe_models.Recipe.objects.get()
    assert recipe.author_id == author.id
    assert recipe.name == "Chicken pasta"
    assert recipe.meal_times == ["DINNER"]
    assert recipe.number_of_servings == 3

    recipe_embedding = recipe.embeddings.get()
    assert recipe_embedding.vendor == "FAKE"
    assert recipe_embedding.model == "fake"
    assert len(recipe_embedding.vector) > 0
    assert recipe_embedding.prompt_hash == "469509d8f71e8ae9ff4a4200fc53330b"
