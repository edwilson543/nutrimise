from django.core import validators as django_validators
from django.db import models as django_models

from nutrimise.domain import constants, ingredients, menus

from . import _menu


class MenuRequirements(django_models.Model):
    """
    The requirements to meet when optimising a menu.
    """

    id = django_models.BigAutoField(primary_key=True)

    menu = django_models.OneToOneField(
        _menu.Menu, on_delete=django_models.CASCADE, related_name="requirements"
    )

    optimisation_mode = django_models.TextField(choices=menus.OptimisationMode.choices)

    maximum_occurrences_per_recipe = django_models.SmallIntegerField(
        validators=[django_validators.MinValueValidator(limit_value=1)]
    )

    dietary_requirements = django_models.ManyToManyField(
        "ingredients.DietaryRequirement", related_name="+", blank=True
    )

    def __str__(self) -> str:
        return f"Requirements for '{self.menu.name}'"

    def to_domain_model(self):
        nutrient_requirements = [
            requirement.to_domain_model()
            for requirement in self.nutrient_requirements.all()
        ]
        variety_requirements = [
            requirement.to_domain_model()
            for requirement in self.variety_requirements.all()
        ]
        dietary_requirement_ids = self.dietary_requirements.values_list("id", flat=True)

        return menus.MenuRequirements(
            optimisation_mode=menus.OptimisationMode(self.optimisation_mode),
            nutrient_requirements=tuple(nutrient_requirements),
            variety_requirements=tuple(variety_requirements),
            maximum_occurrences_per_recipe=self.maximum_occurrences_per_recipe,
            dietary_requirement_ids=tuple(dietary_requirement_ids),
        )


class NutrientRequirement(django_models.Model):
    """
    The nutrient requirements to meet when optimising a menu.
    """

    id = django_models.BigAutoField(primary_key=True)

    menu_requirements = django_models.ForeignKey(
        MenuRequirements,
        on_delete=django_models.CASCADE,
        related_name="nutrient_requirements",
    )

    nutrient = django_models.ForeignKey(
        "ingredients.Nutrient", on_delete=django_models.PROTECT, related_name="+"
    )

    minimum_quantity = django_models.FloatField(null=True, blank=True)

    maximum_quantity = django_models.FloatField(null=True, blank=True)

    target_quantity = django_models.FloatField(null=True, blank=True)

    units = django_models.TextField(choices=ingredients.NutrientUnit.choices)

    enforcement_interval = django_models.TextField(
        choices=constants.NutrientRequirementEnforcementInterval.choices
    )

    class Meta:
        constraints = [
            django_models.UniqueConstraint(
                fields=["menu_requirements_id", "nutrient_id"],
                name="unique_requirements_per_nutrient_per_menu",
            )
        ]

    def __str__(self) -> str:
        return f"{self.nutrient.name} requirements"

    def to_domain_model(self):
        return menus.NutrientRequirement(
            nutrient_id=self.nutrient_id,
            minimum_quantity=self.minimum_quantity,
            maximum_quantity=self.maximum_quantity,
            target_quantity=self.target_quantity,
            units=ingredients.NutrientUnit(self.units),
            enforcement_interval=constants.NutrientRequirementEnforcementInterval(
                self.enforcement_interval
            ),
        )


class VarietyRequirement(django_models.Model):
    """
    Requirements for the number of ingredients that must feature in a menu, per category.
    """

    id = django_models.BigAutoField(primary_key=True)

    menu_requirements = django_models.ForeignKey(
        MenuRequirements,
        on_delete=django_models.CASCADE,
        related_name="variety_requirements",
    )

    ingredient_category = django_models.ForeignKey(
        "ingredients.IngredientCategory",
        on_delete=django_models.PROTECT,
        related_name="+",
    )

    minimum = django_models.PositiveSmallIntegerField(null=True, blank=True)

    maximum = django_models.PositiveSmallIntegerField(null=True, blank=True)

    target = django_models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        constraints = [
            django_models.UniqueConstraint(
                fields=["menu_requirements_id", "ingredient_category_id"],
                name="unique_requirements_per_ingredient_category_per_menu",
            )
        ]

    def __str__(self) -> str:
        return f"{self.ingredient_category.name} requirements"

    def to_domain_model(self):
        return menus.VarietyRequirement(
            ingredient_category_id=self.ingredient_category_id,
            minimum=self.minimum,
            maximum=self.maximum,
            target=self.target,
        )
