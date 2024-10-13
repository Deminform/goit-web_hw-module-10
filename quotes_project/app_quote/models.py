from django.db import models


class Author(models.Model):
    fullname = models.CharField(max_length=100)
    born_date = models.DateField()
    born_location = models.CharField(max_length=150)
    description = models.TextField()


class Quote(models.Model):
    tags = models.CharField(max_length=50)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    quote = models.TextField()
