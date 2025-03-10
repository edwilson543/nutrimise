import abc

import attrs

from nutrimise.domain.data_extraction import _constants, _output_structure


@attrs.frozen
class DataExtractionServiceMisconfigured(Exception):
    vendor: _constants.DataExtractionVendor


@attrs.frozen
class UnableToExtractRecipe(Exception):
    vendor: _constants.DataExtractionVendor
    model: _constants.DataExtractionModel


@attrs.frozen
class UnableToExtractIngredientNutritionalInformation(Exception):
    vendor: _constants.DataExtractionVendor
    model: _constants.DataExtractionModel


@attrs.frozen
class DataExtractionService(abc.ABC):
    model: _constants.DataExtractionModel
    vendor: _constants.DataExtractionVendor

    @abc.abstractmethod
    def extract_recipe_from_image(
        self,
        *,
        base64_image: str,
        existing_ingredients: list[_output_structure.Ingredient],
    ) -> _output_structure.Recipe:
        """
        Extract structured recipe data from the passed image.

        :raises UnableToExtractRecipe: If the service is unable to extract the image
            for some reason.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def extract_recipe_from_url(
        self,
        *,
        url: str,
        existing_ingredients: list[_output_structure.Ingredient],
    ) -> _output_structure.Recipe:
        """
        Extract structure recipe data from the webpage at the given URL.

        :raises UnableToExtractRecipe: If the service is unable to access or extract
            the data for some reason.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def extract_ingredient_nutritional_information(
        self,
        *,
        ingredients: list[_output_structure.Ingredient],
        nutrients: list[_output_structure.Nutrient],
    ) -> list[_output_structure.IngredientNutritionalInformation]:
        """
        Get the quantity of each nutrient in each ingredient.

        :raises UnableToExtractIngredientNutritionalInformation: If the service is unable
            to extract the information for some reason.
        """
        raise NotImplementedError
