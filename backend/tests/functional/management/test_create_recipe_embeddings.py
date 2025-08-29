from django.core import management as django_management
from django.test import override_settings
from numpy import testing as np_testing

from nutrimise.data.recipes import models as recipe_models
from nutrimise.domain import embeddings
from testing.factories import data as data_factories


@override_settings(EMBEDDING_VENDOR="FAKE")
def test_creates_embeddings_for_all_recipes():
    recipes = [data_factories.Recipe() for _ in range(0, 2)]

    django_management.call_command("create_recipe_embeddings")

    assert recipe_models.RecipeEmbedding.objects.count() == len(recipes)
    for recipe in recipes:
        embedding = recipe.embeddings.get()
        assert embedding.vendor == embeddings.EmbeddingVendor.FAKE
        expected_vector = embeddings.get_stub_vector_embedding()
        np_testing.assert_array_equal(embedding.vector, expected_vector)


@override_settings(EMBEDDING_VENDOR="BROKEN")
def test_does_not_create_embeddings_when_embedding_service_unavailable():
    data_factories.Recipe()

    django_management.call_command("create_recipe_embeddings")

    assert not recipe_models.RecipeEmbedding.objects.exists()
