from django.contrib.auth.forms import forms
from django.forms import CharField, DateField, TextInput

from .models import Quote, Author


class AuthorForm(forms.ModelForm):
    fullname = CharField(max_length=100, required=True, widget=TextInput(attrs={'class': 'form-control'}))
    born_date = DateField(required=True)
    born_location = CharField(max_length=150, required=True, widget=TextInput(attrs={'class': 'form-control'}))
    description = CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = Author
        fields = ('fullname', 'born_date', 'born_location', 'description')


class QuoteForm(forms.ModelForm):
    quote = CharField(max_length=100, required=True, widget=TextInput(attrs={'class': 'form-control'}))
    author = DateField(required=True)
    tags = CharField(max_length=150, required=True, widget=TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Author
        fields = ('quote', 'author', 'tags')

