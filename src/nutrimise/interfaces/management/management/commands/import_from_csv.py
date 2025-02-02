import csv
import enum
import pathlib

import attrs
from django import forms as django_forms
from django.conf import settings
from django.core.management import base as django_management
from django.db import transaction

from . import _forms


DATA_IMPORT_PATH = pathlib.Path(settings.BASE_DIR).parents[1] / "data"


class FileName(enum.Enum):
    # Ingredients.
    DIETARY_REQUIREMENT = "dietary-requirement.csv"
    INGREDIENT = "ingredient.csv"
    INGREDIENT_CATEGORY = "ingredient-category.csv"
    NUTRIENT = "nutrient.csv"
    INGREDIENT_NUTRITIONAL_INFORMATION = "ingredient-nutritional-information.csv"


@attrs.frozen
class ValidationError(Exception):
    filename: FileName
    invalid_rows: dict[int, str]  # Mapping of row numbers to errors.

    def __str__(self) -> str:
        return "\n".join(
            f"{self.filename.value}: Error in row {row}: {error}"
            for row, error in self.invalid_rows.items()
        )


@attrs.define
class CSVFile:
    filename: FileName
    model_form: type[django_forms.ModelForm]
    _successful_import_count: int = attrs.field(default=0, init=False)

    def process_to_db(self, *, path: pathlib.Path) -> None:
        filepath = path / self.filename.value
        invalid_rows: dict[int, str] = {}

        with open(filepath, "r", encoding="utf-8-sig") as file, transaction.atomic():
            reader = csv.DictReader(file)
            for row_number, row in enumerate(reader):
                form = self.model_form(data=row)
                if form.is_valid():
                    form.save()
                    self._successful_import_count += 1
                else:
                    invalid_rows[row_number] = str(form.errors.as_text())

        if invalid_rows:
            raise ValidationError(filename=self.filename, invalid_rows=invalid_rows)

    def success_message(self) -> str:
        return f"Imported {self._successful_import_count} row(s) from '{self.filename.value}'"


class Command(django_management.BaseCommand):
    def add_arguments(self, parser: django_management.CommandParser) -> None:
        parser.add_argument("--dataset", default="example")

    def handle(self, *args: object, **options: str) -> None:
        path = DATA_IMPORT_PATH / options["dataset"]
        csv_files = [
            CSVFile(
                filename=FileName.DIETARY_REQUIREMENT,
                model_form=_forms.DietaryRequirement,
            ),
            CSVFile(filename=FileName.NUTRIENT, model_form=_forms.Nutrient),
            CSVFile(
                filename=FileName.INGREDIENT_CATEGORY,
                model_form=_forms.IngredientCategory,
            ),
            CSVFile(filename=FileName.INGREDIENT, model_form=_forms.Ingredient),
            CSVFile(
                filename=FileName.INGREDIENT_NUTRITIONAL_INFORMATION,
                model_form=_forms.IngredientNutritionalInformation,
            ),
        ]

        for csv_file in csv_files:
            try:
                csv_file.process_to_db(path=path)
            except ValidationError as exc:
                self.stderr.write(str(exc))
            else:
                self.stdout.write(csv_file.success_message())
