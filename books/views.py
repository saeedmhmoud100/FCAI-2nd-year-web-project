from django.shortcuts import render
from django.views.generic import ListView, DetailView

from books.models import Book


# Create your views here.


class BookListView(ListView):
    queryset = Book.objects.active()
    context_object_name = 'books'


class BorrowedBookListView(ListView):
    queryset = Book.objects.active()
    template_name = 'books/borrowed_books_list.html'
    def get_queryset(self):
        return self.queryset.get_borrowed_by_user(self.request.user)


class BookDetailView(DetailView):
    model = Book

    def get_queryset(self):
        return Book.objects.active().filter(slug=self.kwargs['slug'])
