# Third party imports
import pytest

# Local application imports
from reciply.interfaces.rest_api.users import serializers
from tests import factories


class TestRegisterUser:
    @pytest.fixture
    def valid_data(self) -> dict[str, str]:
        yield {
            "username": "some-new-username",
            "password1": "password",
            "password2": "password",
            "email": "test@example.com",
        }

    def test_valid_data_accepted(self, valid_data: dict[str, str]):
        data = valid_data

        serializer = serializers.RegisterUser(data=data)

        assert serializer.is_valid(), serializer.errors
        assert serializer.validated_data == data

    def test_username_not_valid_if_already_in_use(self, valid_data: dict[str, str]):
        user = factories.User()
        invalid_data = valid_data | {"username": user.username}

        serializer = serializers.RegisterUser(data=invalid_data)

        assert not serializer.is_valid()
        assert serializer.errors == {"username": ["Username already taken"]}

    def test_non_matching_password_not_valid(self, valid_data: dict[str, str]):
        invalid_data = valid_data | {
            "password1": "something",
            "password2": "something-else",
        }

        serializer = serializers.RegisterUser(data=invalid_data)

        assert not serializer.is_valid()
        assert serializer.errors == {"password": ["Passwords do not match"]}
