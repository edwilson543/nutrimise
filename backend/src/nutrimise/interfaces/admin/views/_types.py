from django import http as django_http
from django.contrib.auth import models as auth_models


class AuthenticatedHttpRequest(django_http.HttpRequest):
    user: auth_models.User
