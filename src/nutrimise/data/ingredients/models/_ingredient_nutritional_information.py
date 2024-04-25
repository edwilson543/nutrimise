from django.db import models as django_models

from nutrimise.data import constants

from . import _ingredient, _nutrient


class IngredientNutritionalInformation(django_models.Model):
    """
    Information on the amount of a nutrient found in an ingredient.
    """

    id = django_models.BigAutoField(primary_key=True)

    ingredient = django_models.ForeignKey(
        _ingredient.Ingredient,
        on_delete=django_models.CASCADE,
        related_name="nutritional_information",
    )

    nutrient = django_models.ForeignKey(
        _nutrient.Nutrient, on_delete=django_models.PROTECT, related_name="+"
    )

    quantity_per_gram = django_models.FloatField()

    units = django_models.TextField(choices=constants.NutrientUnit.choices)

    class Meta:
        constraints = [
            django_models.UniqueConstraint(
                fields=["ingredient", "nutrient"],
                name="ingredient_nutrient_unique_together",
            )
        ]

    def __str__(self) -> str:
        return f"{self.nutrient.name} in {self.ingredient.name}"
