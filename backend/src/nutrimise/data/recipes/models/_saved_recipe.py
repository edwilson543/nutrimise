from django.contrib.auth import models as auth_models
from django.db import models as django_models

from . import _recipe


class SavedRecipe(django_models.Model):
    """
    A record that a particular user has a saved recipe.
    """

    id = django_models.BigAutoField(primary_key=True)

    user = django_models.ForeignKey(
        auth_models.User, on_delete=django_models.CASCADE, related_name="saved_recipes"
    )

    recipe = django_models.ForeignKey(
        _recipe.Recipe, on_delete=django_models.CASCADE, related_name="saves"
    )

    class Meta:
        constraints = [
            django_models.UniqueConstraint(
                fields=["user", "recipe"], name="user_can_only_save_recipe_once"
            )
        ]
