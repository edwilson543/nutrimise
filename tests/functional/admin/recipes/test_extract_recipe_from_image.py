import pathlib

from django import urls as django_urls
from django.test import override_settings

from nutrimise.data.recipes import models as recipe_models
from nutrimise.domain import image_extraction


TEST_IMAGE_PATH = pathlib.Path(__file__).parent / "test-image.jpeg"


@override_settings(IMAGE_EXTRACTION_VENDOR="FAKE")
def test_extracts_image_and_creates_recipe(admin_client):
    url = django_urls.reverse("recipe-extract")
    response = admin_client.get(url)

    assert response.status_code == 200

    form = response.forms["upload-image"]
    with open(TEST_IMAGE_PATH, "rb") as uploaded_image:
        form["image"] = ("curry.jpeg", uploaded_image.read())
    submit_response = form.submit()

    recipe = recipe_models.Recipe.objects.get()
    fake_service = image_extraction.FakeImageExtractService()
    assert recipe.name == fake_service._canned_recipe.name
    assert recipe.description == fake_service._canned_recipe.description

    assert submit_response.status_code == 302
    assert submit_response.location == django_urls.reverse(
        "admin:recipes_recipe_change", kwargs={"object_id": recipe.id}
    )
