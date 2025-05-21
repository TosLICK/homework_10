from bson import ObjectId
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator

# Create your views here.
from .utils import get_mongodb
from .forms import AuthorForm, QuoteForm
from .mongo_models import Author, Quote
from .mongo_models import Author as MongoAuthor

from mongoengine import connect


def main(request, page=1):
    # return render(request, 'quotes/main.html')
    db = get_mongodb()
    quotes = db.quotes.find()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page})

@login_required
def new_author(request):
    db = get_mongodb()
    connect('hw', host='mongodb://localhost:27017/hw')
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            author = Author(
                fullname=data['fullname'],
                born_date=data['born_date'],
                born_location=data['born_location'],
                description=data['description']
            )
            author.save()
            return redirect(to='quotes:author', id=author.id)
        else:
            return render(request, 'quotes/new_author.html', {'form': form})

    return render(request, 'quotes/new_author.html', {'form': AuthorForm()})

@login_required
def new_quote(request):
    connect('hw', host='mongodb://localhost:27017/hw')
    authors = list(MongoAuthor.objects.all())
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            tags = [tag.strip() for tag in data['tags'].split()]
            # author_id = request.POST.get('author')
            author_id = data['author']
            # if author_id:
            try:
                # author_obj = MongoAuthor.objects.get(id=str(author_id))
                # author_obj = MongoAuthor.objects.get(id=ObjectId(author_id))
                # author_obj = Author.objects.get(id=author_id)
                author_obj = MongoAuthor.objects.get(id=author_id)
                quote = Quote(
                    quote=data['quote'],
                    author=author_obj,
                    tags=tags
                )
                quote.save()
                return redirect(to='quotes:root')
            except Exception as e:
                form.add_error('author', f'Author not found or id error: {e}')
            # else:
            #     form.add_error('author', 'Author is required.')
        return render(request, 'quotes/new_quote.html', context={'form': form, 'authors': authors})

    return render(request, 'quotes/new_quote.html', context={'form': QuoteForm(), 'authors': authors})

def author(request, id):
    db = get_mongodb()
    author = db.authors.find_one({'_id': ObjectId(id)})
    if author is None:
        return render(request, 'quotes/author.html', context={'author': None, 'quotes': None})
    
    quotes = db.quotes.find({'author': author['_id']})
    return render(request, 'quotes/author.html', context={'quotes': quotes, 'author': author})
