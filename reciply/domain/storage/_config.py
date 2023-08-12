from __future__ import annotations

# Standard library imports
import abc
from typing import Generic, TypeVar

# Third party imports
import attrs

# Django imports
from django.conf import settings
from django.core import files
from django.utils import module_loading

# Local application imports
from data.recipes import models as recipe_models


class _StorageError(Exception):
    pass


class UnableToUploadFile(_StorageError):
    pass


class UnableToLocateFile(_StorageError):
    pass


class UnableToDeleteFile(_StorageError):
    pass


class StorageContext:
    """
    Store and generate the context for some file storage operation.
    """

    def serialize(self) -> dict[str, str]:
        return attrs.asdict(self)

    @classmethod
    @abc.abstractmethod
    def for_recipe(cls, recipe: recipe_models.Recipe) -> StorageContext:
        """
        Get the storage context for some new recipe image.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def from_recipe_image(cls, recipe: recipe_models.RecipeImage) -> StorageContext:
        """
        Get the storage context for some existing recipe image.
        """
        pass


StorageContextType = TypeVar("StorageContextType", bound=StorageContext)


class FileStorage(abc.ABC, Generic[StorageContextType]):
    """
    Interact with a file persistence system to perform CRUD operations.
    """

    context_class: StorageContextType

    def __init__(self, storage_context: StorageContextType) -> None:
        self.storage_context = storage_context

    @abc.abstractmethod
    def upload(self, file: files.File) -> None:
        """
        Persist some new file in storage.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_public_source(self) -> str:
        """
        Get the URL from which some file can be publicly accessed.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self) -> None:
        """
        Delete the file from persisted storage.
        """
        raise NotImplementedError


def get_file_storage_class() -> type[FileStorage]:
    """
    Return a concrete instance of the FileStorage class.
    """
    return module_loading.import_string(settings.FILE_STORAGE_CLASS)  # type: ignore[misc]
