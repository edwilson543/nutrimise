from unittest import mock

from django import urls as django_urls
from django.test import override_settings

from nutrimise.data.recipes import models as recipe_models
from nutrimise.domain.image_extraction import _vendors as image_extraction_vendors
from testing.factories import images as image_factories


@override_settings(IMAGE_EXTRACTION_VENDOR="FAKE")
def test_extracts_image_and_creates_recipe(admin_client):
    add_recipe_url = django_urls.reverse("admin:recipes_recipe_add")
    response = admin_client.get(add_recipe_url)

    assert response.status_code == 200

    form = response.forms["upload-image"]
    form["image"] = image_factories.get_uploaded_image()
    submit_response = form.submit()

    recipe = recipe_models.Recipe.objects.get()
    fake_service = image_extraction_vendors.FakeImageExtractionService()
    assert recipe.name == fake_service.canned_recipe.name
    assert recipe.description == fake_service.canned_recipe.description

    assert submit_response.status_code == 302
    assert submit_response.location == django_urls.reverse(
        "admin:recipes_recipe_change", kwargs={"object_id": recipe.id}
    )


@override_settings(IMAGE_EXTRACTION_VENDOR="BROKEN")
@mock.patch("django.contrib.messages.error")
def test_handles_error_when_image_extraction_service_is_broken(
    mock_error_messages: mock.Mock, admin_client
):
    add_recipe_url = django_urls.reverse("admin:recipes_recipe_add")
    response = admin_client.get(add_recipe_url)

    assert response.status_code == 200

    form = response.forms["upload-image"]
    form["image"] = image_factories.get_uploaded_image()
    submit_response = form.submit()

    assert not recipe_models.Recipe.objects.exists()

    assert submit_response.status_code == 302
    assert submit_response.location == add_recipe_url

    mock_error_messages.assert_called_once()
    expected_message = "Unexpected error extracting image from recipe."
    assert mock_error_messages.call_args_list[0].kwargs["message"] == expected_message


@override_settings(IMAGE_EXTRACTION_VENDOR="FAKE_NO_SERVICE")
@mock.patch("django.contrib.messages.error")
def test_handles_error_when_no_image_extraction_service_is_installed_for_vendor(
    mock_error_messages: mock.Mock, admin_client
):
    add_recipe_url = django_urls.reverse("admin:recipes_recipe_add")
    response = admin_client.get(add_recipe_url)

    assert response.status_code == 200

    form = response.forms["upload-image"]
    form["image"] = image_factories.get_uploaded_image()
    submit_response = form.submit()

    assert not recipe_models.Recipe.objects.exists()

    assert submit_response.status_code == 302
    assert submit_response.location == add_recipe_url

    mock_error_messages.assert_called_once()
    expected_message = "Image extraction is not configured."
    assert mock_error_messages.call_args_list[0].kwargs["message"] == expected_message
