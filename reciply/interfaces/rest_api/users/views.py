# Third party imports
from knox import views as knox_views
from rest_framework import authentication
from rest_framework import request as drf_request
from rest_framework import response as drf_response
from rest_framework import status as drf_status
from rest_framework import views

# Local application imports
from app import users
from interfaces.rest_api.users import serializers


class Login(knox_views.LoginView):
    """
    Use basic authentication when users login since they won't have a token yet.
    """

    authentication_classes = [authentication.BasicAuthentication]


class Register(views.APIView):
    """
    Register a new user.
    """

    def post(
        self, request: drf_request, *args: object, **kwargs: object
    ) -> drf_response.Response:
        serializer = serializers.RegisterUser(data=request.data)
        if serializer.is_valid():
            try:
                token_data = users.create_user(
                    username=serializer.validated_data["username"],
                    password=serializer.validated_data["password1"],
                    email=serializer.validated_data["email"],
                )
            except users.UserAlreadyExists:
                return drf_response.Response(
                    {"username": ["Username already taken"]},
                    status=drf_status.HTTP_400_BAD_REQUEST,
                )

            return drf_response.Response(token_data, status=drf_status.HTTP_200_OK)

        return drf_response.Response(status=drf_status.HTTP_400_BAD_REQUEST)
