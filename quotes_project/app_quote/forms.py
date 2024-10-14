from django.forms import CharField, DateField, ModelChoiceField, TextInput, ModelForm, DateInput, Select, Textarea

from .models import Quote, Author


class AuthorForm(ModelForm):
    fullname = CharField(
        max_length=100,
        required=True,
        widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Fullname'}))

    born_date = DateField(
        required=True,
        widget=DateInput(attrs={'class': 'form-control', 'placeholder': 'Born Date', 'type': 'date'}))

    born_location = CharField(
        max_length=150,
        required=True,
        widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Born Location'}))

    description = CharField(
        required=True,
        widget=Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'})
    )

    class Meta:
        model = Author
        fields = ('fullname', 'born_date', 'born_location', 'description')


class QuoteForm(ModelForm):
    quote = CharField(
        required=True,
        widget=Textarea(attrs={'class': 'form-control', 'placeholder': 'Quote'}))

    author = ModelChoiceField(
        queryset=Author.objects.all(),
        required=True,
        widget=Select(attrs={'class': 'form-select'}))

    tags = CharField(
        max_length=150,
        required=True,
        widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Tags'}))

    class Meta:
        model = Quote
        fields = ('quote', 'author', 'tags')
