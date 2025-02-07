import attrs

from nutrimise.domain import constants
from nutrimise.domain.image_extraction import _constants, _output_structure

from . import _base


def get_canned_recipe(
    *, ingredients: list[_output_structure.RecipeIngredient] | None = None
) -> _output_structure.Recipe:
    return _output_structure.Recipe(
        name="My fake recipe",
        description="Description for the fake recipe",
        meal_times=[constants.MealTime.DINNER],
        number_of_servings=3,
        ingredients=ingredients or [],
    )


@attrs.frozen
class FakeImageExtractionService(_base.ImageExtractionService):
    model: _constants.ImageExtractionModel = _constants.ImageExtractionModel.FAKE
    vendor: _constants.ImageExtractionVendor = _constants.ImageExtractionVendor.FAKE

    canned_recipe: _output_structure.Recipe = attrs.field(factory=get_canned_recipe)

    def extract_recipe_from_image(
        self,
        *,
        base64_image: str,
        existing_ingredients: list[_output_structure.Ingredient],
    ) -> _output_structure.Recipe:
        return self.canned_recipe
