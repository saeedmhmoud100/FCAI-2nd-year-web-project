from django.shortcuts import render
from django.views.generic import ListView, DetailView

from books.models import Book


# Create your views here.


class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'


class BookDetailView(DetailView):
    model = Book

    def get_queryset(self):
        return Book.objects.filter(slug=self.kwargs['slug'])