from django import forms as django_forms


class ImageUpload(django_forms.Form):
    image = django_forms.ImageField()
