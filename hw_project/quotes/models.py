from django.db import models


# Create your models here.
class Author(models.Model):
    fullname = models.CharField(max_length=50)
    born_date = models.CharField(max_length=50)
    born_location = models.CharField(max_length=150)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)


class Quote(models.Model):
    quote = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='quotes')
    author = models.ForeignKey(Author, related_name='quotes', on_delete=models.CASCADE, default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
