from typing import Any

from django.core.management import base as django_management

from nutrimise.app import ingredients as ingredients_app
from nutrimise.domain import image_extraction


class Command(django_management.BaseCommand):
    """
    Bulk extract the missing nutritional information for the ingredient bank.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._extraction_service = image_extraction.get_image_extraction_service()

    def handle(self, *args: object, **options: object) -> None:
        ingredients_app.gather_ingredient_nutritional_information(
            extraction_service=self._extraction_service
        )
