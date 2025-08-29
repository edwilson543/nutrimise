import base64
import io

from django.db import transaction
from PIL import Image

from nutrimise.domain import data_extraction, embeddings, recipes

from . import _create_or_update_recipe_embedding, _extraction_helpers


def extract_recipe_from_image(
    *,
    author: recipes.RecipeAuthor | None,
    image: Image.Image,
    data_extraction_service: data_extraction.DataExtractionService,
    embedding_service: embeddings.EmbeddingService,
) -> int:
    """
    Extract a recipe and its components from an image and save it to the database.

    :raises UnableToExtractRecipe: If the recipe could not be extracted for some reason.
    :raises RecipeAlreadyExists: If a recipe with the extracted name already exists for the
        author.
    """
    buffered = io.BytesIO()
    image.save(buffered, format=image.format)
    base64_image = base64.b64encode(buffered.getvalue())

    existing_ingredients = _extraction_helpers.get_existing_ingredients()

    extracted_recipe = data_extraction_service.extract_recipe_from_image(
        base64_image=base64_image.decode("utf-8"),
        existing_ingredients=existing_ingredients,
    )

    with transaction.atomic():
        recipe_id = _extraction_helpers.persist_extracted_recipe(
            extracted_recipe=extracted_recipe, author=author
        )

    _create_or_update_recipe_embedding.create_or_update_recipe_embedding(
        recipe_id=recipe_id, embedding_service=embedding_service
    )

    return recipe_id
