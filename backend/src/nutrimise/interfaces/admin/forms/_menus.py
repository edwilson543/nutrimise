from django import forms as django_forms

from nutrimise.domain import menus


class OptimiseMenu(django_forms.Form):
    optimisation_mode = django_forms.ChoiceField(choices=menus.OptimisationMode.choices)
    prompt = django_forms.CharField(
        max_length=128,
        required=False,
        widget=django_forms.Textarea(attrs={"style": "width: 50%;", "rows": 3}),
    )
