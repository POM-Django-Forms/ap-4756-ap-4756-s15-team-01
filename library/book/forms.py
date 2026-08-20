from django import forms
from django.core.exceptions import ValidationError
from .models import Book
from author.models import Author


def validate_non_negative(value):
    if value < 0:
        raise ValidationError('Count cannot be negative.')


class BookForm(forms.ModelForm):
    authors = forms.ModelMultipleChoiceField(
        queryset=Author.objects.all(),
        required=False,
        widget=forms.SelectMultiple
    )
    count = forms.IntegerField(validators=[validate_non_negative])

    class Meta:
        model = Book
        fields = ('name', 'description', 'count')
        labels = {
            'name': 'Name',
            'description': 'Description',
            'count': 'Available Copies',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['authors'].label_from_instance = lambda obj: f"{obj.name} {obj.surname}"