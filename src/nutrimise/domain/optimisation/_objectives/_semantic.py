import attrs
import pulp as lp
from numpy import linalg as np_linalg

from nutrimise.domain import embeddings, recipes
from nutrimise.domain.optimisation import _inputs, _variables


@attrs.frozen
class SemanticOptimisationError(Exception):
    pass


@attrs.frozen
class EmbeddingModelNotSet(SemanticOptimisationError):
    def __str__(self) -> str:
        return "Semantic optimisation is not available because no embedding model is configured."


@attrs.frozen
class MenuEmbeddingMissing(SemanticOptimisationError):
    menu_id: int
    model: embeddings.EmbeddingModel

    def __str__(self) -> str:
        return f"Menu {self.menu_id} has no embedding for model {self.model.value}"


@attrs.frozen
class RecipeEmbeddingMissing(SemanticOptimisationError):
    recipe_id: int
    model: embeddings.EmbeddingModel

    def __str__(self) -> str:
        return f"Recipe {self.recipe_id} has no embedding for model {self.model.value}"


def add_semantic_objective_to_problem(
    *,
    problem: lp.LpProblem,
    inputs: _inputs.OptimiserInputs,
    variables: _variables.Variables,
) -> lp.LpProblem:
    """
    Maximise the degree of semantic match between the menu and the selected recipes.

    This is achieved by minimising the L2 distance between the menu's embedding vector
    and that of the selected recipes.
    """
    l2_distances = _get_l2_distances_from_recipes_to_menu(inputs)

    objective_function = lp.lpSum(
        l2_distances[variable.recipe.id] * variable.lp_variable
        for variable in variables.decision_variables
    )

    problem += objective_function
    problem.sense = lp.LpMinimize
    return problem


def _get_l2_distances_from_recipes_to_menu(
    inputs: _inputs.OptimiserInputs,
) -> dict[int, float]:
    embedding = _get_menu_embedding(inputs)

    return {
        recipe.id: _get_l2_distance_from_recipe_to_menu_embedding(recipe, embedding)
        for recipe in inputs.recipes_to_consider
    }


def _get_menu_embedding(inputs: _inputs.OptimiserInputs) -> embeddings.Embedding:
    if not (model := inputs.embedding_model):
        raise EmbeddingModelNotSet

    for embedding in inputs.menu.embeddings:
        if embedding.model == model:
            return embedding
    raise MenuEmbeddingMissing(menu_id=inputs.menu.id, model=model)


def _get_l2_distance_from_recipe_to_menu_embedding(
    recipe: recipes.Recipe, menu_embedding: embeddings.Embedding
) -> float:
    recipe_embedding = _get_recipe_embedding(recipe, menu_embedding.model)
    return float(np_linalg.norm(recipe_embedding.vector - menu_embedding.vector))


def _get_recipe_embedding(
    recipe: recipes.Recipe, model: embeddings.EmbeddingModel
) -> embeddings.Embedding:
    for embedding in recipe.embeddings:
        if embedding.model == model:
            return embedding
    raise RecipeEmbeddingMissing(recipe_id=recipe.id, model=model)
