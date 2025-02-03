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
    prompt = _get_embedding_prompt_for_recipe(recipe)

    if _has_recipe_already_been_embedded(
        recipe=recipe, prompt=prompt, embedding_service=embedding_service
    ):
        return

    embedding = embedding_service.get_embedding(text=prompt)
    recipe_operations.create_or_update_recipe_embedding(
        recipe_id=recipe_id, embedding=embedding
    )


def _get_embedding_prompt_for_recipe(recipe: recipes.Recipe) -> str:
    prompt = """Create an embedding of this recipe that will be useful for:
    - Sematic search
    - Comparing it with the embeddings of meal plan requirements"""

    prompt += f"Recipe name: {recipe.name}"
    if recipe.description:
        prompt += f"\nRecipe description: {recipe.description}"
    return prompt


def _has_recipe_already_been_embedded(
    *, recipe: recipes.Recipe, prompt: str, embedding_service: embeddings.EmbeddingService
) -> bool:
    hashed_prompt = embeddings.get_hash_for_text(text=prompt)

    for embedding in recipe.embeddings:
        if (
            embedding.vendor == embedding_service.vendor
            and embedding.model == embedding_service.model
            and embedding.embedded_content_hash == hashed_prompt
        ):
            return True

    return False
