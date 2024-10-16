import os

import scrapy
import json
from scrapy.crawler import CrawlerProcess
from django.conf import settings


class QuotesSpider(scrapy.Spider):
    name = 'quotes_spider'
    start_urls = ['https://quotes.toscrape.com/']

    quotes_data = []
    authors_data = []
    authors_visited = set()

    file_path_author = os.path.join(settings.MEDIA_ROOT, 'seeds', 'authors.json')
    file_path_quotes_tags = os.path.join(settings.MEDIA_ROOT, 'seeds', 'quotes.json')

    def parse(self, response):
        for quote in response.css('div.quote'):
            text = quote.css('span.text::text').get().strip()
            author = quote.css('small.author::text').get().strip()
            tags = quote.css('div.tags a.tag::text').getall()
            self.quotes_data.append({
                'tags': tags,
                'author': author,
                'quote': text
            })

            author_url = quote.css('span a::attr(href)').get()
            if author_url and author not in self.authors_visited:
                self.authors_visited.add(author)
                yield response.follow(author_url, self.parse_author)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_author(self, response):
        fullname = response.css('h3.author-title::text').get().strip()
        born_date = response.css('span.author-born-date::text').get().strip()
        born_location = response.css('span.author-born-location::text').get().strip()
        description = response.css('div.author-description::text').get().strip()
        self.authors_data.append({
            'fullname': fullname,
            'born_date': born_date,
            'born_location': born_location,
            'description': description
        })

    def close(self, reason):
        with open(self.file_path_quotes_tags, 'w', encoding='utf-8') as f:
            json.dump(self.quotes_data, f, ensure_ascii=False, indent=2)
        with open(self.file_path_author, 'w', encoding='utf-8') as f:
            json.dump(self.authors_data, f, ensure_ascii=False, indent=2)


def run_spider():
    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.start()
