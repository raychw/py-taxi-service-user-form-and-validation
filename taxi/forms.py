from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


class ValidatorMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise forms.ValidationError("Length of license number must be 8!")
        if not (license_number[:3].isupper() and license_number[:3].isalpha()):
            raise forms.ValidationError(
                "First 3 characters of license number must be uppercase!"
            )
        if not license_number[3:].isdigit():
            raise forms.ValidationError(
                "Last 5 characters of license number must be digits!"
            )
        return license_number


class DriverLicenseUpdateForm(forms.ModelForm, ValidatorMixin):
    class Meta:
        model = Driver
        fields = ["license_number"]


class DriverCreateForm(UserCreationForm, ValidatorMixin):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number", "first_name", "last_name"
        )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = Car
        fields = "__all__"
