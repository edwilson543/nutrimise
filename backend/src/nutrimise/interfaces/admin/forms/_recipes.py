from django import forms as django_forms

from nutrimise.data.recipes import models as recipe_models


class ExtractRecipeFromImage(django_forms.Form):
    image = django_forms.ImageField()
    author = django_forms.ModelChoiceField(
        queryset=recipe_models.RecipeAuthor.objects.order_by("first_name"),
        required=False,
    )


class ExtractRecipeFromURL(django_forms.Form):
    url = django_forms.URLField(
        widget=django_forms.TextInput(attrs={"style": "width: 50%;"})
    )
