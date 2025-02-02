from nutrimise.data.recipes import operations as recipe_operations
from nutrimise.data.recipes import queries as recipe_queries
from nutrimise.domain import embeddings, recipes


UnableToGetEmbedding = embeddings.UnableToGetEmbedding


def create_or_update_recipe_embedding(
    *, recipe_id: int, embedding_service: embeddings.EmbeddingService
) -> None:
    """
    Ensure the recipe has an up-to-date embedding for the installed embedding service.

    raises UnableToGetEmbedding: If the service is unable to produce an embedding
        for some reason.
    """
    recipe = recipe_queries.get_recipe(recipe_id=recipe_id)
    text = _get_text_from_recipe(recipe)

    if _has_recipe_already_been_embedded(
        recipe=recipe, text=text, embedding_service=embedding_service
    ):
        return

    embedding = embedding_service.get_embedding(text=text)
    recipe_operations.create_or_update_recipe_embedding(
        recipe_id=recipe_id, embedding=embedding
    )


def _get_text_from_recipe(recipe: recipes.Recipe) -> str:
    text = f"Recipe: {recipe.name}"
    if recipe.description:
        text += f"\nDescription: {recipe.description}"
    return text


def _has_recipe_already_been_embedded(
    *, recipe: recipes.Recipe, text: str, embedding_service: embeddings.EmbeddingService
) -> bool:
    hashed_text = embeddings.get_hash_for_text(text=text)

    for embedding in recipe.embeddings:
        if (
            embedding.vendor == embedding_service.vendor
            and embedding.model == embedding_service.model
            and embedding.embedded_content_hash == hashed_text
        ):
            return True

    return False
