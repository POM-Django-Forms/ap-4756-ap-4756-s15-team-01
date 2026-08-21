from django import forms
from .models import Author


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'surname', 'patronymic']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '20'}),
            'surname': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '20'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '20'}),
        }
        labels = {
            'name': 'Name',
            'surname': 'Surname',
            'patronymic': 'Patronymic',
        }

    def clean(self):
        cleaned_data = super().clean()
        for field in ['name', 'surname', 'patronymic']:
            val = cleaned_data.get(field)
            if val:
                cleaned_data[field] = val.strip()
        return cleaned_data

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise forms.ValidationError("The name is required.")
        if len(name) > 20:
            raise forms.ValidationError("The name must contain fewer than 20 characters.")
        return name

    def clean_surname(self):
        surname = self.cleaned_data.get('surname', '').strip()
        if not surname:
            raise forms.ValidationError("The surname is required.")
        if len(surname) > 20:
            raise forms.ValidationError("The surname must contain fewer than 20 characters.")
        return surname

    def clean_patronymic(self):
        patronymic = self.cleaned_data.get('patronymic', '').strip()
        if not patronymic:
            raise forms.ValidationError("The patronymic is required.")
        if len(patronymic) > 20:
            raise forms.ValidationError("The patronymic must contain fewer than 20 characters.")
        return patronymic


class AuthorFilterForm(forms.Form):
    name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name'
        })
    )
