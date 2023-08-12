from __future__ import annotations

# Standard library imports
import dataclasses
import enum
import io
import pathlib
import typing
import uuid

# Django imports
from django.conf import settings

# Local application imports
from data.recipes import models as recipe_models
from domain.storage import _config as storage_config


class Namespace(enum.StrEnum):
    RECIPES = "recipes"


@dataclasses.dataclass(frozen=True)
class StorageContext(storage_config.StorageContext):
    namespace: Namespace
    filename: str

    @classmethod
    def for_recipe(cls, recipe: recipe_models.Recipe) -> StorageContext:
        return cls(
            namespace=Namespace.RECIPES,
            filename=f"recipe-{recipe.id}-{uuid.uuid4()}.jpg",
        )

    @classmethod
    def from_recipe_image(
        cls, recipe_image: recipe_models.RecipeImage
    ) -> StorageContext:
        return cls(
            namespace=recipe_image.storage_context.get("namespace", ""),
            filename=recipe_image.storage_context.get("filename", ""),
        )

    @property
    def directory(self) -> pathlib.Path:
        return typing.cast(pathlib.Path, settings.MEDIA_ROOT) / self.namespace

    @property
    def filepath(self) -> pathlib.Path:
        return self.directory / self.filename


class LocalFileStorage(storage_config.FileStorage[StorageContext]):
    """
    Implementation of file storage for testing purposes.
    """

    context_class = StorageContext

    def upload(self, *, file: io.BytesIO, storage_context: StorageContext) -> None:
        if not storage_context.directory.is_dir():
            pathlib.Path.mkdir(storage_context.directory, parents=True)
        with open(storage_context.filepath, mode="wb") as new_file:
            new_file.write(file.getbuffer())

    def get_public_source(self, *, storage_context: StorageContext) -> str:
        if (
            typing.cast(pathlib.Path, settings.MEDIA_ROOT)
            / storage_context.namespace
            / storage_context.filename
        ).is_file():
            return f"{settings.MEDIA_BASE_URL}/{storage_context.namespace}/{storage_context.filename}"  # type: ignore[misc]
        raise storage_config.UnableToLocateFile

    def delete(self, *, storage_context: StorageContext) -> None:
        raise NotImplementedError
