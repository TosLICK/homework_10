import os
import django

from pymongo import MongoClient

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hw_project.settings")
django.setup()

from quotes.models import Author, Quote, Tag


client = MongoClient("mongodb://localhost:27017/")

db = client.hw

authors = db.authors.find()
for author in authors:
    Author.objects.get_or_create(
        fullname=author['fullname'],
        born_date=author['born_date'],
        born_location=author['born_location'],
        description=author['description'],
    )

quotes = db.quotes.find()

for quote in quotes:
    tags = []
    for tag in quote['tags']:
        tag_obj, *_ = Tag.objects.get_or_create(name=tag)
        tags.append(tag_obj)

    exist_quote = bool(len(Quote.objects.filter(quote=quote['quote'])))

    if not exist_quote:
        author = db.authors.find_one({'_id': quote['author']})
        author_obj = Author.objects.get(fullname=author['fullname'])
        quote_obj = Quote.objects.create(
            quote=quote['quote'],
            author=author_obj
        )
        for tag in tags:
            quote_obj.tags.add(tag)
