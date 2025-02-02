from nutrimise.domain import embeddings

from . import models as recipe_models


def create_or_update_recipe_embedding(
    *, recipe_id: int, embedding: embeddings.Embedding
) -> None:
    recipe_models.RecipeEmbedding.objects.update_or_create(
        recipe_id=recipe_id,
        model=embedding.model.value,
        vendor=embedding.vendor.value,
        defaults={
            "vector": embedding.vector,
            "embedded_content_hash": embedding.embedded_content_hash,
        },
    )
