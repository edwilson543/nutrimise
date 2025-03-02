from django.core import management as django_management
from django.test import override_settings

from nutrimise.data.recipes import models as recipe_models


@override_settings(DATA_EXTRACTION_VENDOR="FAKE", EMBEDDING_VENDOR="FAKE")
def test_extracts_recipes_from_test_dataset():
    django_management.call_command("extract_recipes_from_images", dataset="test")

    assert recipe_models.Recipe.objects.count() == 2

    author = recipe_models.RecipeAuthor.objects.get()
    assert author.first_name == "Ed"
    assert author.last_name == "Wilson"

    authored_recipe = author.recipes.get()
    assert authored_recipe.name == "My fake recipe"

    anonymous_recipe = recipe_models.Recipe.objects.get(author_id=None)
    assert anonymous_recipe.name == "My fake recipe"
