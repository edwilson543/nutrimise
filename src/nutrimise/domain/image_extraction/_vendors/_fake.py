import attrs

from nutrimise.domain.image_extraction import _constants, _output_structure

from . import _base


def _get_canned_recipe() -> _output_structure.Recipe:
    return _output_structure.Recipe(
        name="My fake recipe", description="Description for the fake recipe"
    )


@attrs.frozen
class FakeImageExtractService(_base.ImageExtractionService):
    model: _constants.ImageExtractionModel = _constants.ImageExtractionModel.FAKE
    vendor: _constants.ImageExtractionVendor = _constants.ImageExtractionVendor.FAKE

    _canned_recipe: _output_structure.Recipe = attrs.field(factory=_get_canned_recipe)

    def extract_recipe_from_image(
        self, *, base64_image: str
    ) -> _output_structure.Recipe:
        return self._canned_recipe
