from django.db import models as django_models


class RecipeAuthor(django_models.Model):
    """
    The author of a recipe.
    """

    id = django_models.BigAutoField(primary_key=True)

    first_name = django_models.TextField()

    last_name = django_models.TextField()

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
