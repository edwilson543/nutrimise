from __future__ import annotations

from collections import defaultdict

import attrs

from nutrimise.domain import ingredients, recipes

from . import _model


@attrs.frozen
class RecipeNotInLookup(Exception):
    recipe_id: int


@attrs.frozen
class ShoppingListItem:
    ingredient: ingredients.Ingredient
    quantity: float

    def __add__(self, other: ShoppingListItem) -> ShoppingListItem:
        if self.ingredient != other.ingredient:
            raise ValueError(
                "Cannot add shopping list items for different ingredients!"
            )
        return ShoppingListItem(
            ingredient=self.ingredient,
            quantity=self.quantity + other.quantity,
        )

    @classmethod
    def from_recipe_ingredient(
        cls, recipe_ingredient: recipes.RecipeIngredient
    ) -> ShoppingListItem:
        return cls(
            ingredient=recipe_ingredient.ingredient,
            quantity=recipe_ingredient.quantity,
        )


@attrs.frozen
class ShoppingList:
    items: tuple[ShoppingListItem, ...]

    def __getitem__(self, item: ingredients.Ingredient) -> ShoppingListItem:
        for shopping_list_item in self.items:
            if shopping_list_item.ingredient.id == item.id:
                return shopping_list_item
        raise KeyError(f"Ingredient {item.id} is not in the shopping list.")

    @property
    def items_by_ingredient_category(
        self,
    ) -> dict[ingredients.IngredientCategory, tuple[ShoppingListItem, ...]]:
        categorised: defaultdict[
            ingredients.IngredientCategory, tuple[ShoppingListItem, ...]
        ] = defaultdict(tuple)

        for item in self.items:
            categorised[item.ingredient.category] += (item,)

        return {
            category: tuple(sorted(items, key=lambda item: item.ingredient.name))
            for category, items in categorised.items()
        }


def get_shopping_list(
    *, menu: _model.Menu, recipe_lookup: dict[int, recipes.Recipe]
) -> ShoppingList:
    shopping_list_items: dict[int, ShoppingListItem] = {}

    for item in menu.items:
        if (recipe_id := item.recipe_id) is None:
            continue

        try:
            recipe = recipe_lookup[recipe_id]
        except KeyError as exc:
            raise RecipeNotInLookup(recipe_id=recipe_id) from exc

        for recipe_ingredient in recipe.ingredients:
            shopping_list_item = ShoppingListItem.from_recipe_ingredient(
                recipe_ingredient
            )
            ingredient_id = recipe_ingredient.ingredient.id

            if ingredient_id not in shopping_list_items:
                shopping_list_items[ingredient_id] = shopping_list_item
            else:
                shopping_list_items[ingredient_id] += shopping_list_item

    items = shopping_list_items.values()
    return ShoppingList(items=tuple(items))
