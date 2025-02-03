import pytest

from nutrimise.app.menus import _create_or_update_menu_embedding
from nutrimise.data.menus import models as menu_models
from nutrimise.domain import embeddings
from testing.factories import data as data_factories


def test_creates_embedding_idempotently():
    embedding_service = embeddings.FakeEmbeddingService()
    menu = data_factories.Menu()

    _create_or_update_menu_embedding.create_or_update_menu_embedding(
        menu_id=menu.id, embedding_service=embedding_service
    )

    assert len(embedding_service.created_embeddings) == 1
    embedding = menu_models.MenuEmbedding.objects.get()
    assert embedding_service.created_embeddings[0] == embedding.to_domain_model()

    # Calling the function again should not create another embedding.
    embedding_service = embeddings.FakeEmbeddingService()
    _create_or_update_menu_embedding.create_or_update_menu_embedding(
        menu_id=menu.id, embedding_service=embedding_service
    )
    assert len(embedding_service.created_embeddings) == 0


def test_updates_existing_embedding_when_menu_name_changes():
    embedding_service = embeddings.FakeEmbeddingService()
    menu = data_factories.Menu(name="Original name")

    _create_or_update_menu_embedding.create_or_update_menu_embedding(
        menu_id=menu.id, embedding_service=embedding_service
    )

    assert len(embedding_service.created_embeddings) == 1
    embedding = menu_models.MenuEmbedding.objects.get()
    assert embedding_service.created_embeddings[0] == embedding.to_domain_model()

    menu.name = "Updated name"
    menu.save(update_fields=["name"])

    # Calling the function again should create a new embedding.
    embedding_service = embeddings.FakeEmbeddingService()
    _create_or_update_menu_embedding.create_or_update_menu_embedding(
        menu_id=menu.id, embedding_service=embedding_service
    )
    assert len(embedding_service.created_embeddings) == 1


def test_raises_when_embedding_service_is_unavailable():
    embedding_service = embeddings.BrokenEmbeddingService()
    menu = data_factories.Menu(name="Original name")

    with pytest.raises(_create_or_update_menu_embedding.UnableToGetEmbedding) as exc:
        _create_or_update_menu_embedding.create_or_update_menu_embedding(
            menu_id=menu.id, embedding_service=embedding_service
        )

    assert exc.value.vendor == embedding_service.vendor
    assert exc.value.model == embedding_service.model
