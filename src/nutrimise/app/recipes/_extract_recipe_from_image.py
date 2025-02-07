import base64
import io

from django.contrib.auth import models as auth_models
from PIL import Image

from nutrimise.data.recipes import operations as recipe_operations
from nutrimise.domain import image_extraction


UnableToExtractRecipeFromImage = image_extraction.UnableToExtractRecipeFromImage


def extract_recipe_from_image(
    *,
    author: auth_models.User,
    uploaded_image: Image.Image,
    image_extraction_service: image_extraction.ImageExtractionService,
) -> int:
    """
    Extract a recipe and its components from an image and save it to the database.

    :raises UnableToExtractRecipeFromImage: If the recipe could not be extracted for some reason.
    """
    buffered = io.BytesIO()
    uploaded_image.save(buffered, format=uploaded_image.format)
    base64_image = base64.b64encode(buffered.getvalue())

    recipe = image_extraction_service.extract_recipe_from_image(
        base64_image=base64_image.decode("utf-8")
    )

    recipe_id = recipe_operations.create_recipe(
        author=author,
        name=recipe.name,
        description=recipe.description,
        number_of_servings=recipe.number_of_servings,
        meal_times=recipe.meal_times,
    )

    return recipe_id
