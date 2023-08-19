# Local application imports
from domain.recipes import queries
from tests import factories
from tests.helpers import storage as storage_helpers


class TestGetImageSource:
    @storage_helpers.install_test_file_storage
    def test_gets_image_source_local_storage(self):
        recipe_image = factories.RecipeImage.build()

        image_source = queries.get_image_source(recipe_image=recipe_image)

        assert image_source == storage_helpers.PUBLIC_IMAGE_SOURCE
