from nutrimise.data.ingredients import operations as ingredient_operations
from nutrimise.data.ingredients import queries as ingredient_queries
from nutrimise.domain import image_extraction


def gather_ingredient_nutritional_information(
    *,
    extraction_service: image_extraction.ImageExtractionService,
) -> None:
    """
    Ask an AI for the quantity of every nutrient in every ingredient, and save it in the DB.
    """
    all_ingredients = [
        image_extraction.Ingredient.from_domain_model(ingredient)
        for ingredient in ingredient_queries.get_ingredients()
    ]
    nutrients = [
        image_extraction.Nutrient.from_domain_model(nutrient)
        for nutrient in ingredient_queries.get_nutrients()
    ]

    for ingredient in all_ingredients:
        _gather_nutritional_information_for_ingredient(
            ingredient=ingredient,
            nutrients=nutrients,
            extraction_service=extraction_service,
        )


def _gather_nutritional_information_for_ingredient(
    *,
    ingredient: image_extraction.Ingredient,
    nutrients: list[image_extraction.Nutrient],
    extraction_service: image_extraction.ImageExtractionService,
) -> None:
    assert ingredient.id  # For mypy.

    existing_nutritional_information = (
        ingredient_queries.get_ingredient_nutritional_information(
            ingredient_id=ingredient.id
        )
    )
    nutrient_ids_with_info = [
        existing_info.nutrient.id for existing_info in existing_nutritional_information
    ]
    nutrients_without_info = [
        nutrient for nutrient in nutrients if nutrient.id not in nutrient_ids_with_info
    ]

    if not nutrients_without_info:
        return

    ingredient_nutritional_information = (
        extraction_service.extract_ingredient_nutritional_information(
            ingredients=[ingredient], nutrients=nutrients
        )
    )

    for info in ingredient_nutritional_information:
        ingredient_operations.create_ingredient_nutritional_information(
            ingredient_id=info.ingredient_id,
            nutrient_id=info.nutrient_id,
            nutrient_quantity_per_gram_of_ingredient=info.nutrient_quantity_per_gram_of_ingredient,
        )
