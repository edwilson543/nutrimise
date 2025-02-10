from django import forms as django_forms

from nutrimise.data.recipes import models as recipe_models


class ImageUpload(django_forms.Form):
    image = django_forms.ImageField()
    author = django_forms.ModelChoiceField(
        queryset=recipe_models.RecipeAuthor.objects.order_by("first_name"),
        required=False,
    )
