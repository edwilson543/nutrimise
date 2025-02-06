import base64
import io

from django.contrib.auth import models as auth_models
from PIL import Image

from nutrimise.data.recipes import operations as recipe_operations
from nutrimise.domain import image_extraction


def extract_image_from_recipe(
    *,
    uploaded_image: Image.Image,
    image_extraction_service: image_extraction.ImageExtractionService,
    author: auth_models.User,
) -> int:
    buffered = io.BytesIO()
    uploaded_image.save(buffered, format="JPEG")
    base64_image = base64.b64encode(buffered.getvalue())

    recipe = image_extraction_service.extract_recipe_from_image(
        base64_image=base64_image.decode("utf-8")
    )

    recipe_id = recipe_operations.create_recipe(
        name=recipe.name, description=recipe.description, author=author
    )

    return recipe_id


if __name__ == "__main__":
    uploaded_image = Image.open("download.jpeg")
    print("Pillow image: ", uploaded_image)

    buffered = io.BytesIO()
    uploaded_image.save(buffered, format="JPEG")
    base64_image = base64.b64encode(buffered.getvalue())

    print("B64 image: ", str(base64_image))
