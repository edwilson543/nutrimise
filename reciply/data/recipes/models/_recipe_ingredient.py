# Django imports
from django.db import models as django_models

# Local application imports
from data.ingredients import models as ingredient_models

from . import _recipe


class RecipeIngredient(django_models.Model):
    """
    Record that a known quantity of some ingredient should be included in a recipe.
    """

    recipe = django_models.ForeignKey(
        _recipe.Recipe, on_delete=django_models.CASCADE, related_name="ingredients"
    )

    ingredient = django_models.ForeignKey(
        ingredient_models.Ingredient,
        on_delete=django_models.PROTECT,
        related_name="recipe_ingredients",
    )

    quantity = django_models.FloatField()

    def __str__(self) -> str:
        return f"{self.ingredient.name_singular} for {self.recipe.name}"
