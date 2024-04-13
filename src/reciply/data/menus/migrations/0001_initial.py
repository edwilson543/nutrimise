import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

from reciply.data import constants


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
                ("id", models.AutoField(primary_key=True, serialize=False)),
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
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "day",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "Monday"),
                            (2, "Tuesday"),
                            (3, "Wednesday"),
                            (4, "Thursday"),
                            (5, "Friday"),
                            (6, "Saturday"),
                            (7, "Sunday"),
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
                ("optimiser_generated", models.BooleanField(default=False)),
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
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("maximum_occurrences_per_recipe", models.SmallIntegerField()),
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
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("minimum_quantity", models.FloatField(null=True)),
                ("maximum_quantity", models.FloatField(null=True)),
                ("target_quantity", models.FloatField(null=True)),
                ("units", models.TextField(choices=constants.NutrientUnit.choices)),
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
    ]
