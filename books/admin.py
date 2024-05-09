from django.contrib import admin

from books.models import Book, BookImage

# Register your models here.

admin.site.register(Book)
admin.site.register(BookImage)