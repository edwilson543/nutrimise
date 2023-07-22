# Third party imports
from rest_framework import request

# Django imports
from django.contrib.auth import models as auth_models


class AuthenticatedRequest(request.Request):
    user: auth_models.User
