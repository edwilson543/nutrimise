from django import forms as django_forms

from nutrimise.data.ingredients import models as ingredient_models

M2M_DELIMITER = "|"


class DietaryRequirement(django_forms.ModelForm):
    class Meta:
        model = ingredient_models.DietaryRequirement
        fields = ["name"]


class Nutrient(django_forms.ModelForm):
    class Meta:
        model = ingredient_models.Nutrient
        fields = ["name"]


class IngredientCategory(django_forms.ModelForm):
    class Meta:
        model = ingredient_models.IngredientCategory
        fields = ["name"]


class Ingredient(django_forms.ModelForm):
    category = django_forms.CharField()
    dietary_requirements = django_forms.CharField()

    class Meta:
        model = ingredient_models.Ingredient
        fields = ["name", "units", "grams_per_unit"]

    def save(self, commit: bool = True) -> ingredient_models.Ingredient:
        self.instance.category = self.cleaned_data["category"]
        super().save(commit=commit)
        if dietary_requirement_names := self.cleaned_data["dietary_requirements"]:
            dietary_requirements = ingredient_models.DietaryRequirement.objects.filter(
                name__in=dietary_requirement_names
            ).values_list("id", flat=True)
            self.instance.dietary_requirements_satisfied.add(*dietary_requirements)
        return self.instance

    def clean_category(self) -> ingredient_models.IngredientCategory:
        category_name = self.cleaned_data["category"]
        try:
            return ingredient_models.IngredientCategory.objects.get(name=category_name)
        except ingredient_models.IngredientCategory.DoesNotExist as exc:
            raise django_forms.ValidationError(str(exc)) from exc

    def clean_dietary_requirements(self) -> list[str]:
        if not (dietary_requirements := self.cleaned_data["dietary_requirements"]):
            return []
        return dietary_requirements.split(M2M_DELIMITER)


class IngredientNutritionalInformation(django_forms.ModelForm):
    ingredient = django_forms.CharField()
    nutrient = django_forms.CharField()

    class Meta:
        model = ingredient_models.IngredientNutritionalInformation
        fields = ["quantity_per_gram", "units"]

    def save(
        self, commit: bool = True
    ) -> ingredient_models.IngredientNutritionalInformation:
        self.instance.ingredient = self.cleaned_data["ingredient"]
        self.instance.nutrient = self.cleaned_data["nutrient"]
        return super().save(commit=commit)

    def clean_ingredient(self) -> ingredient_models.Ingredient:
        ingredient_name = self.cleaned_data["ingredient"]
        try:
            return ingredient_models.Ingredient.objects.get(name=ingredient_name)
        except ingredient_models.Ingredient.DoesNotExist as exc:
            raise django_forms.ValidationError(str(exc)) from exc

    def clean_nutrient(self) -> ingredient_models.Nutrient:
        nutrient_name = self.cleaned_data["nutrient"]
        try:
            return ingredient_models.Nutrient.objects.get(name=nutrient_name)
        except ingredient_models.Nutrient.DoesNotExist as exc:
            raise django_forms.ValidationError(str(exc)) from exc
