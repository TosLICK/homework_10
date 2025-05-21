from django.forms import ModelForm, CharField, TextInput, Textarea, Form
from .models import Author, Quote


class AuthorForm(ModelForm):
    fullname = CharField(min_length=3, max_length=50, required=True, widget=TextInput())
    born_date = CharField(max_length=50, required=True, widget=TextInput())
    born_location = CharField(max_length=150, required=True, widget=TextInput())
    description = Textarea()
    
    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']

# class QuoteForm(ModelForm):
class QuoteForm(Form):
    quote = CharField(max_length=300, required=True, widget=TextInput(), label="Quote")
    author = CharField(max_length=100, required=True, widget=TextInput(), label="Author")
    # author = ModelChoiceField(queryset=Author.objects.all(), required=True, label="Author", empty_label="(Nothing)")
    tags = CharField(max_length=100, required=True, widget=TextInput(), label="Tags, separated by spaces")

    class Meta:
        model = Quote
        fields = ['quote', 'author', 'tags']
