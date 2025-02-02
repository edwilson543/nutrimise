import numpy as np

from nutrimise.data.recipes import models as recipe_models
from nutrimise.data.recipes import operations as recipe_operations
from nutrimise.domain import embeddings
from tests.factories import data as data_factories


class TestCreateOrUpdateRecipeEmbedding:
    def test_creates_new_embedding_for_recipe_with_model(self):
        recipe = data_factories.Recipe()
        embedding = data_factories.RecipeEmbedding.build().to_domain_model()
        assert not recipe_models.RecipeEmbedding.objects.exists()

        recipe_operations.create_or_update_recipe_embedding(
            recipe_id=recipe.id, embedding=embedding
        )

        persisted_embedding = recipe_models.RecipeEmbedding.objects.get()
        assert persisted_embedding.to_domain_model() == embedding

    def test_updates_existing_embedding_for_recipe_with_model(self):
        original_embedding = data_factories.RecipeEmbedding.create(
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

        recipe_operations.create_or_update_recipe_embedding(
            recipe_id=original_embedding.recipe_id, embedding=updated_embedding
        )

        persisted_embedding = recipe_models.RecipeEmbedding.objects.get()
        assert persisted_embedding.to_domain_model() == updated_embedding
