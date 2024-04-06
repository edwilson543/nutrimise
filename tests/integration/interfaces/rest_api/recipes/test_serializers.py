# Local application imports
from interfaces.rest_api.recipes import serializers
from tests import factories
from tests.helpers import storage as storage_helpers


class TestRecipeDetail:
    @storage_helpers.install_test_file_storage
    def test_serializes_recipe_with_images(self):
        recipe = factories.Recipe()

        hero_image = factories.RecipeImage(recipe=recipe, is_hero=True)
        extra_image = factories.RecipeImage(recipe=recipe, is_hero=False)

        recipe_ingredient = factories.RecipeIngredient(recipe=recipe, quantity=1)

        serialized_recipe = serializers.RecipeDetail(instance=recipe).data

        assert serialized_recipe["id"] == recipe.id

        images = serialized_recipe["images"]
        assert images == [
            {
                "id": hero_image.id,
                "is_hero": True,
                "image_source": storage_helpers.PUBLIC_IMAGE_SOURCE,
            },
            {
                "id": extra_image.id,
                "is_hero": False,
                "image_source": storage_helpers.PUBLIC_IMAGE_SOURCE,
            },
        ]

        ingredients = serialized_recipe["ingredients"]
        assert len(ingredients) == 1
        assert recipe_ingredient.ingredient.name_singular in ingredients[0]

        nutritional_information = serialized_recipe["nutritional_information"]
        assert nutritional_information["protein"] > 0
        assert nutritional_information["carbohydrates"] > 0
