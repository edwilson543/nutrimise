import pytest

from nutrimise.app.recipes import _create_or_update_recipe_embedding
from nutrimise.data.recipes import models as recipe_models
from nutrimise.domain import embeddings
from tests.factories import data as data_factories


def test_creates_embedding_idempotently():
    embedding_service = embeddings.FakeEmbeddingService()
    recipe = data_factories.Recipe()

    _create_or_update_recipe_embedding.create_or_update_recipe_embedding(
        recipe_id=recipe.id, embedding_service=embedding_service
    )

    assert len(embedding_service.created_embeddings) == 1
    embedding = recipe_models.RecipeEmbedding.objects.get()
    assert embedding_service.created_embeddings[0] == embedding.to_domain_model()

    # Calling the function again should not create another embedding.
    embedding_service = embeddings.FakeEmbeddingService()
    _create_or_update_recipe_embedding.create_or_update_recipe_embedding(
        recipe_id=recipe.id, embedding_service=embedding_service
    )
    assert len(embedding_service.created_embeddings) == 0


def test_updates_existing_embedding_when_recipe_name_changes():
    embedding_service = embeddings.FakeEmbeddingService()
    recipe = data_factories.Recipe(name="Original name")

    _create_or_update_recipe_embedding.create_or_update_recipe_embedding(
        recipe_id=recipe.id, embedding_service=embedding_service
    )

    assert len(embedding_service.created_embeddings) == 1
    embedding = recipe_models.RecipeEmbedding.objects.get()
    assert embedding_service.created_embeddings[0] == embedding.to_domain_model()

    recipe.name = "Updated name"
    recipe.save(update_fields=["name"])

    # Calling the function again should create a new embedding.
    embedding_service = embeddings.FakeEmbeddingService()
    _create_or_update_recipe_embedding.create_or_update_recipe_embedding(
        recipe_id=recipe.id, embedding_service=embedding_service
    )
    assert len(embedding_service.created_embeddings) == 1


def test_raises_when_embedding_service_is_unavailable():
    embedding_service = embeddings.BrokenEmbeddingService()
    recipe = data_factories.Recipe(name="Original name")

    with pytest.raises(_create_or_update_recipe_embedding.UnableToGetEmbedding) as exc:
        _create_or_update_recipe_embedding.create_or_update_recipe_embedding(
            recipe_id=recipe.id, embedding_service=embedding_service
        )

    assert exc.value.vendor == embedding_service.vendor
    assert exc.value.model == embedding_service.model
