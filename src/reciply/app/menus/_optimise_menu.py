from reciply.data.menus import models as menu_models
# from reciply.domain.nutrition_optimisation import optimiser


def optimise_recipes_for_menu(*, menu_id: int) -> menu_models.Menu:
    # menu = menu_models.Menu.objects.prefetch_related("menus").get(id=menu_id)
    # optimiser.optimise_recipes_for_menu()
    pass