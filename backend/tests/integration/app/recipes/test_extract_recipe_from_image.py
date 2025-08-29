import pytest

from nutrimise.app.recipes import _exceptions, _extract_recipe_from_image
from nutrimise.data.ingredients import models as ingredient_models
from nutrimise.data.recipes import models as recipe_models
from nutrimise.domain import data_extraction, embeddings
from nutrimise.domain.data_extraction import _vendors as data_extraction_vendors
from testing.factories import data as data_factories
from testing.factories import domain as domain_factories
from testing.factories import images as image_factories


def test_extracts_recipe_with_author_using_fake_extraction_service():
    author = data_factories.RecipeAuthor()
    image = image_factories.get_image()

    # Create a recipe for the fake data extraction service.
    recipe_ingredient = data_extraction.RecipeIngredient.from_domain_model(
        domain_factories.RecipeIngredient()
    )
    canned_recipe = data_extraction_vendors.get_canned_recipe(
        ingredients=[recipe_ingredient]
    )
    data_extraction_service = data_extraction_vendors.FakeDataExtractionService(
        canned_recipe=canned_recipe
    )

    embedding_service = embeddings.FakeEmbeddingService()

    recipe_id = _extract_recipe_from_image.extract_recipe_from_image(
        author=author,
        image=image,
        data_extraction_service=data_extraction_service,
        embedding_service=embedding_service,
    )

    new_ingredient_category = ingredient_models.IngredientCategory.objects.get()
    assert new_ingredient_category.name == recipe_ingredient.ingredient.category_name

    new_ingredient = ingredient_models.Ingredient.objects.get()
    assert new_ingredient.name == recipe_ingredient.ingredient.name
    assert new_ingredient.category.id == new_ingredient_category.id
    assert new_ingredient_category.name == recipe_ingredient.ingredient.category_name

    recipe = recipe_models.Recipe.objects.get()
    assert recipe.id == recipe_id
    assert recipe.name == data_extraction_service.canned_recipe.name
    assert recipe.description == data_extraction_service.canned_recipe.description

    recipe_ingredient = recipe.ingredients.get()
    assert recipe_ingredient.ingredient_id == new_ingredient.id
    assert recipe_ingredient.quantity == recipe_ingredient.quantity

    recipe_embedding = recipe.embeddings.get()
    assert recipe_embedding.vendor == embedding_service.vendor.value


def test_extracts_recipe_without_author_using_fake_extraction_service():
    image = image_factories.get_image()
    data_extraction_service = data_extraction_vendors.FakeDataExtractionService()

    recipe_id = _extract_recipe_from_image.extract_recipe_from_image(
        author=None,
        image=image,
        data_extraction_service=data_extraction_service,
        embedding_service=embeddings.FakeEmbeddingService(),
    )

    recipe = recipe_models.Recipe.objects.get()
    assert recipe.id == recipe_id
    assert recipe.author_id is None


def test_raises_if_extracted_recipe_is_not_unique_for_author():
    image = image_factories.get_image()
    data_extraction_service = data_extraction_vendors.FakeDataExtractionService()
    embedding_service = embeddings.FakeEmbeddingService()

    author = data_factories.RecipeAuthor()
    canned_recipe = data_extraction_service.canned_recipe
    data_factories.Recipe(name=canned_recipe.name, author=author)

    with pytest.raises(_exceptions.RecipeAlreadyExists) as exc:
        _extract_recipe_from_image.extract_recipe_from_image(
            author=author,
            image=image,
            data_extraction_service=data_extraction_service,
            embedding_service=embedding_service,
        )

    assert exc.value.name == canned_recipe.name
    assert exc.value.author_id == author.id


def test_raises_when_extraction_service_errors():
    image = image_factories.get_image()
    data_extraction_service = data_extraction_vendors.BrokenDataExtractionService()

    with pytest.raises(data_extraction.UnableToExtractRecipe) as exc:
        _extract_recipe_from_image.extract_recipe_from_image(
            author=None,
            image=image,
            data_extraction_service=data_extraction_service,
            embedding_service=embeddings.FakeEmbeddingService(),
        )

    assert exc.value.vendor == data_extraction_service.vendor
    assert exc.value.model == data_extraction_service.model
