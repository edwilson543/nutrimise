from django import urls
from django.conf import settings
from django.conf.urls import static
from django.contrib import admin

urlpatterns = [
    urls.path("admin/", urls.include("nutrimise.interfaces.admin.urls")),
    urls.path("admin/", admin.site.urls),
] + static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # type: ignore[operator, arg-type]
