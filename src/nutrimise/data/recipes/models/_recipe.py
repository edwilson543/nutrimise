from __future__ import annotations

from django.contrib.postgres import fields as pg_fields
from django.db import models as django_models

from nutrimise.data.ingredients import queries as ingredient_queries
from nutrimise.domain import recipes

from . import _recipe_author


class Recipe(django_models.Model):
    """
    Basic data that defines a recipe.
    """

    id = django_models.BigAutoField(primary_key=True)

    author = django_models.ForeignKey(
        _recipe_author.RecipeAuthor,
        on_delete=django_models.CASCADE,
        related_name="recipes",
        null=True,
    )

    name = django_models.CharField(max_length=128)

    description = django_models.TextField(blank=True)

    methodology = django_models.TextField(blank=True)

    meal_times = pg_fields.ArrayField(
        base_field=django_models.TextField(choices=recipes.MealTime.choices)
    )

    number_of_servings = django_models.PositiveSmallIntegerField()

    created_at = django_models.DateTimeField(auto_now_add=True)

    updated_at = django_models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            django_models.UniqueConstraint(
                "author", "name", name="author_can_only_have_one_recipe_per_name"
            )
        ]

    def __str__(self) -> str:
        return self.name

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
        meal_times = [recipes.MealTime(meal_time) for meal_time in self.meal_times]
        embeddings = [
            embedding.to_domain_model() for embedding in self.embeddings.all()
        ]

        return recipes.Recipe(
            id=self.id,
            name=self.name,
            description=self.description,
            methodology=self.methodology,
            meal_times=tuple(meal_times),
            nutritional_information_per_serving=tuple(nutritional_information),
            ingredients=tuple(ingredients),
            embeddings=tuple(embeddings),
        )
