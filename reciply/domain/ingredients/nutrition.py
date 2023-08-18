from __future__ import annotations

# Standard library imports
import dataclasses
from collections.abc import Iterable

# Local application imports
from data.ingredients import models as ingredient_models
from data.menus import models as menu_models
from data.recipes import models as recipe_models


@dataclasses.dataclass(frozen=True)
class NutritionalInformation:
    """
    Absolute nutritional information for an ingredient, recipe or menu.
    """

    protein_grams: float
    carbohydrates_grams: float

    # ----------
    # Factories
    # ----------

    @classmethod
    def for_ingredient(
        cls, *, ingredient: ingredient_models.Ingredient, quantity: float
    ) -> NutritionalInformation:
        """
        Get the nutritional information for a single ingredient.
        """
        conversion_factor = ingredient.grams_per_unit * quantity

        return cls(
            protein_grams=ingredient.protein_per_gram * conversion_factor,
            carbohydrates_grams=ingredient.carbohydrates_per_gram * conversion_factor,
        )

    @classmethod
    def for_recipe(cls, *, recipe: recipe_models.Recipe) -> NutritionalInformation:
        """
        Aggregate the nutritional information for all ingredients in a recipe.
        """
        return _sum(
            cls.for_ingredient(
                ingredient=recipe_ingredient.ingredient,
                quantity=recipe_ingredient.quantity,
            )
            for recipe_ingredient in recipe.ingredients.all()
        )

    @classmethod
    def for_menu(cls, *, menu: menu_models.Menu) -> NutritionalInformation:
        """
        Aggregate the nutritional information for all ingredients in all recipes of a menu.
        """
        return _sum(
            cls.for_recipe(recipe=menu_item.recipe)
            for menu_item in menu.items.prefetch_related(
                "recipe__ingredients__ingredient"
            )
        )

    @classmethod
    def zero(cls) -> NutritionalInformation:
        return cls(protein_grams=0, carbohydrates_grams=0)

    # ----------
    # Dunder methods
    # ----------

    def __add__(self, other: NutritionalInformation) -> NutritionalInformation:
        return NutritionalInformation(
            protein_grams=self.protein_grams + other.protein_grams,
            carbohydrates_grams=self.carbohydrates_grams + other.carbohydrates_grams,
        )


def _sum(items: Iterable[NutritionalInformation]) -> NutritionalInformation:
    """
    Sum nutritional information for 0 or more items.

    Using this rather than __radd__ is due to typing.
    """
    total = NutritionalInformation.zero()
    for item in items:
        total += item
    return total
