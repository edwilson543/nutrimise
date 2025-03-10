from django.contrib import admin

from ._ingredients import (
    IngredientAdmin,
    IngredientNutritionalInformationAdmin,
    NutrientAdmin,
)
from ._menus import MenuAdmin, MenuEmbeddingAdmin, MenuItemAdmin
from ._recipes import RecipeAdmin, RecipeEmbeddingAdmin, RecipeIngredientAdmin


# Overrides
admin.site.site_header = "nutrimise"
admin.site.site_title = "nutrimise"
