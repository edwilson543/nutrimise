import abc

import attrs

from nutrimise.domain.image_extraction import _constants, _output_structure


@attrs.frozen
class ImageExtractionServiceMisconfigured(Exception):
    vendor: _constants.ImageExtractionVendor


@attrs.frozen
class UnableToExtractRecipeFromImage(Exception):
    vendor: _constants.ImageExtractionVendor
    model: _constants.ImageExtractionModel


@attrs.frozen
class ImageExtractionService(abc.ABC):
    model: _constants.ImageExtractionModel
    vendor: _constants.ImageExtractionVendor

    @abc.abstractmethod
    def extract_recipe_from_image(self, *, base64_image: str) -> _output_structure.Recipe:
        """
        Get an embedding for the passed text.

        :raises UnableToExtractRecipeFromImage: If the service is unable to extract the image
            for some reason.
        """
        raise NotImplementedError
