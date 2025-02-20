from django.db import models as django_models

from nutrimise.domain import ingredients


class Nutrient(django_models.Model):
    """
    Some nutrient, e.g. protein.
    """

    id = django_models.BigAutoField(primary_key=True)

    name = django_models.TextField(unique=True)

    units = django_models.TextField(choices=ingredients.NutrientUnit.choices)

    def __str__(self) -> str:
        return self.name

    def to_domain_model(self) -> ingredients.Nutrient:
        return ingredients.Nutrient(
            id=self.id, name=self.name, units=ingredients.NutrientUnit(self.units)
        )
