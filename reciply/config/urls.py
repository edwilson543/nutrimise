# Django imports
from django import urls
from django.conf import settings
from django.conf.urls import static
from django.contrib import admin

urlpatterns = [
    urls.path("admin/", admin.site.urls),
    urls.path("api/", urls.include("interfaces.rest_api.urls")),
] + static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
