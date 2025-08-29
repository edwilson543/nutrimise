from __future__ import annotations

from collections.abc import Iterable

import pydantic

from nutrimise.data.recipes import models as recipe_models


class RecipeList(pydantic.BaseModel):
    recipes: list[_Recipe]

    @classmethod
    def from_orm(cls, recipes: Iterable[recipe_models.Recipe]) -> RecipeList:
        return cls(recipes=[_Recipe.from_orm(recipe) for recipe in recipes])


class _Recipe(pydantic.BaseModel):
    id: int
    name: str
    description: str
    media_url: str

    @classmethod
    def from_orm(cls, recipe: recipe_models.Recipe) -> _Recipe:
        return cls(
            id=recipe.id,
            name=recipe.name,
            description=recipe.description,
            media_url=recipe.image_url,
        )
