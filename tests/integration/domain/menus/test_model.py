from reciply.domain import menus

from tests.factories import data as data_factories


class TestMenuFromOrmModel:
    def test_converts_menu_orm_model_with_requirements_to_menu_domain(self):
        orm_menu = data_factories.Menu()
        orm_item = data_factories.MenuItem(menu=orm_menu)
        orm_requirements = data_factories.MenuRequirements(menu=orm_menu)
        orm_nutrient_requirement = data_factories.NutrientRequirement(
            menu_requirements=orm_requirements,
            minimum_quantity=0,
            maximum_quantity=10,
            target_quantity=None,
        )

        menu = menus.Menu.from_orm_model(menu=orm_menu)

        assert menu.id == orm_menu.id

        assert len(menu.items) == 1
        item = menu.items[0]
        assert item.id == orm_item.id
        assert item.recipe_id == orm_item.recipe_id
        assert item.day == orm_item.day
        assert item.meal_time == orm_item.meal_time

        assert (
            menu.requirements.maximum_occurrences_per_recipe
            == orm_requirements.maximum_occurrences_per_recipe
        )
        assert len(menu.requirements.nutrient_requirements) == 1
        nutrient_requirement = menu.requirements.nutrient_requirements[0]
        assert nutrient_requirement.nutrient_id == orm_nutrient_requirement.nutrient_id
        assert (
            nutrient_requirement.minimum_quantity
            == orm_nutrient_requirement.minimum_quantity
        )
        assert (
            nutrient_requirement.maximum_quantity
            == orm_nutrient_requirement.maximum_quantity
        )
        assert (
            nutrient_requirement.target_quantity
            == orm_nutrient_requirement.target_quantity
        )
        assert (
            nutrient_requirement.enforcement_interval
            == orm_nutrient_requirement.enforcement_interval
        )

    def test_converts_menu_orm_model_without_requirements_to_menu_domain(self):
        orm_menu = data_factories.Menu()

        menu = menus.Menu.from_orm_model(menu=orm_menu)

        assert menu.id == orm_menu.id
        assert len(menu.items) == 0
        assert menu.requirements is None
