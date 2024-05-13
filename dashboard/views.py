from django.views.generic import ListView

from books.models import Book
from books.views import BookListView
from categories.views import CategoryListView


# Create your views here.

class AdminBookListView(BookListView):
    model = Book
    template_name = 'dashboard/book_list.html'

    def get_queryset(self):
        return Book.objects.all().order_by('id')


class AdminCategoryListView(CategoryListView):
    template_name = 'dashboard/categories_list.html'
