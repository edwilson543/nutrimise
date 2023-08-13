from __future__ import annotations

# Standard library imports
import dataclasses
import enum
import io
import uuid

# Third party imports
import boto3
from boto3 import exceptions as aws_exceptions

# Django imports
from django.conf import settings

# Local application imports
from data.recipes import models as recipe_models
from domain import storage


class Folder(enum.StrEnum):
    RECIPES = "recipes"


@dataclasses.dataclass(frozen=True)
class StorageContext(storage.StorageContext):
    key: str
    bucket: str

    @classmethod
    def for_recipe(cls, recipe: recipe_models.Recipe) -> StorageContext:
        return cls(
            key=f"{Folder.RECIPES}/recipe-{recipe.id}-{uuid.uuid4()}.jpg",
            bucket=settings.AWS_BUCKET_NAME,
        )

    @classmethod
    def from_recipe_image(
        cls, recipe_image: recipe_models.RecipeImage
    ) -> StorageContext:
        return cls(
            key=recipe_image.storage_context.get("key", ""),
            bucket=recipe_image.storage_context.get("bucket", ""),
        )


class S3FileStorage(storage.FileStorage[StorageContext]):
    """
    Implementation of file storage for testing purposes.
    """

    context_class = StorageContext

    def __init__(self) -> None:
        session = boto3.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION_NAME,
        )
        self.client = session.client("s3")
        self.resource = session.resource("s3")

    def upload(self, *, file: io.BytesIO, storage_context: StorageContext) -> None:
        if storage_context.key and storage_context.bucket:
            try:
                self.client.put_object(
                    Body=file,
                    Bucket=storage_context.bucket,
                    Key=storage_context.key,
                )
            except aws_exceptions.S3UploadFailedError:
                raise storage.UnableToUploadFile
        else:
            raise storage.UnableToUploadFile

    def get_public_source(self, *, storage_context: StorageContext) -> str:
        if not (storage_context.bucket and storage_context.key):
            raise storage.UnableToLocateFile
        return f"https://s3-{settings.AWS_REGION_NAME}.amazonaws.com/{storage_context.bucket}/{storage_context.key}"

    def delete(self, *, storage_context: StorageContext) -> None:
        bucket = self.resource.Bucket(name=storage_context.bucket)
        bucket.delete_objects(Delete={"Objects": [{"Key": storage_context.key}]})
