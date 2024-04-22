from __future__ import annotations

from django.db import models as django_models

from nutrimise.data import constants
from nutrimise.data.recipes import models as recipe_models

from . import _menu


class MenuItem(django_models.Model):
    """
    A single item from a menu.
    """

    id = django_models.BigAutoField(primary_key=True)

    menu = django_models.ForeignKey(
        _menu.Menu, on_delete=django_models.CASCADE, related_name="items"
    )

    recipe = django_models.ForeignKey(
        recipe_models.Recipe,
        on_delete=django_models.CASCADE,
        null=True,
        blank=True,
        related_name="recipes",
    )

    day = django_models.PositiveSmallIntegerField(choices=constants.Day.choices)

    meal_time = django_models.CharField(
        max_length=16, choices=constants.MealTime.choices
    )

    optimiser_generated = django_models.BooleanField(default=True)

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
        return f"Day {self.day} {self.meal_time.title()}"

    # ----------
    # Mutators
    # ----------

    def update_recipe(self, recipe_id: int) -> MenuItem:
        self.recipe_id = recipe_id
        self.save(update_fields=["recipe", "updated_at"])
        return self

    def lock_from_optimiser(self) -> None:
        if self.optimiser_generated:
            self.optimiser_generated = False
        self.save(update_fields=["optimiser_generated", "updated_at"])

    def unlock_for_optimiser(self) -> None:
        if not self.optimiser_generated:
            self.optimiser_generated = True
        self.save(update_fields=["optimiser_generated", "updated_at"])
