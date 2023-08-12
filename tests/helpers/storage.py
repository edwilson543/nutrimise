from __future__ import annotations

# Third party imports
import attrs

# Django imports
from django.core import files
from django.test import override_settings

# Local application imports
from data.recipes import models as recipe_models
from domain.storage import _config as storage_config

PUBLIC_IMAGE_SOURCE = "media/some-url.jpg"

install_test_file_storage = override_settings(
    FILE_STORAGE_CLASS="tests.helpers.storage.TestFileStorage"
)


@attrs.frozen
class StorageContext(storage_config.StorageContext):
    key: str

    @classmethod
    def for_recipe(cls, recipe: recipe_models.Recipe) -> StorageContext:
        return cls(key=f"recipe-{recipe.id}")

    @classmethod
    def from_recipe_image(
        cls, recipe_image: recipe_models.RecipeImage
    ) -> StorageContext:
        return cls(key=f"recipe-{recipe_image.recipe.id}")


class TestFileStorage(storage_config.FileStorage[StorageContext]):
    """
    Implementation of file storage for testing purposes.
    """

    context_class = StorageContext

    # Create an in memory upload store
    uploaded_files: dict[str, files.File] = {}

    def upload(self, *, file: files.File, storage_context: StorageContext) -> None:
        self.uploaded_files[storage_context.key] = file

    def get_public_source(self, *, storage_context: StorageContext) -> str:
        return PUBLIC_IMAGE_SOURCE

    def delete(self, *, storage_context: StorageContext) -> None:
        if storage_context.key in self.uploaded_files:
            self.uploaded_files.pop(storage_context.key)
        else:
            raise storage_config.UnableToDeleteFile
