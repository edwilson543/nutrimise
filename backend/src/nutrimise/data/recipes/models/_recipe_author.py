from django.db import models as django_models

from nutrimise.domain import recipes


class RecipeAuthor(django_models.Model):
    """
    The author of a recipe.
    """

    id = django_models.BigAutoField(primary_key=True)

    first_name = django_models.TextField()

    last_name = django_models.TextField()

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def to_domain_model(self):
        return recipes.RecipeAuthor(
            id=self.id, first_name=self.first_name, last_name=self.last_name
        )
