from __future__ import annotations

# Third party imports
import attrs

# Local application imports
from reciply.data import constants
from reciply.data.menus import models as menu_models


@attrs.frozen
class Menu:
    id: int
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
            items=MenuItem.from_orm_model(items=list(menu.items.all())),
            requirements=requirements,
        )


@attrs.frozen
class MenuItem:
    id: int
    recipe_id: int | None
    day: constants.Day
    meal_time: constants.MealTime

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
            )
            for item in items
        )


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
    minimum_grams: float | None
    maximum_grams: float | None
    target_grams: float | None
    enforcement_interval: menu_models.NutrientRequirementEnforcementInterval

    @classmethod
    def from_orm_model(
        cls, *, requirements: list[menu_models.NutrientRequirement]
    ) -> tuple[NutrientRequirement, ...]:
        return tuple(
            cls(
                nutrient_id=requirement.nutrient_id,
                minimum_grams=requirement.minimum_grams,
                maximum_grams=requirement.maximum_grams,
                target_grams=requirement.target_grams,
                enforcement_interval=menu_models.NutrientRequirementEnforcementInterval(
                    requirement.enforcement_interval
                ),
            )
            for requirement in requirements
        )
