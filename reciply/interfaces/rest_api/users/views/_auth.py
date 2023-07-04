# Third party imports
from knox import views as knox_views
from rest_framework import authentication


class Login(knox_views.LoginView):
    """
    Use basic authentication when users login since they won't have a token yet.
    """

    authentication_classes = [authentication.BasicAuthentication]
