import django_webtest
import pytest
from django.contrib.auth import models as auth_models


@pytest.mark.django_db
def admin_client(django_app) -> django_webtest.DjangoTestApp:
    admin = auth_models.User.objects.create_superuser(
        "admin", "admin@example.com", "password"
    )
    django_app.set_user(admin)
    return django_app
