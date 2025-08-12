import numpy as np
import pytest

from nutrimise.data.recipes import models as recipe_models
from nutrimise.data.recipes import operations as recipe_operations
from nutrimise.domain import embeddings, recipes
from testing.factories import data as data_factories
from testing.factories import domain as domain_factories


class TestCreateRecipe:
    def test_creates_recipe_with_unique_name_for_author(self):
        author = data_factories.RecipeAuthor()

        ingredient = data_factories.Ingredient()
        recipe_ingredient = domain_factories.RecipeIngredient(
            ingredient=ingredient.to_domain_model()
        )

        other_ingredient = data_factories.Ingredient()
        other_recipe_ingredient = domain_factories.RecipeIngredient(
            ingredient=other_ingredient.to_domain_model()
        )

        recipe_id = recipe_operations.create_recipe(
            author=author,
            name="Chicken curry",
            description="Saagfest",
            methodology="Put saag in fest",
            meal_times=[recipes.MealTime.LUNCH],
            number_of_servings=3,
            recipe_ingredients=[recipe_ingredient, other_recipe_ingredient],
        )

        recipe = recipe_models.Recipe.objects.get()
        assert recipe.id == recipe_id
        assert recipe.author_id == author.id
        assert recipe.name == "Chicken curry"
        assert recipe.description == "Saagfest"
        assert recipe.methodology == "Put saag in fest"
        assert recipe.meal_times == ["LUNCH"]
        assert recipe.number_of_servings == 3

        assert recipe.ingredients.count() == 2
        first_ingredient = recipe.ingredients.get(ingredient_id=ingredient.id)
        assert first_ingredient.quantity == recipe_ingredient.quantity
        second_ingredient = recipe.ingredients.get(ingredient_id=other_ingredient.id)
        assert second_ingredient.quantity == other_recipe_ingredient.quantity

    def test_raises_when_recipe_already_exists_for_author(self):
        author = data_factories.RecipeAuthor.create()
        existing_recipe = data_factories.Recipe(author=author)

        with pytest.raises(recipe_operations.RecipeAlreadyExists) as exc:
            recipe_operations.create_recipe(
                author=author.to_domain_model(),
                name=existing_recipe.name,
                description="",
                methodology="",
                meal_times=[recipes.MealTime.LUNCH],
                number_of_servings=3,
                recipe_ingredients=[],
            )

        assert exc.value.name == existing_recipe.name
        assert exc.value.author_id == existing_recipe.author_id

    def test_raises_when_recipe_already_exists_for_anonymous_author(self):
        existing_recipe = data_factories.Recipe(author=None)

        with pytest.raises(recipe_operations.RecipeAlreadyExists) as exc:
            recipe_operations.create_recipe(
                author=None,
                name=existing_recipe.name,
                description="",
                methodology="",
                meal_times=[recipes.MealTime.LUNCH],
                number_of_servings=3,
                recipe_ingredients=[],
            )

        assert exc.value.name == existing_recipe.name
        assert exc.value.author_id is None

    def test_different_authors_can_have_duplicate_recipe_names(self):
        author = data_factories.RecipeAuthor()
        recipe = data_factories.Recipe(author=author)

        other_author = data_factories.RecipeAuthor()

        new_recipe_id = recipe_operations.create_recipe(
            author=other_author,
            name=recipe.name,
            description=recipe.description,
            methodology=recipe.methodology,
            meal_times=[recipes.MealTime.LUNCH],
            number_of_servings=3,
            recipe_ingredients=[],
        )

        assert recipe_models.Recipe.objects.count() == 2
        new_recipe = recipe_models.Recipe.objects.exclude(id=recipe.id).get()
        assert new_recipe.id == new_recipe_id
        assert new_recipe.name == recipe.name

    def test_ignores_conflicting_ingredients(self):
        ingredient = data_factories.Ingredient()
        recipe_ingredient = domain_factories.RecipeIngredient(
            ingredient=ingredient, quantity=10.0
        )
        other_recipe_ingredient = domain_factories.RecipeIngredient(
            ingredient=ingredient, quantity=20.0
        )

        recipe_operations.create_recipe(
            author=None,
            name="Some name",
            description="Some description",
            methodology="",
            meal_times=[recipes.MealTime.DINNER],
            number_of_servings=3,
            recipe_ingredients=[recipe_ingredient, other_recipe_ingredient],
        )

        recipe = recipe_models.Recipe.objects.get()
        created_ingredient = recipe.ingredients.get()
        assert created_ingredient.ingredient_id == ingredient.id
        assert created_ingredient.quantity == recipe_ingredient.quantity


class TestCreateOrUpdateRecipeEmbedding:
    def test_creates_new_embedding_for_recipe_with_model(self):
        recipe = data_factories.Recipe()
        embedding = domain_factories.Embedding()
        assert not recipe_models.RecipeEmbedding.objects.exists()

        recipe_operations.create_or_update_recipe_embedding(
            recipe_id=recipe.id, embedding=embedding
        )

        persisted_embedding = recipe_models.RecipeEmbedding.objects.get()
        assert persisted_embedding.to_domain_model() == embedding

    def test_updates_existing_embedding_for_recipe_with_model(self):
        original_embedding = data_factories.RecipeEmbedding.create(
            vector=np.zeros(embeddings.EMBEDDING_DIMENSIONS),
            vendor=embeddings.EmbeddingVendor.OPENAI.value,
            model=embeddings.EmbeddingModel.TEXT_EMBEDDING_3_SMALL,
        )

        updated_embedding = embeddings.Embedding(
            vector=np.ones(embeddings.EMBEDDING_DIMENSIONS),
            prompt_hash="ABC123",
            vendor=embeddings.EmbeddingVendor(original_embedding.vendor),
            model=embeddings.EmbeddingModel(original_embedding.model),
        )

        recipe_operations.create_or_update_recipe_embedding(
            recipe_id=original_embedding.recipe_id, embedding=updated_embedding
        )

        persisted_embedding = recipe_models.RecipeEmbedding.objects.get()
        assert persisted_embedding.to_domain_model() == updated_embedding


class TestGetOrCreateRecipeAuthor:
    @pytest.mark.parametrize(
        "first_name,last_name",
        [
            ("WES", "HOOLAHAN"),
            ("wes", "hoolahan"),
            ("WES", "hoolahan"),
            ("wes", "HOOLAHAN"),
        ],
    )
    def test_gets_recipe_author(self, first_name: str, last_name: str):
        author = data_factories.RecipeAuthor.create(
            first_name=first_name, last_name=last_name
        )

        new_author = recipe_operations.get_or_create_recipe_author(
            first_name=author.first_name.lower(),
            last_name=author.last_name.lower(),
        )

        assert author.id == new_author.id

    def test_creates_recipe_author(self):
        existing_author = data_factories.RecipeAuthor(
            first_name="Wes", last_name="Hoolahan"
        )

        new_author = recipe_operations.get_or_create_recipe_author(
            first_name="Wes",
            last_name="Carewlaland",
        )

        assert existing_author.id != new_author
        new_author = recipe_models.RecipeAuthor.objects.get(id=new_author.id)
        assert new_author.first_name == "Wes"
        assert new_author.last_name == "Carewlaland"
