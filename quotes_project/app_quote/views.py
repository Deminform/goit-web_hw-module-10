import json

from django.shortcuts import render
from .models import Quote, Author


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
