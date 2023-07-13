from __future__ import annotations

# Django imports
from django.contrib.auth import models as auth_models
from django.db import models as django_models


class Recipe(django_models.Model):
    """
    Basic data that defines a recipe.
    """

    id = django_models.AutoField(primary_key=True)

    author = django_models.ForeignKey(auth_models.User, on_delete=django_models.CASCADE)

    name = django_models.CharField(max_length=128)

    description = django_models.TextField()

    class Meta:
        constraints = [
            django_models.UniqueConstraint(
                "author", "name", name="users_can_only_have_one_recipe_per_name"
            )
        ]

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
