from nutrimise.domain import ingredients

from . import models as ingredient_models


def get_or_create_ingredient_category(*, name: str) -> ingredients.IngredientCategory:
    category, _ = ingredient_models.IngredientCategory.objects.get_or_create(
        name__iexact=name, defaults={"name": name}
    )
    return category.to_domain_model()


def get_or_create_ingredient(
    *,
    name: str,
    category_id: int,
    units: str | None,
    grams_per_unit: float,
) -> ingredients.Ingredient:
    pass
