from testing.factories import data as data_factories


class TestRecipeAuthorToDomainModel:
    def test_converts_recipe_author_to_domain_model(self):
        author = data_factories.RecipeAuthor()

        result = author.to_domain_model()

        assert result.id == author.id
        assert result.first_name == author.first_name
        assert result.last_name == author.last_name
