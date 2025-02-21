import attrs

from nutrimise.domain.image_extraction import _constants, _output_structure

from . import _base


@attrs.frozen
class BrokenImageExtractionService(_base.ImageExtractionService):
    model: _constants.ImageExtractionModel = _constants.ImageExtractionModel.FAKE
    vendor: _constants.ImageExtractionVendor = _constants.ImageExtractionVendor.BROKEN

    def extract_recipe_from_image(
        self,
        *,
        base64_image: str,
        existing_ingredients: list[_output_structure.Ingredient],
    ) -> _output_structure.Recipe:
        raise _base.UnableToExtractRecipeFromImage(vendor=self.vendor, model=self.model)

    def extract_ingredient_nutritional_information(
        self,
        *,
        ingredients: list[_output_structure.Ingredient],
        nutrients: list[_output_structure.Nutrient],
    ) -> list[_output_structure.IngredientNutritionalInformation]:
        raise _base.UnableToExtractIngredientNutritionalInformation(
            vendor=self.vendor, model=self.model
        )
