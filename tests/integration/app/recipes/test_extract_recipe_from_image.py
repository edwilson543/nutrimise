import pytest

from nutrimise.app.recipes import _extract_recipe_from_image
from nutrimise.data.recipes import models as recipe_models
from nutrimise.domain import image_extraction
from nutrimise.domain.image_extraction import _vendors as image_extraction_vendors
from testing.factories import data as data_factories
from testing.factories import images as image_factories


def test_extracts_recipe_using_fake_extraction_service():
    author = data_factories.User()
    image = image_factories.get_image()
    image_extraction_service = image_extraction_vendors.FakeImageExtractionService()

    recipe_id = _extract_recipe_from_image.extract_recipe_from_image(
        author=author,
        uploaded_image=image,
        image_extraction_service=image_extraction_service,
    )

    recipe = recipe_models.Recipe.objects.get()
    assert recipe.id == recipe_id
    assert recipe.name == image_extraction_service._canned_recipe.name
    assert recipe.description == image_extraction_service._canned_recipe.description

    # If we extract from the image again, we should get a new recipe rather than an error.
    _extract_recipe_from_image.extract_recipe_from_image(
        author=author,
        uploaded_image=image,
        image_extraction_service=image_extraction_service,
    )

    assert recipe_models.Recipe.objects.count() == 2


def test_raises_embedding_service_errors():
    author = data_factories.User()
    image = image_factories.get_image()
    image_extraction_service = image_extraction_vendors.BrokenImageExtractionService()

    with pytest.raises(image_extraction.UnableToExtractRecipeFromImage) as exc:
        _extract_recipe_from_image.extract_recipe_from_image(
            author=author,
            uploaded_image=image,
            image_extraction_service=image_extraction_service,
        )

    assert exc.value.vendor == image_extraction_service.vendor
    assert exc.value.model == image_extraction_service.model
