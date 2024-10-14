import json

from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .models import Quote, Author
from .forms import QuoteForm, AuthorForm


def index(request):
    return render(request, 'app_quote/index.html')


def quotes(request):
    context = Quote.objects.all()
    return None


def initialize_database(request):
    with open('seeds/quotes.json', 'r', encoding='utf-8') as file:
        result = json.load(file)

        for item in result:
            quote = Quote(
                tags=item['tags'],
                author=item['author'],
                quote=item['quote'],
            )
            quote.save()

    with open('seeds/authors.json', 'r', encoding='utf-8') as file:
        result = json.load(file)

        for item in result:
            author = Author(
                fullname=item['fullname'],
                born_date=item['born_date'],
                born_location=item['born_location'],
                description=item['description'],
            )
            author.save()


class QuoteView(CreateView):
    model = Quote
    form_class = QuoteForm
    template_name = 'app_quote/add-quote.html'
    success_url = reverse_lazy('quotes:my-quotes')


class AuthorView(CreateView):
    model = Author
    form_class = AuthorForm
    template_name = 'app_quote/add-author.html'
    success_url = reverse_lazy('quotes:my-quotes')


def my_quotes(request):
    result_quotes = Quote.objects.all()
    return render(request, 'app_quote/my-quotes.html', context={'result_quotes': result_quotes})
