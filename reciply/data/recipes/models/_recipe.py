from __future__ import annotations

# Standard library imports
from typing import TYPE_CHECKING

# Django imports
from django.contrib.auth import models as auth_models
from django.db import models as django_models

if TYPE_CHECKING:
    from . import _recipe_image


class Recipe(django_models.Model):
    """
    Basic data that defines a recipe.
    """

    id = django_models.AutoField(primary_key=True)

    author = django_models.ForeignKey(auth_models.User, on_delete=django_models.CASCADE)

    name = django_models.CharField(max_length=128)

    description = django_models.TextField(blank=True)

    created_at = django_models.DateTimeField(auto_now_add=True)

    updated_at = django_models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            django_models.UniqueConstraint(
                "author", "name", name="users_can_only_have_one_recipe_per_name"
            )
        ]

    def __str__(self) -> str:
        return self.name

    # ----------
    # Factories
    # ----------

    @classmethod
    def new(
        cls,
        *,
        author: auth_models.User,
        name: str,
        description: str,
    ) -> Recipe:
        return cls.objects.create(
            author=author,
            name=name,
            description=description,
        )

    def new_image(
        self, is_hero: bool, storage_context: dict[str, str]
    ) -> _recipe_image.RecipeImage:
        return self.images.create(is_hero=is_hero, storage_context=storage_context)
