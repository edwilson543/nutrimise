from __future__ import annotations

# Standard library imports
from typing import TYPE_CHECKING

# Django imports
from django.contrib.auth import models as auth_models
from django.db import models as django_models

# Local application imports
from reciply.data import constants

if TYPE_CHECKING:
    # Local application imports
    from reciply.data.recipes import models as recipe_models

    from . import _menu_item


class Menu(django_models.Model):
    """
    A collection of recipes.
    """

    id = django_models.AutoField(primary_key=True)

    author = django_models.ForeignKey(
        auth_models.User, on_delete=django_models.CASCADE, related_name="menus"
    )

    name = django_models.CharField(max_length=128)

    description = django_models.TextField()

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

    def add_item(
        self,
        *,
        recipe: recipe_models.Recipe,
        day: constants.Day,
        meal_time: constants.MealTime,
    ) -> _menu_item.MenuItem:
        """
        Persist a list of menu items in the db.
        """
        return self.items.create(recipe=recipe, day=day, meal_time=meal_time)

    def add_items(
        self,
        *,
        items: list[_menu_item.MenuItem],
    ) -> list[_menu_item.MenuItem]:
        """
        Persist a list of menu items in the db.
        """
        return self.items.bulk_create(items)
