# Generated by Django 5.0.4 on 2025-02-10 07:14

import django.core.validators
import django.db.models.deletion
import pgvector.django.vector
from django.conf import settings
from django.db import migrations, models

from nutrimise.domain import embeddings


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("ingredients", "0001_initial"),
        ("recipes", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Menu",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=128)),
                ("description", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="menus",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MenuEmbedding",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("vector", pgvector.django.vector.VectorField(dimensions=embeddings.EMBEDDING_DIMENSIONS)),
                ("prompt_hash", models.TextField()),
                (
                    "vendor",
                    models.TextField(
                        choices=[
                            ("OPENAI", "OpenAI"),
                            ("FAKE", "Fake"),
                            ("FAKE_NO_SERVICE", "Fake no service"),
                            ("BROKEN", "Broken"),
                        ]
                    ),
                ),
                (
                    "model",
                    models.TextField(
                        choices=[
                            ("text-embedding-3-small", "text-embedding-3-small"),
                            ("fake", "fake"),
                        ]
                    ),
                ),
                (
                    "menu",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="embeddings",
                        to="menus.menu",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MenuItem",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "day",
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(limit_value=1)
                        ]
                    ),
                ),
                (
                    "meal_time",
                    models.CharField(
                        choices=[
                            ("BREAKFAST", "Breakfast"),
                            ("LUNCH", "Lunch"),
                            ("DINNER", "Dinner"),
                        ],
                        max_length=16,
                    ),
                ),
                ("optimiser_generated", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "menu",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="menus.menu",
                    ),
                ),
                (
                    "recipe",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="recipes",
                        to="recipes.recipe",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MenuRequirements",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "optimisation_mode",
                    models.TextField(
                        choices=[
                            ("RANDOM", "Random"),
                            ("SEMANTIC", "Semantic"),
                            ("NUTRIENT", "Nutrient"),
                            ("VARIETY", "Ingredient variety"),
                            ("EVERYTHING", "Everything"),
                        ]
                    ),
                ),
                (
                    "maximum_occurrences_per_recipe",
                    models.SmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(limit_value=1)
                        ]
                    ),
                ),
                (
                    "dietary_requirements",
                    models.ManyToManyField(
                        blank=True,
                        related_name="+",
                        to="ingredients.dietaryrequirement",
                    ),
                ),
                (
                    "menu",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="requirements",
                        to="menus.menu",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="NutrientRequirement",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("minimum_quantity", models.FloatField(blank=True, null=True)),
                ("maximum_quantity", models.FloatField(blank=True, null=True)),
                ("target_quantity", models.FloatField(blank=True, null=True)),
                (
                    "units",
                    models.TextField(choices=[("GRAMS", "Grams"), ("KCAL", "kcal")]),
                ),
                (
                    "enforcement_interval",
                    models.TextField(choices=[("DAILY", "Daily")]),
                ),
                (
                    "menu_requirements",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="nutrient_requirements",
                        to="menus.menurequirements",
                    ),
                ),
                (
                    "nutrient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="ingredients.nutrient",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="VarietyRequirement",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("minimum", models.PositiveSmallIntegerField(blank=True, null=True)),
                ("maximum", models.PositiveSmallIntegerField(blank=True, null=True)),
                ("target", models.PositiveSmallIntegerField(blank=True, null=True)),
                (
                    "ingredient_category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="ingredients.ingredientcategory",
                    ),
                ),
                (
                    "menu_requirements",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="variety_requirements",
                        to="menus.menurequirements",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="menu",
            constraint=models.UniqueConstraint(
                models.F("author"),
                models.F("name"),
                name="users_can_only_have_one_menu_per_name",
            ),
        ),
        migrations.AddConstraint(
            model_name="menuembedding",
            constraint=models.UniqueConstraint(
                fields=("menu", "model"), name="unique_menu_embedding_per_model"
            ),
        ),
        migrations.AddConstraint(
            model_name="menuitem",
            constraint=models.UniqueConstraint(
                models.F("menu"),
                models.F("meal_time"),
                models.F("day"),
                name="each_menu_can_only_have_one_meal_per_meal_time_per_day",
            ),
        ),
        migrations.AddConstraint(
            model_name="nutrientrequirement",
            constraint=models.UniqueConstraint(
                fields=("menu_requirements_id", "nutrient_id"),
                name="unique_requirements_per_nutrient_per_menu",
            ),
        ),
        migrations.AddConstraint(
            model_name="varietyrequirement",
            constraint=models.UniqueConstraint(
                fields=("menu_requirements_id", "ingredient_category_id"),
                name="unique_requirements_per_ingredient_category_per_menu",
            ),
        ),
    ]
