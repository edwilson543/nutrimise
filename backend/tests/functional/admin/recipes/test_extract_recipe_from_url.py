from unittest import mock

from django import urls as django_urls
from django.test import override_settings

from nutrimise.data.recipes import models as recipe_models
from nutrimise.domain.data_extraction import _vendors as data_extraction_vendors


@override_settings(DATA_EXTRACTION_VENDOR="FAKE", EMBEDDING_VENDOR="FAKE")
def test_extracts_image_and_creates_recipe(admin_client):
    add_recipe_url = django_urls.reverse("admin:recipes_recipe_add")
    response = admin_client.get(add_recipe_url)

    assert response.status_code == 200

    form = response.forms["extract-recipe-from-url-form"]
    form["url"] = "https://recipes.com/some-recipe/"
    submit_response = form.submit()

    recipe = recipe_models.Recipe.objects.get()
    fake_service = data_extraction_vendors.FakeDataExtractionService()
    assert recipe.name == fake_service.canned_recipe.name
    assert recipe.description == fake_service.canned_recipe.description
    assert recipe.author_id is None

    assert submit_response.status_code == 302
    assert submit_response.location == django_urls.reverse(
        "admin:recipes_recipe_change", kwargs={"object_id": recipe.id}
    )


@override_settings(DATA_EXTRACTION_VENDOR="BROKEN", EMBEDDING_VENDOR="FAKE")
@mock.patch("django.contrib.messages.error")
def test_handles_error_when_data_extraction_service_is_broken(
    mock_error_messages: mock.Mock, admin_client
):
    add_recipe_url = django_urls.reverse("admin:recipes_recipe_add")
    response = admin_client.get(add_recipe_url)

    assert response.status_code == 200

    form = response.forms["extract-recipe-from-url-form"]
    form["url"] = "https://recipes.com/some-recipe/"
    submit_response = form.submit()

    assert not recipe_models.Recipe.objects.exists()

    assert submit_response.status_code == 302
    assert submit_response.location == add_recipe_url

    mock_error_messages.assert_called_once()
    expected_message = "Unexpected error extracting recipe from url."
    assert mock_error_messages.call_args_list[0].kwargs["message"] == expected_message


@override_settings(DATA_EXTRACTION_VENDOR="FAKE_NO_SERVICE", EMBEDDING_VENDOR="FAKE")
@mock.patch("django.contrib.messages.error")
def test_handles_error_when_no_data_extraction_service_is_installed_for_vendor(
    mock_error_messages: mock.Mock, admin_client
):
    add_recipe_url = django_urls.reverse("admin:recipes_recipe_add")
    response = admin_client.get(add_recipe_url)

    assert response.status_code == 200

    form = response.forms["extract-recipe-from-url-form"]
    form["url"] = "https://recipes.com/some-recipe/"
    submit_response = form.submit()

    assert not recipe_models.Recipe.objects.exists()

    assert submit_response.status_code == 302
    assert submit_response.location == add_recipe_url

    mock_error_messages.assert_called_once()
    expected_message = "Image extraction service is not configured."
    assert mock_error_messages.call_args_list[0].kwargs["message"] == expected_message
