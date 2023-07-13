from __future__ import annotations

# Django imports
from django.db import models as django_models

# Local application imports
from data import constants


class RecipeImage(django_models.Model):
    """
    An image of a recipe.
    """

    id = django_models.AutoField(primary_key=True)

    recipe = django_models.ForeignKey("Recipe", on_delete=django_models.CASCADE)

    image = django_models.ImageField(upload_to=constants.MediaNamespace.RECIPES)

    is_hero = django_models.BooleanField()

    created_at = django_models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            django_models.UniqueConstraint(
                "recipe", "is_hero", name="recipe_can_only_have_one_hero_image"
            )
        ]
