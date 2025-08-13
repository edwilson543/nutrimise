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
            media_url=_random_media_url(recipe.id),
        )


def _random_media_url(recipe_id: int) -> str:
    images = [
        "https://ichef.bbc.co.uk/ace/standard/1600/food/recipes/how_to_make_fish_pie_56143_16x9.jpg.webp",
        "https://feelgoodfoodie.net/wp-content/uploads/2025/06/Spaghetti-and-Meatballs-09.jpg",
        "https://munchingwithmariyah.com/wp-content/uploads/2025/03/IMG_4915.jpg",
        "https://www.cubesnjuliennes.com/wp-content/uploads/2020/09/Palak-Chicken-Saag-Recipe.jpg",
        "https://hips.hearstapps.com/del.h-cdn.co/assets/17/35/1600x1600/square-1504128527-delish-mushroom-risotto.jpg?resize=1200:*",
        "https://ichef.bbc.co.uk/ace/standard/1600/food/recipes/one-pan_chicken_68593_16x9.jpg.webp",
    ]
    return images[recipe_id % len(images)]
