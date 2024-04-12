import factory
from reciply.domain import ingredients


class Nutrient(factory.Factory):
    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: f"nutrient-{n}")

    class Meta:
        model = ingredients.Nutrient


class NutritionalInformation(factory.Factory):
    nutrient = factory.SubFactory(Nutrient)
    nutrient_quantity_grams = 1

    class Meta:
        model = ingredients.NutritionalInformation
