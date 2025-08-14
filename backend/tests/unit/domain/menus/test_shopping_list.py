import pytest

from nutrimise.domain import menus
from testing.factories import domain as domain_factories


class TestShoppingListByIngredientCategory:
    def test_groups_ingredients_into_categories(self):
        meat = domain_factories.IngredientCategory(name="meat")
        chicken = domain_factories.Ingredient(category=meat)
        pork = domain_factories.Ingredient(category=meat)

        vegetable = domain_factories.IngredientCategory(name="vegetable")
        brocoli = domain_factories.Ingredient(category=vegetable)
        carrot = domain_factories.Ingredient(category=vegetable)

        items = (
            menus.ShoppingListItem(ingredient=pork, quantity=1.0),
            menus.ShoppingListItem(ingredient=carrot, quantity=1.0),
            menus.ShoppingListItem(ingredient=chicken, quantity=1.0),
            menus.ShoppingListItem(ingredient=brocoli, quantity=1.0),
        )

        shopping_list = menus.ShoppingList(items=items)
        items_by_category = shopping_list.items_by_ingredient_category

        assert len(items_by_category) == 2
        assert items_by_category[meat] == (items[2], items[0])
        assert items_by_category[vegetable] == (items[3], items[1])


class TestGetShoppingList:
    def test_combines_all_ingredients_for_all_menu_items_to_make_shopping_list(self):
        ingredient = domain_factories.Ingredient()
        other_ingredient = domain_factories.Ingredient()

        recipe_ingredient = domain_factories.RecipeIngredient(
            ingredient=ingredient, quantity=2.0
        )
        recipe_other_ingredient = domain_factories.RecipeIngredient(
            ingredient=other_ingredient, quantity=3.0
        )
        recipe_ingredients = (recipe_ingredient, recipe_other_ingredient)
        recipe = domain_factories.Recipe(ingredients=recipe_ingredients)

        other_recipe_ingredient = domain_factories.RecipeIngredient(
            ingredient=ingredient, quantity=7.0
        )
        other_recipe_other_ingredient = domain_factories.RecipeIngredient(
            ingredient=other_ingredient, quantity=15.0
        )
        other_recipe_ingredients = (
            other_recipe_ingredient,
            other_recipe_other_ingredient,
        )
        other_recipe = domain_factories.Recipe(ingredients=other_recipe_ingredients)

        recipe_lookup = {recipe.id: recipe, other_recipe.id: other_recipe}

        menu_item = domain_factories.MenuItem(recipe_id=recipe.id)
        other_menu_item = domain_factories.MenuItem(recipe_id=other_recipe.id)
        menu = domain_factories.Menu(items=(menu_item, other_menu_item))

        shopping_list = menus.get_shopping_list(menu=menu, recipe_lookup=recipe_lookup)

        assert len(shopping_list.items) == 2
        assert shopping_list[ingredient].quantity == 9.0
        assert shopping_list[other_ingredient].quantity == 18.0

    def test_creates_empty_shopping_list_for_menu_with_no_recipes(self):
        menu = domain_factories.Menu()

        shopping_list = menus.get_shopping_list(menu=menu, recipe_lookup={})

        assert shopping_list.items == ()

    def test_raises_when_recipe_not_in_lookup(self):
        recipe = domain_factories.Recipe()

        menu_item = domain_factories.MenuItem(recipe_id=recipe.id)
        menu = domain_factories.Menu(items=(menu_item,))

        with pytest.raises(menus.RecipeNotInLookup) as exc:
            menus.get_shopping_list(menu=menu, recipe_lookup={})

        assert exc.value.recipe_id == recipe.id
