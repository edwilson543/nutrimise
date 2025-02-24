import pytest

from nutrimise.data.recipes import queries as recipe_queries
from nutrimise.domain import embeddings, recipes
from testing.factories import data as data_factories
from testing.factories import domain as domain_factories


class TestGetRecipe:
    def test_gets_recipe_when_exists(self):
        recipe = data_factories.Recipe()

        result = recipe_queries.get_recipe(recipe_id=recipe.id)

        assert isinstance(result, recipes.Recipe)
        assert result.id == recipe.id

    def test_raises_when_recipe_does_not_exist(self):
        with pytest.raises(recipe_queries.RecipeDoesNotExist) as exc:
            recipe_queries.get_recipe(recipe_id=123)

        assert exc.value.recipe_id == 123


class TestGetRecipes:
    def test_gets_all_recipes(self):
        data_factories.Recipe()
        data_factories.Recipe()

        result = recipe_queries.get_recipes()

        assert len(result) == 2

    def test_only_gets_recipe_matching_passed_ids(self):
        recipe = data_factories.Recipe()
        data_factories.Recipe()

        result = recipe_queries.get_recipes(recipe_ids=(recipe.id,))

        assert result == (recipe.to_domain_model(),)

    def test_only_gets_recipes_meeting_single_dietary_requirement(self):
        dietary_requirement = data_factories.DietaryRequirement()
        matching_recipe = data_factories.Recipe.create_to_satisfy_dietary_requirements(
            dietary_requirements=(dietary_requirement,)
        )

        # Some non-matching recipes.
        data_factories.Recipe()
        data_factories.Recipe.create_to_satisfy_dietary_requirements(
            dietary_requirements=(data_factories.DietaryRequirement(),)
        )

        result = recipe_queries.get_recipes(
            dietary_requirement_ids=(dietary_requirement.id,)
        )

        assert len(result) == 1
        assert result[0].id == matching_recipe.id

    def test_only_gets_recipes_meeting_multiple_dietary_requirements(self):
        veggie = data_factories.DietaryRequirement()
        gluten_free = data_factories.DietaryRequirement()

        matching_recipe = data_factories.Recipe.create_to_satisfy_dietary_requirements(
            dietary_requirements=(veggie, gluten_free)
        )
        # Make some recipes that are just veggie / gluten-free.
        data_factories.Recipe.create_to_satisfy_dietary_requirements(
            dietary_requirements=(veggie,)
        )
        data_factories.Recipe.create_to_satisfy_dietary_requirements(
            dietary_requirements=(gluten_free,)
        )

        result = recipe_queries.get_recipes(
            dietary_requirement_ids=(veggie.id, gluten_free.id)
        )
        data_factories.Recipe()

        assert len(result) == 1
        assert result[0].id == matching_recipe.id

    def test_gets_empty_tuple_when_there_are_no_recipes(self):
        result = recipe_queries.get_recipes()

        assert result == ()


class TestGetRecipesOrderedByDistanceToVector:
    def test_gets_recipes_with_embedding_closest_to_matching_vector(self):
        padding = [0] * (embeddings.EMBEDDING_DIMENSIONS - 2)
        embedding = domain_factories.Embedding(vector=[1, 0] + padding)

        closest = data_factories.RecipeEmbedding(
            vector=[1, 1] + padding,
            vendor=embedding.vendor.value,
            model=embedding.model.value,
        )
        next_closest = data_factories.RecipeEmbedding(
            vector=[1, 2] + padding,
            vendor=embedding.vendor.value,
            model=embedding.model.value,
        )

        # Create an embedding for the correct vendor / model, but with a greater L2 distance.
        data_factories.RecipeEmbedding(
            vector=[1, 3] + padding,
            vendor=embedding.vendor.value,
            model=embedding.model.value,
        )

        # Create an embedding with the same vector as the test embedding but for the wrong vendor.
        data_factories.RecipeEmbedding(
            vector=embedding.vector, vendor="Some other vendor"
        )

        result = recipe_queries.get_recipes_closest_to_vector(
            embedding=embedding, limit=2
        )

        assert list(result) == [closest.recipe, next_closest.recipe]
