import numpy as np

from nutrimise.data.recipes import models as recipe_models
from nutrimise.data.recipes import operations as recipe_operations
from nutrimise.domain import constants, embeddings
from testing.factories import data as data_factories
from testing.factories import domain as domain_factories


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


class TestCreateRecipe:
    def test_creates_recipe_with_unique_name_for_author(self):
        author = data_factories.User()

        recipe_id = recipe_operations.create_recipe(
            author=author,
            name="Chicken curry",
            description="Saagfest",
            meal_times=[constants.MealTime.LUNCH],
            number_of_servings=3,
        )

        recipe = recipe_models.Recipe.objects.get()
        assert recipe.id == recipe_id
        assert recipe.author_id == author.id
        assert recipe.name == "Chicken curry"
        assert recipe.description == "Saagfest"
        assert recipe.meal_times == ["LUNCH"]
        assert recipe.number_of_servings == 3

    def test_creates_recipe_with_duplicate_name_for_author(self):
        recipe = data_factories.Recipe()

        new_recipe_id = recipe_operations.create_recipe(
            author=recipe.author,
            name=recipe.name,
            description="Saagfest",
            meal_times=[constants.MealTime.LUNCH],
            number_of_servings=3,
        )

        assert recipe_models.Recipe.objects.count() == 2
        new_recipe = recipe_models.Recipe.objects.exclude(id=recipe.id).get()
        assert new_recipe.id == new_recipe_id
        assert new_recipe.name.startswith(f"{recipe.name} (duplicate")

    def test_different_authors_can_have_duplicate_recipe_names(self):
        author = data_factories.User()
        recipe = data_factories.Recipe(author=author)

        other_author = data_factories.User()

        new_recipe_id = recipe_operations.create_recipe(
            author=other_author,
            name=recipe.name,
            description=recipe.description,
            meal_times=[constants.MealTime.LUNCH],
            number_of_servings=3,
        )

        assert recipe_models.Recipe.objects.count() == 2
        new_recipe = recipe_models.Recipe.objects.exclude(id=recipe.id).get()
        assert new_recipe.id == new_recipe_id
        assert new_recipe.name == recipe.name
