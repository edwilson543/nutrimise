import attrs

from nutrimise.domain import recipes
from nutrimise.domain.data_extraction import _constants, _output_structure

from . import _base


def get_canned_recipe(
    *,
    ingredients: list[_output_structure.RecipeIngredient] | None = None,
    author: _output_structure.RecipeAuthor | None = None,
) -> _output_structure.Recipe:
    return _output_structure.Recipe(
        name="My fake recipe",
        description="Description for the fake recipe",
        methodology="Boil em mash em stick em in a stew.",
        meal_times=[recipes.MealTime.DINNER],
        number_of_servings=3,
        ingredients=ingredients or [],
        author=author,
    )


@attrs.frozen
class FakeDataExtractionService(_base.DataExtractionService):
    model: _constants.DataExtractionModel = _constants.DataExtractionModel.FAKE
    vendor: _constants.DataExtractionVendor = _constants.DataExtractionVendor.FAKE

    canned_recipe: _output_structure.Recipe = attrs.field(factory=get_canned_recipe)

    def extract_recipe_from_image(
        self,
        *,
        base64_image: str,
        existing_ingredients: list[_output_structure.Ingredient],
    ) -> _output_structure.Recipe:
        return self.canned_recipe

    def extract_recipe_from_url(
        self, *, url: str, existing_ingredients: list[_output_structure.Ingredient]
    ) -> _output_structure.Recipe:
        return self.canned_recipe

    def extract_ingredient_nutritional_information(
        self,
        *,
        ingredients: list[_output_structure.Ingredient],
        nutrients: list[_output_structure.Nutrient],
    ) -> list[_output_structure.IngredientNutritionalInformation]:
        info_list: list[_output_structure.IngredientNutritionalInformation] = []

        for ingredient in ingredients:
            for nutrient in nutrients:
                assert ingredient.id is not None  # For mypy.
                info = _output_structure.IngredientNutritionalInformation(
                    ingredient_id=ingredient.id,
                    nutrient_id=nutrient.id,
                    nutrient_quantity_per_gram_of_ingredient=1.0,
                )
                info_list.append(info)

        return info_list
