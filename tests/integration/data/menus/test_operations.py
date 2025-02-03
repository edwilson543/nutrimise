import numpy as np

from nutrimise.data.menus import models as menu_models
from nutrimise.data.menus import operations as menu_operations
from nutrimise.domain import embeddings
from testing.factories import data as data_factories
from testing.factories import domain as domain_factories


class TestUpdateMenuItemRecipe:
    def test_updates_menu_item_recipe(self):
        recipe = data_factories.Recipe()
        menu_item = data_factories.MenuItem(recipe_id=None)

        menu_operations.update_menu_item_recipe(
            menu_item_id=menu_item.id, recipe_id=recipe.id
        )

        menu_item.refresh_from_db()
        assert menu_item.recipe == recipe


class TestCreateOrUpdateMenuEmbedding:
    def test_creates_new_embedding_for_menu_with_model(self):
        menu = data_factories.Menu()
        embedding = domain_factories.Embedding()
        assert not menu_models.MenuEmbedding.objects.exists()

        menu_operations.create_or_update_menu_embedding(
            menu_id=menu.id, embedding=embedding
        )

        persisted_embedding = menu_models.MenuEmbedding.objects.get()
        assert persisted_embedding.to_domain_model() == embedding

    def test_updates_existing_embedding_for_menu_with_model(self):
        original_embedding = data_factories.MenuEmbedding.create(
            vector=np.zeros(embeddings.EMBEDDING_DIMENSIONS),
            vendor=embeddings.EmbeddingVendor.OPENAI.value,
            model=embeddings.EmbeddingModel.TEXT_EMBEDDING_3_SMALL,
        )

        updated_embedding = embeddings.Embedding(
            vector=np.ones(embeddings.EMBEDDING_DIMENSIONS),
            embedded_content_hash="ABC123",
            vendor=embeddings.EmbeddingVendor(original_embedding.vendor),
            model=embeddings.EmbeddingModel(original_embedding.model),
        )

        menu_operations.create_or_update_menu_embedding(
            menu_id=original_embedding.menu_id, embedding=updated_embedding
        )

        persisted_embedding = menu_models.MenuEmbedding.objects.get()
        assert persisted_embedding.to_domain_model() == updated_embedding
