from __future__ import annotations

from django.contrib.auth import models as auth_models
from django.contrib.postgres import fields as pg_fields
from django.db import models as django_models

from nutrimise.data.ingredients import queries as ingredient_queries
from nutrimise.domain import constants, recipes


class Recipe(django_models.Model):
    """
    Basic data that defines a recipe.
    """

    id = django_models.BigAutoField(primary_key=True)

    author = django_models.ForeignKey(auth_models.User, on_delete=django_models.CASCADE)

    name = django_models.CharField(max_length=128)

    description = django_models.TextField(blank=True)

    meal_times = pg_fields.ArrayField(
        base_field=django_models.TextField(choices=constants.MealTime.choices)
    )

    number_of_servings = django_models.PositiveSmallIntegerField()

    created_at = django_models.DateTimeField(auto_now_add=True)

    updated_at = django_models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            django_models.UniqueConstraint(
                "author", "name", name="users_can_only_have_one_recipe_per_name"
            )
        ]

    def __str__(self) -> str:
        return self.name

    @classmethod
    def new(
        cls,
        *,
        author: auth_models.User,
        name: str,
        description: str,
        meal_times: list[constants.MealTime],
        number_of_servings: int,
    ) -> Recipe:
        return cls.objects.create(
            author=author,
            name=name,
            description=description,
            meal_times=meal_times,
            number_of_servings=number_of_servings,
        )

    def to_domain_model(self):
        nutritional_information = (
            ingredient_queries.get_nutritional_information_for_recipe(
                recipe=self, per_serving=True
            )
        )
        ingredients = [
            recipe_ingredient.to_domain_model()
            for recipe_ingredient in self.ingredients.all()
        ]

        return recipes.Recipe(
            id=self.id,
            meal_times=tuple(
                constants.MealTime(meal_time) for meal_time in self.meal_times
            ),
            nutritional_information_per_serving=tuple(nutritional_information),
            ingredients=tuple(ingredients),
        )
