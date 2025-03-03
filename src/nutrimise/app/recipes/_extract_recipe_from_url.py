from django.db import transaction

from nutrimise.domain import data_extraction, embeddings

from . import _create_or_update_recipe_embedding, _extraction_helpers


def extract_recipe_from_url(
    *,
    url: str,
    data_extraction_service: data_extraction.DataExtractionService,
    embedding_service: embeddings.EmbeddingService,
) -> int:
    """
    Extract a recipe and its components from a URL and save it to the database.

    :raises UnableToExtractRecipe: If the recipe could not be extracted for some reason.
    :raises RecipeAlreadyExists: If a recipe with the extracted name already exists for the
        author.
    """
    existing_ingredients = _extraction_helpers.get_existing_ingredients()
    extracted_recipe = data_extraction_service.extract_recipe_from_url(
        url=url, existing_ingredients=existing_ingredients
    )

    with transaction.atomic():
        recipe_id = _extraction_helpers.persist_extracted_recipe(
            extracted_recipe=extracted_recipe, author=None
        )

    _create_or_update_recipe_embedding.create_or_update_recipe_embedding(
        recipe_id=recipe_id, embedding_service=embedding_service
    )

    return recipe_id
