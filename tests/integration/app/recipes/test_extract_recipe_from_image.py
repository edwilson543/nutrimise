import pytest

from nutrimise.app.recipes import _extract_recipe_from_image
from nutrimise.data.ingredients import models as ingredient_models
from nutrimise.data.recipes import models as recipe_models
from nutrimise.domain import image_extraction
from nutrimise.domain.image_extraction import _vendors as image_extraction_vendors
from testing.factories import data as data_factories
from testing.factories import domain as domain_factories
from testing.factories import images as image_factories


def test_extracts_recipe_using_fake_extraction_service():
    recipe_ingredient = image_extraction.RecipeIngredient.from_domain_model(
        domain_factories.RecipeIngredient()
    )
    canned_recipe = image_extraction_vendors.get_canned_recipe(
        ingredients=[recipe_ingredient]
    )

    author = data_factories.RecipeAuthor()
    image = image_factories.get_image()
    image_extraction_service = image_extraction_vendors.FakeImageExtractionService(
        canned_recipe=canned_recipe
    )

    recipe_id = _extract_recipe_from_image.extract_recipe_from_image(
        author=author,
        uploaded_image=image,
        image_extraction_service=image_extraction_service,
    )

    new_ingredient_category = ingredient_models.IngredientCategory.objects.get()
    assert new_ingredient_category.name == recipe_ingredient.ingredient.category_name

    new_ingredient = ingredient_models.Ingredient.objects.get()
    assert new_ingredient.name == recipe_ingredient.ingredient.name
    assert new_ingredient.category.id == new_ingredient_category.id
    assert new_ingredient_category.name == recipe_ingredient.ingredient.category_name

    recipe = recipe_models.Recipe.objects.get()
    assert recipe.id == recipe_id
    assert recipe.name == image_extraction_service.canned_recipe.name
    assert recipe.description == image_extraction_service.canned_recipe.description

    recipe_ingredient = recipe.ingredients.get()
    assert recipe_ingredient.ingredient_id == new_ingredient.id
    assert recipe_ingredient.quantity == recipe_ingredient.quantity


def test_creates_duplicate_recipe_if_image_extraction_model_returns_existing_name():
    author = data_factories.RecipeAuthor()
    image = image_factories.get_image()
    image_extraction_service = image_extraction_vendors.FakeImageExtractionService()

    recipe_id = _extract_recipe_from_image.extract_recipe_from_image(
        author=author,
        uploaded_image=image,
        image_extraction_service=image_extraction_service,
    )

    recipe = recipe_models.Recipe.objects.get()
    assert recipe.id == recipe_id
    assert recipe.name == image_extraction_service.canned_recipe.name
    assert recipe.description == image_extraction_service.canned_recipe.description

    # If we extract from the image again, we should get a new recipe rather than an error.
    _extract_recipe_from_image.extract_recipe_from_image(
        author=author,
        uploaded_image=image,
        image_extraction_service=image_extraction_service,
    )

    assert recipe_models.Recipe.objects.count() == 2


def test_raises_embedding_service_errors():
    image = image_factories.get_image()
    image_extraction_service = image_extraction_vendors.BrokenImageExtractionService()

    with pytest.raises(image_extraction.UnableToExtractRecipeFromImage) as exc:
        _extract_recipe_from_image.extract_recipe_from_image(
            author=None,
            uploaded_image=image,
            image_extraction_service=image_extraction_service,
        )

    assert exc.value.vendor == image_extraction_service.vendor
    assert exc.value.model == image_extraction_service.model
