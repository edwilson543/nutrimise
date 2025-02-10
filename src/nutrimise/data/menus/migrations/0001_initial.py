import django.db.models.deletion
from django.conf import settings
from django.core import validators as django_validators
from django.db import migrations, models

from nutrimise.domain import ingredients, menus


class Migration(migrations.Migration):
    initial = True

    dependencies = [
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
            name="MenuItem",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "day",
                    models.PositiveSmallIntegerField(
                        validators=[django_validators.MinValueValidator(limit_value=1)]
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
                        on_delete=django.db.models.deletion.CASCADE,
                        null=True,
                        blank=True,
                        related_name="recipes",
                        to="recipes.recipe",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MenuRequirements",
            fields=[
                (
                    "id",
                    models.BigAutoField(primary_key=True, serialize=False),
                ),
                (
                    "maximum_occurrences_per_recipe",
                    models.SmallIntegerField(
                        validators=[django_validators.MinValueValidator(limit_value=1)]
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
                (
                    "optimisation_mode",
                    models.TextField(
                        choices=menus.OptimisationMode.choices,
                    ),
                ),
                (
                    "dietary_requirements",
                    models.ManyToManyField(
                        related_name="+",
                        to="ingredients.dietaryrequirement",
                        blank=True,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="NutrientRequirement",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("minimum_quantity", models.FloatField(null=True, blank=True)),
                ("maximum_quantity", models.FloatField(null=True, blank=True)),
                ("target_quantity", models.FloatField(null=True, blank=True)),
                ("units", models.TextField(choices=ingredients.NutrientUnit.choices)),
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
            model_name="varietyrequirement",
            constraint=models.UniqueConstraint(
                fields=("menu_requirements_id", "ingredient_category_id"),
                name="unique_requirements_per_ingredient_category_per_menu",
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
            model_name="menu",
            constraint=models.UniqueConstraint(
                models.F("author"),
                models.F("name"),
                name="users_can_only_have_one_menu_per_name",
            ),
        ),
        migrations.AddConstraint(
            model_name="nutrientrequirement",
            constraint=models.UniqueConstraint(
                fields=("menu_requirements_id", "nutrient_id"),
                name="unique_requirements_per_nutrient_per_menu",
            ),
        ),
    ]
