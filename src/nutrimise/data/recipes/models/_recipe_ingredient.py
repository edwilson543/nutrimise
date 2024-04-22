from django.db import models as django_models

from nutrimise.data.ingredients import models as ingredient_models

from . import _recipe


class RecipeIngredient(django_models.Model):
    """
    Record that a known quantity of some ingredient should be included in a recipe.
    """

    id = django_models.BigAutoField(primary_key=True)

    recipe = django_models.ForeignKey(
        _recipe.Recipe, on_delete=django_models.CASCADE, related_name="ingredients"
    )

    ingredient = django_models.ForeignKey(
        ingredient_models.Ingredient,
        on_delete=django_models.PROTECT,
        related_name="recipe_ingredients",
    )

    # Total to meet `number_of_portions` on the recipe.
    quantity = django_models.FloatField()

    class Meta:
        constraints = [
            django_models.UniqueConstraint(
                "recipe", "ingredient", name="ingredient_features_max_once_per_recipe"
            )
        ]

    def __str__(self) -> str:
        return f"{self.ingredient.name} for {self.recipe.name}"

    # ----------
    # Queries
    # ----------

    def grams(self) -> float:
        return self.quantity * self.ingredient.grams_per_unit
