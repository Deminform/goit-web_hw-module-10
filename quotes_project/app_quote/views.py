import json
import logging

from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Count

import dateparser

from .models import Quote, Author, Tag
from .forms import QuoteForm, AuthorForm, QuoteEditForm
from .scrap import QuotesSpider, run_spider



@login_required
def initialize_database(request):
    run_spider()

    with open(QuotesSpider.file_path_author, 'r', encoding='utf-8') as file:
        result = json.load(file)

        for item in result:
            author_result = Author(
                fullname=item['fullname'],
                born_date=dateparser.parse(item['born_date']).date(),
                born_location=item['born_location'],
                description=item['description'],
            )
            author_result.save()

    with open(QuotesSpider.file_path_quotes_tags, 'r', encoding='utf-8') as file:
        result = json.load(file)

        for item in result:
            try:
                author_result = Author.objects.get(fullname=item['author'])
                user_result = User.objects.first()
            except Author.DoesNotExist:
                author_result = None
            if author_result:
                quote = Quote(
                    quote=item['quote'],
                    author=author_result,
                    created_by_id=user_result.id,
                )
                quote.save()
                for tag_name in item['tags']:
                    tag_obj, _ = Tag.objects.get_or_create(name=tag_name)
                    quote.tags.add(tag_obj)
    return redirect('app_quotes:index')


def index(request):
    result_quotes = Quote.objects.all().order_by('id')
    tags_result = Tag.objects.annotate(quote_count=Count('quotes')).order_by('-quote_count')[:10]
    paginator = Paginator(result_quotes, settings.PAGE_SIZE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        'title': 'Quotes | Home',
        "top_tags": tags_result
    }
    return render(request, 'app_quote/index.html', context)


def tags(request, tag):
    result_quotes = Quote.objects.filter(tags__name__in=[tag]).order_by('id').all()
    tags_result = Tag.objects.annotate(quote_count=Count('quotes')).order_by('-quote_count')[:10]
    paginator = Paginator(result_quotes, settings.PAGE_SIZE)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
        'title': 'Search result for ' + tag,
        "search_request": tag,
        "top_tags": tags_result
    }
    return render(request, 'app_quote/search.html', context)


def top_tags(request):
    tags_result = Tag.objects.annotate(quote_count=Count('quotes')).order_by('-quote_count')[:10]
    context = {"top_tags": tags_result}
    return render(request, 'app_quote/top-tags.html', context)


def author(request, pk):
    result_author = Author.objects.get(pk=pk)
    context = {
        "result_author": result_author,
        'title': 'About ' + result_author.fullname
    }
    return render(request, 'app_quote/author.html', context)


@login_required
def my_quotes(request):
    result_quotes = Quote.objects.filter(created_by_id=request.user.id)
    paginator = Paginator(result_quotes, settings.PAGE_SIZE)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'app_quote/my-quotes.html', context={'page_obj': page_obj})


@login_required
def remove_quote(request, pk):
    quote = get_object_or_404(Quote, pk=pk)
    if quote.created_by != request.user:
        raise PermissionDenied('You are not allowed to delete this quote.')
    quote.delete()
    return redirect('app_quotes:my-quotes')


class QuoteView(CreateView):
    model = Quote
    form_class = QuoteForm
    template_name = 'app_quote/add-quote.html'
    success_url = reverse_lazy('app_quotes:my-quotes')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class AuthorView(CreateView):
    model = Author
    form_class = AuthorForm
    template_name = 'app_quote/add-author.html'
    success_url = reverse_lazy('app_quotes:my-quotes')


class QuoteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Quote
    form_class = QuoteEditForm
    template_name = 'app_quote/edit-quote.html'
    success_url = reverse_lazy('app_quotes:my-quotes')

    def test_func(self):
        quote = self.get_object()
        return quote.created_by == self.request.user

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied('You are not allowed to edit this object.')
        else:
            return super().handle_no_permission()
