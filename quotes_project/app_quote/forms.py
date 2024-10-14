from django.forms import CharField, DateField, ModelChoiceField, TextInput, ModelForm, DateInput, Select, Textarea

from .models import Quote, Author, Tag


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

    def save(self, commit=True):
        quote = super().save(commit=False)
        if commit:
            quote.save()
        tags_str = self.cleaned_data['tags']
        tags_list = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
        for tag_name in tags_list:
            tag_obj, created = Tag.objects.get_or_create(name=tag_name)
            quote.tags.add(tag_obj)
        return quote


class QuoteEditForm(ModelForm):
    tags = CharField(
        required=True,
        widget=TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tags (coma-separated)'}),
        help_text='Enter tags separated by commas'
    )

    class Meta:
        model = Quote
        fields = ('quote', 'author', 'tags')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['tags'].initial = ', '.join([tag.name for tag in self.instance.tags.all()])

    def save(self, commit=True):
        quote = super().save(commit=False)
        if commit:
            quote.save()

        tags_str = self.cleaned_data['tags']
        tags_list = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
        quote.tags.clear()
        for tag_name in tags_list:
            tag_obj, created = Tag.objects.get_or_create(name=tag_name)
            quote.tags.add(tag_obj)
        return quote
