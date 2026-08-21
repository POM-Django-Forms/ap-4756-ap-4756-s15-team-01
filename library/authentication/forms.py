from django import forms
from .models import CustomUser
from django.contrib.auth import authenticate

ROLE_CHOICES = (
    (0, 'Visitor'),
    (1, 'Librarian'),
)


class RegisterForm(forms.Form):
    first_name = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    middle_name = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        max_length=100,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    role = forms.TypedChoiceField(
        choices=ROLE_CHOICES,
        coerce=int,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('The user with this email already exists.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'})
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise forms.ValidationError('Invalid email or password.')
            self.user_cache = user
        return cleaned_data


class ProfileUpdateForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter new password'}),
        required=False,
        label='New Password (leave blank to keep current)'
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'middle_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '20'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '20'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '20'}),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name', '').strip()
        if not first_name:
            raise forms.ValidationError("First name is required.")
        if len(first_name) > 20:
            raise forms.ValidationError("First name must be under 20 characters.")
        return first_name

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get('password')

        if new_password:
            user.set_password(new_password)

        if commit:
            user.save()
        return user
