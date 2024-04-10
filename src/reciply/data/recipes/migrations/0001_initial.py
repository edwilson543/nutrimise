# Django imports
import django.db.models.deletion
from django.conf import settings
from django.contrib.postgres import fields as pg_fields
from django.db import migrations, models

# Local application imports
from reciply.data import constants


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("ingredients", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Recipe",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=128)),
                ("description", models.TextField(blank=True)),
                (
                    "meal_times",
                    pg_fields.ArrayField(
                        base_field=models.TextField(choices=constants.MealTime.choices)
                    ),
                ),
                ("number_of_servings", models.PositiveSmallIntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RecipeIngredient",
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
                ("quantity", models.FloatField()),
                (
                    "ingredient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="recipe_ingredients",
                        to="ingredients.ingredient",
                    ),
                ),
                (
                    "recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ingredients",
                        to="recipes.recipe",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="recipe",
            constraint=models.UniqueConstraint(
                models.F("author"),
                models.F("name"),
                name="users_can_only_have_one_recipe_per_name",
            ),
        ),
        migrations.AddConstraint(
            model_name="recipeingredient",
            constraint=models.UniqueConstraint(
                models.F("recipe"),
                models.F("ingredient"),
                name="ingredient_features_max_once_per_recipe",
            ),
        ),
    ]
