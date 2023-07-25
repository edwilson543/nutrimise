from __future__ import annotations

# Django imports
from django.db import models as django_models

# Local application imports
from data import constants
from data.recipes import models as recipe_models

from . import _menu


class MenuItem(django_models.Model):
    """
    A single item from a menu.
    """

    id = django_models.AutoField(primary_key=True)

    menu = django_models.ForeignKey(
        _menu.Menu, on_delete=django_models.CASCADE, related_name="items"
    )

    recipe = django_models.ForeignKey(
        recipe_models.Recipe, on_delete=django_models.CASCADE, related_name="recipes"
    )

    day = django_models.PositiveSmallIntegerField(choices=constants.Day.choices)

    meal_time = django_models.CharField(
        max_length=16, choices=constants.MealTime.choices
    )

    created_at = django_models.DateTimeField(auto_now_add=True)

    updated_at = django_models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            django_models.UniqueConstraint(
                "menu",
                "meal_time",
                "day",
                name="each_menu_can_only_have_one_meal_per_meal_time_per_day",
            )
        ]

    def __str__(self) -> str:
        return f"{self.meal_time} ({self.day}) for {self.menu}"
