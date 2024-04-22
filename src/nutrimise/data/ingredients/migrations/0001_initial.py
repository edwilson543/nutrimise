from django.db import migrations, models

from nutrimise.data import constants


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DietaryRequirement",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("name", models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="IngredientCategory",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("name", models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Ingredient",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=128, unique=True)),
                (
                    "category",
                    models.ForeignKey(
                        "ingredients.IngredientCategory",
                        on_delete=models.PROTECT,
                        related_name="ingredients",
                    ),
                ),
                (
                    "units",
                    models.CharField(max_length=64, null=True, blank=True),
                ),
                ("grams_per_unit", models.FloatField()),
                (
                    "dietary_requirements_satisfied",
                    models.ManyToManyField(
                        related_name="ingredients",
                        to="ingredients.dietaryrequirement",
                        blank=True,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Nutrient",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("name", models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="IngredientNutritionalInformation",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("quantity_per_gram", models.FloatField()),
                ("units", models.TextField(choices=constants.NutrientUnit.choices)),
                (
                    "ingredient",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        related_name="nutritional_information",
                        to="ingredients.ingredient",
                    ),
                ),
                (
                    "nutrient",
                    models.ForeignKey(
                        on_delete=models.deletion.PROTECT,
                        related_name="+",
                        to="ingredients.nutrient",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="ingredientnutritionalinformation",
            constraint=models.UniqueConstraint(
                fields=("ingredient", "nutrient"),
                name="ingredient_nutrient_unique_together",
            ),
        ),
    ]
