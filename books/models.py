from django.conf import settings
from django.db import models

from categories.models import Category
from project.db.models import BasicModel

# Create your models here.

User = settings.AUTH_USER_MODEL


def book_cover_path(instance, filename):
    return f'book_covers/{instance.slug}/{filename}'


class BookImage(BasicModel):
    image = models.ImageField(upload_to=book_cover_path)

    def __str__(self):
        return self.book.title


class Book(BasicModel):
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books')
    cover = models.OneToOneField(BookImage, on_delete=models.CASCADE, related_name='book')
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    views = models.IntegerField(default=0)
    description = models.TextField()
    is_borrowed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
