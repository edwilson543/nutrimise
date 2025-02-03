from django.contrib import admin

from ._ingredients import (
    IngredientAdmin,
    IngredientNutritionalInformationAdmin,
    NutrientAdmin,
)
from ._menus import MenuAdmin, MenuItemAdmin, MenuEmbeddingAdmin
from ._recipes import RecipeAdmin, RecipeEmbeddingAdmin, RecipeIngredientAdmin


# Overrides
admin.site.site_header = "nutrimise admin"
admin.site.site_title = "nutrimise"
