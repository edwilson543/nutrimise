from django import urls
from django.conf import settings
from django.conf.urls import static
from django.contrib import admin

urlpatterns = [
    urls.path("admin/", urls.include("reciply.interfaces.admin.urls")),
    urls.path("admin/", admin.site.urls),
] + static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
