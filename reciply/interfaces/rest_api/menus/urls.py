# Django imports
from django import urls as django_urls

from . import views

urlpatterns = [
    django_urls.path(
        "menu/list/",
        views.MyMenuList.as_view(),
        name="my-menu-list",
    ),
    django_urls.path("menu/create/", views.MenuCreate.as_view(), name="menu-create"),
    django_urls.path("menu/<int:id>/", views.MenuDetail.as_view(), name="menu-detail"),
]
