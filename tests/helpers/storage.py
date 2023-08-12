from __future__ import annotations

# Third party imports
import attrs

# Django imports
from django.core import files

# Local application imports
from data.recipes import models as recipe_models
from domain.storage import _config as storage_config


@attrs.frozen
class StorageContext(storage_config.StorageContext):
    key: str

    @classmethod
    def for_recipe(cls, recipe: recipe_models.Recipe) -> StorageContext:
        return cls(key=f"key-recipe-{recipe.id}")

    @classmethod
    def from_recipe_image(
        cls, recipe_image: recipe_models.RecipeImage
    ) -> StorageContext:
        return cls(key=f"key-image-{recipe_image.id}")


class TestFileStorage(storage_config.FileStorage[StorageContext]):
    """
    Implementation of file storage for testing purposes.
    """

    context_class = StorageContext

    # Create an in memory upload store
    uploaded_files: dict[str, files.File] = {}

    def upload(self, file: files.File) -> None:
        self.uploaded_files[self.storage_context.key] = file

    def get_public_source(self) -> str:
        if self.storage_context.key in self.uploaded_files:
            return f"some-url/{self.uploaded_files['key'].file}"
        raise storage_config.UnableToUploadFile

    def delete(self) -> None:
        if self.storage_context.key in self.uploaded_files:
            self.uploaded_files.pop(self.storage_context.key)
        else:
            raise storage_config.UnableToDeleteFile
