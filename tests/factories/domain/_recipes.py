# Third party imports
import factory

# Local application imports
from reciply.domain import recipes


class Recipe(factory.Factory):
    id = factory.Sequence(lambda n: n)
    meal_times = factory.LazyFunction(tuple)
    nutritional_information = factory.LazyFunction(tuple)

    class Meta:
        model = recipes.Recipe
