from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    fullname = models.CharField(max_length=100)
    born_date = models.DateField()
    born_location = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return self.fullname

    class Meta:
        ordering = ['fullname']


class Tag(models.Model):
    name = models.CharField(max_length=40, unique=True, null=False)

    def __str__(self):
        return self.name


class Quote(models.Model):
    tags = models.ManyToManyField(Tag, related_name='quotes')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    quote = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
