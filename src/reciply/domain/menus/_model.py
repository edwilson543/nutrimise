from __future__ import annotations

import attrs

from reciply.data import constants
from reciply.data.menus import models as menu_models


@attrs.frozen
class Menu:
    id: int
    name: str
    description: str
    items: tuple[MenuItem, ...]
    requirements: MenuRequirements | None

    @classmethod
    def from_orm_model(cls, *, menu: menu_models.Menu) -> Menu:
        try:
            requirements = MenuRequirements.from_orm_model(
                requirements=menu.requirements
            )
        except menu_models.MenuRequirements.DoesNotExist:
            requirements = None

        return cls(
            id=menu.id,
            name=menu.name,
            description=menu.description,
            items=MenuItem.from_orm_model(items=list(menu.items.all())),
            requirements=requirements,
        )

    @property
    def days(self) -> tuple[constants.Day, ...]:
        return tuple(
            sorted(set(item.day for item in self.items), key=lambda day: day.value)
        )

    @property
    def meal_schedule(self) -> dict[constants.MealTime, dict[constants.Day, MenuItem]]:
        schedule: dict[constants.MealTime, dict[constants.Day, MenuItem]] = {}
        for item in self.items:
            schedule[item.meal_time][item.day] = item
        return schedule


@attrs.define
class MenuItem:
    id: int
    recipe_id: int | None
    day: constants.Day
    meal_time: constants.MealTime
    optimiser_generated: bool

    @classmethod
    def from_orm_model(
        cls, *, items: list[menu_models.MenuItem]
    ) -> tuple[MenuItem, ...]:
        return tuple(
            cls(
                id=item.id,
                recipe_id=item.recipe_id,
                day=constants.Day(item.day),
                meal_time=constants.MealTime(item.meal_time),
                optimiser_generated=item.optimiser_generated,
            )
            for item in items
        )

    # Mutators

    def update_recipe_id(self, *, recipe_id: int) -> None:
        self.recipe_id = recipe_id


@attrs.frozen
class MenuRequirements:
    nutrient_requirements: tuple[NutrientRequirement, ...]
    maximum_occurrences_per_recipe: int

    @classmethod
    def from_orm_model(
        cls, *, requirements: menu_models.MenuRequirements
    ) -> MenuRequirements:
        return cls(
            maximum_occurrences_per_recipe=requirements.maximum_occurrences_per_recipe,
            nutrient_requirements=NutrientRequirement.from_orm_model(
                requirements=list(requirements.nutrient_requirements.all())
            ),
        )


@attrs.frozen
class NutrientRequirement:
    nutrient_id: int
    minimum_quantity: float | None
    maximum_quantity: float | None
    target_quantity: float | None
    enforcement_interval: constants.NutrientRequirementEnforcementInterval

    @classmethod
    def from_orm_model(
        cls, *, requirements: list[menu_models.NutrientRequirement]
    ) -> tuple[NutrientRequirement, ...]:
        return tuple(
            cls(
                nutrient_id=requirement.nutrient_id,
                minimum_quantity=requirement.minimum_quantity,
                maximum_quantity=requirement.maximum_quantity,
                target_quantity=requirement.target_quantity,
                enforcement_interval=constants.NutrientRequirementEnforcementInterval(
                    requirement.enforcement_interval
                ),
            )
            for requirement in requirements
        )
