from nutrimise.domain import ingredients
from testing.factories import domain as domain_factories


class TestNutritionalInformationSumByNutrient:
    def test_aggregates_list_containing_nutritional_information_for_same_ingredient(
        self,
    ):
        nutrient = domain_factories.Nutrient()
        other_nutrient = domain_factories.Nutrient()

        unaggregated_list = [
            domain_factories.NutritionalInformation(
                nutrient=nutrient, nutrient_quantity=1.0
            ),
            domain_factories.NutritionalInformation(
                nutrient=other_nutrient, nutrient_quantity=2.0
            ),
            domain_factories.NutritionalInformation(
                nutrient=nutrient, nutrient_quantity=3.0
            ),
        ]

        aggregated_list = ingredients.NutritionalInformation.sum_by_nutrient(
            nutritional_information=unaggregated_list,
            nutrients=[nutrient, other_nutrient],
        )

        assert aggregated_list == [
            domain_factories.NutritionalInformation(
                nutrient=nutrient, nutrient_quantity=4.0
            ),
            domain_factories.NutritionalInformation(
                nutrient=other_nutrient, nutrient_quantity=2.0
            ),
        ]

    def test_includes_zero_nutritional_information_for_unused_nutrient(
        self,
    ):
        nutrient = domain_factories.Nutrient()

        aggregated_list = ingredients.NutritionalInformation.sum_by_nutrient(
            nutritional_information=[], nutrients=[nutrient]
        )

        nutritional_information = domain_factories.NutritionalInformation(
            nutrient=nutrient, nutrient_quantity=0.0
        )
        assert aggregated_list == [nutritional_information]
