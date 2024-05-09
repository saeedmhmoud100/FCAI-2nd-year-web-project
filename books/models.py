from django.db import models

from project.db.models import BasicModel


# Create your models here.

def book_cover_path(instance, filename):
    return f'book_covers/{instance.slug}/{filename}'



class Book(BasicModel):
    title = models.CharField(max_length=100)
    # author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    # rating = models.DecimalField(max_digits=3, decimal_places=2)
    cover = models.ImageField(upload_to=book_cover_path, blank=True)
    views = models.IntegerField(default=0)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    is_borrowed = models.BooleanField(default=True)
    def __str__(self):
        return self.title