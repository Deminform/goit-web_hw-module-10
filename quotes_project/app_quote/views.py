import json

from django.shortcuts import redirect, render
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy

from .models import Quote, Author
from .forms import QuoteForm, AuthorForm, QuoteEditForm


def index(request):
    result_quotes = Quote.objects.all()
    return render(request, 'app_quote/index.html', context={'result_quotes': result_quotes})


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
    success_url = reverse_lazy('app_quotes:my-quotes')


class AuthorView(CreateView):
    model = Author
    form_class = AuthorForm
    template_name = 'app_quote/add-author.html'
    success_url = reverse_lazy('app_quotes:my-quotes')


def author(request, pk):
    result_author = Author.objects.filter(pk=pk)
    return render(request, 'app_quote/author.html', context={'result_author': result_author})


def my_quotes(request):
    result_quotes = Quote.objects.all()
    return render(request, 'app_quote/my-quotes.html', context={'result_quotes': result_quotes})


def remove_quote(request, pk):
    quote = Quote.objects.filter(pk=pk)
    quote.delete()
    return redirect('app_quotes:my-quotes')


class QuoteUpdateView(UpdateView):
    model = Quote
    form_class = QuoteEditForm
    template_name = 'app_quote/edit-quote.html'
    success_url = reverse_lazy('app_quotes:my-quotes')


