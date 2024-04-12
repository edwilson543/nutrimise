from django.db import models as django_models

from . import _ingredient, _nutrient


class IngredientNutritionalInformation(django_models.Model):
    """
    Information on the amount of a nutrient found in an ingredient.
    """

    ingredient = django_models.ForeignKey(
        _ingredient.Ingredient,
        on_delete=django_models.CASCADE,
        related_name="nutritional_information",
    )

    nutrient = django_models.ForeignKey(
        _nutrient.Nutrient, on_delete=django_models.PROTECT, related_name="+"
    )

    quantity_per_gram = django_models.FloatField()

    class Meta:
        constraints = [
            django_models.UniqueConstraint(
                fields=["ingredient", "nutrient"],
                name="ingredient_nutrient_unique_together",
            )
        ]
