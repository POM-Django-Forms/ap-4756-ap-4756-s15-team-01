from django import forms
from order.models import Order
from book.models import Book


class OrderForm(forms.ModelForm):
    book = forms.ModelChoiceField(
        queryset=Book.objects.filter(count__gt=0),
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Choose a book',
    )

    class Meta:
        model = Order
        fields = ('book',)