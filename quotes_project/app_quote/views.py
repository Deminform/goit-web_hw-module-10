import json
import os
import re

from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.conf import settings

import dateparser

from .models import Quote, Author, Tag
from .forms import QuoteForm, AuthorForm, QuoteEditForm


def initialize_database(request):
    file_path_author = os.path.join(settings.MEDIA_ROOT, 'seeds', 'authors.json')
    file_path_quotes_tags = os.path.join(settings.MEDIA_ROOT, 'seeds', 'quotes.json')

    with open(file_path_author, 'r', encoding='utf-8') as file:
        result = json.load(file)

        for item in result:
            author_result = Author(
                fullname=item['fullname'],
                born_date=dateparser.parse(item['born_date']).date(),
                born_location=item['born_location'],
                description=item['description'],
            )
            author_result.save()

    with open(file_path_quotes_tags, 'r', encoding='utf-8') as file:
        result = json.load(file)

        for item in result:
            try:
                author_result = Author.objects.get(fullname=item['author'])
            except Author.DoesNotExist:
                author_result = None
            if author_result:
                quote = Quote(
                    quote=item['quote'],
                    author=author_result,
                )
                quote.save()
                for tag_name in item['tags']:
                    tag_obj, _ = Tag.objects.get_or_create(name=tag_name)
                    quote.tags.add(tag_obj)
    return redirect('app_quotes:index')


def index(request):
    result_quotes = Quote.objects.all()
    paginator = Paginator(result_quotes, settings.PAGE_SIZE)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'app_quote/index.html', context={"page_obj": page_obj})


def author(request, pk):
    result_author = Author.objects.get(pk=pk)
    return render(request, 'app_quote/author.html', context={'result_author': result_author})


def my_quotes(request):
    result_quotes = Quote.objects.all()
    paginator = Paginator(result_quotes, settings.PAGE_SIZE)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'app_quote/my-quotes.html', context={'page_obj': page_obj})


def remove_quote(request, pk):
    quote = Quote.objects.filter(pk=pk)
    quote.delete()
    return redirect('app_quotes:my-quotes')


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


class QuoteUpdateView(UpdateView):
    model = Quote
    form_class = QuoteEditForm
    template_name = 'app_quote/edit-quote.html'
    success_url = reverse_lazy('app_quotes:my-quotes')


