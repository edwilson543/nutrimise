import pathlib
from typing import Any

from django.conf import settings
from django.core.management import base as django_management
from PIL import Image

from nutrimise.app import recipes as recipes_app
from nutrimise.data.recipes import operations as recipe_operations
from nutrimise.domain import embeddings, image_extraction, recipes


IMAGES_DIRECTORY = pathlib.Path(settings.BASE_DIR).parents[1] / "data" / "images"


class Command(django_management.BaseCommand):
    """
    Bulk extract recipes from some images on the local file system.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self._image_extraction_service = image_extraction.get_image_extraction_service()
        self._embedding_service = embeddings.get_embedding_service()

    def add_arguments(self, parser: django_management.CommandParser) -> None:
        parser.add_argument("--dataset", default="target", choices=["target", "test"])

    def handle(self, dataset: str, *args: object, **options: object) -> None:
        images_directory = IMAGES_DIRECTORY / dataset

        for path in images_directory.iterdir():
            if path.is_file():
                author = None
                self._extract_recipe_from_image_on_file_system(
                    filepath=path, author=author
                )

            elif path.is_dir():
                author = _get_author_from_directory(path)
                for image in path.iterdir():
                    self._extract_recipe_from_image_on_file_system(
                        filepath=image, author=author
                    )

    def _extract_recipe_from_image_on_file_system(
        self, *, filepath: pathlib.Path, author: recipes.RecipeAuthor | None
    ) -> None:
        with Image.open(filepath) as image:
            recipes_app.extract_recipe_from_image(
                author=author,
                uploaded_image=image,
                image_extraction_service=self._image_extraction_service,
                embedding_service=self._embedding_service,
            )
        self.stdout.write(f"Extracted recipe from: {filepath.name}")


def _get_author_from_directory(directory: pathlib.Path) -> recipes.RecipeAuthor:
    names = directory.name.split("-")
    first_name = names[0].title()
    last_name = names[1].title()

    author_id = recipe_operations.get_or_create_recipe_author(
        first_name=first_name, last_name=last_name
    )
    return recipes.RecipeAuthor(
        id=author_id, first_name=first_name, last_name=last_name
    )
