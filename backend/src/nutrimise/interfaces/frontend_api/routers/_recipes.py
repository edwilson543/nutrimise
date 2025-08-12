from fastapi import routing

from nutrimise.data.recipes import queries as recipe_queries
from nutrimise.interfaces.frontend_api import schemas


recipe_router = routing.APIRouter()


@recipe_router.get("/")
def list_recipes() -> schemas.RecipeList:
    recipes = recipe_queries.get_recipes()
    return schemas.RecipeList.from_domain(recipes)
