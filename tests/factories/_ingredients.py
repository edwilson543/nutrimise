# Third party imports
import factory

# Local application imports
from data.ingredients import models as ingredient_models


class Ingredient(factory.django.DjangoModelFactory):
    name_singular = factory.Sequence(lambda n: f"ingredient-{n}")
    name_plural = factory.Sequence(lambda n: f"ingredient-{n}s")
    category = "Meat"
    grams_per_unit = 1
    protein_per_gram = 0.5
    carbohydrates_per_gram = 0.5

    class Meta:
        model = ingredient_models.Ingredient
