from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth import models as auth_models
from django.db import models as django_models


if TYPE_CHECKING:
    pass


class Menu(django_models.Model):
    """
    A collection of recipes.
    """

    id = django_models.BigAutoField(primary_key=True)

    author = django_models.ForeignKey(
        auth_models.User, on_delete=django_models.CASCADE, related_name="menus"
    )

    name = django_models.CharField(max_length=128)

    description = django_models.TextField(blank=True)

    created_at = django_models.DateTimeField(auto_now_add=True)

    updated_at = django_models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            django_models.UniqueConstraint(
                "author", "name", name="users_can_only_have_one_menu_per_name"
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
    ) -> Menu:
        return cls.objects.create(
            author=author,
            name=name,
            description=description,
        )
