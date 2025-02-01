import pytest
from django import db as django_db

from tests.factories import data as data_factories


class TestMenuConstraints:
    def test_user_cannot_have_two_menus_with_the_same_name(self):
        menu = data_factories.Menu()

        with pytest.raises(django_db.IntegrityError):
            data_factories.Menu(author=menu.author, name=menu.name)


class TestMenuToDomainModel:
    def test_converts_menu_orm_model_with_requirements_to_menu_domain(self):
        orm_menu = data_factories.Menu()
        orm_item = data_factories.MenuItem(menu=orm_menu)
        orm_requirements = data_factories.MenuRequirements(menu=orm_menu)
        orm_dietary_requirement = data_factories.DietaryRequirement()
        orm_requirements.dietary_requirements.add(orm_dietary_requirement)
        orm_nutrient_requirement = data_factories.NutrientRequirement(
            menu_requirements=orm_requirements,
            minimum_quantity=0,
            maximum_quantity=10,
            target_quantity=None,
        )
        orm_variety_requirement = data_factories.VarietyRequirement(
            menu_requirements=orm_requirements, minimum=0, maximum=10, target=None
        )

        menu = orm_menu.to_domain_model()

        assert menu.id == orm_menu.id

        assert len(menu.items) == 1
        item = menu.items[0]
        assert item.id == orm_item.id
        assert item.recipe_id == orm_item.recipe_id
        assert item.day == orm_item.day
        assert item.meal_time == orm_item.meal_time

        assert (
            menu.requirements.optimisation_mode.value
            == menu.requirements.optimisation_mode
        )
        assert (
            menu.requirements.maximum_occurrences_per_recipe
            == orm_requirements.maximum_occurrences_per_recipe
        )

        dietary_requirement_ids = menu.requirements.dietary_requirement_ids
        assert dietary_requirement_ids == (orm_dietary_requirement.id,)

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

        assert len(menu.requirements.variety_requirements) == 1
        variety_requirement = menu.requirements.variety_requirements[0]
        assert (
            variety_requirement.ingredient_category_id
            == orm_variety_requirement.ingredient_category_id
        )
        assert variety_requirement.minimum == orm_variety_requirement.minimum
        assert variety_requirement.maximum == orm_variety_requirement.maximum
        assert variety_requirement.target == orm_variety_requirement.target

    def test_converts_menu_orm_model_without_requirements_to_menu_domain(self):
        orm_menu = data_factories.Menu()

        menu = orm_menu.to_domain_model()

        assert menu.id == orm_menu.id
        assert len(menu.items) == 0
        assert menu.requirements is None
