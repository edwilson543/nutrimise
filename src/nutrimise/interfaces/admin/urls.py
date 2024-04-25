from django import urls as django_urls

from . import views


urlpatterns = [
    # Recipes.
    django_urls.path(
        route="recipes/<int:recipe_id>/",
        view=views.RecipeDetails.as_view(),
        name="recipe-details",
    ),
    # Menus.
    django_urls.path(
        route="menus/<int:menu_id>/",
        view=views.MenuDetails.as_view(),
        name="menu-details",
    ),
    django_urls.path(
        route="menus/<int:menu_id>/optimise/",
        view=views.OptimiseMenu.as_view(),
        name="menu-optimise",
    ),
    # Menu items.
    django_urls.path(
        route="menu-items/<int:menu_item_id>/lock/",
        view=views.LockMenuItemFromOptimiser.as_view(),
        name="menu-item-lock",
    ),
    django_urls.path(
        route="menu-items/<int:menu_item_id>/unlock/",
        view=views.UnlockMenuItemForOptimiser.as_view(),
        name="menu-item-unlock",
    ),
]
