from django.contrib import messages
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from books.forms import CreateBookForm, UpdateBookForm
from books.models import Book, BookImage


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
        if(self.request.user.is_authenticated):
            Book.objects.active().get(slug=self.kwargs['slug']).increase_views(self.request.user)
        return Book.objects.active().filter(slug=self.kwargs['slug'])


class BookCreateView(CreateView):
    model = Book
    form_class = CreateBookForm
    template_name = 'books/add_book.html'

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        book = form.save()
        book.set_image(form.cleaned_data['image'])
        book.save()
        return super().form_valid(form)

    def get_success_url(self):
        book_url = self.object.get_absolute_url()
        success_message = mark_safe(f'Book added successfully <a href="{book_url}">View Book</a>')
        messages.add_message(self.request, messages.SUCCESS, success_message)
        return reverse('add_book')
        # return reverse('book_details', args=[self.object.slug])


class BookUpdateView(UpdateView):
    model = Book
    form_class = UpdateBookForm
    template_name = 'books/update_book.html'

    def get_queryset(self):
        return Book.objects.active().filter(slug=self.kwargs['slug'])

    def form_valid(self, form):
        book = form.save()
        if form.cleaned_data['image']:
            book.set_image(form.cleaned_data['image'])
        book.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def get_success_url(self):
        book_url = self.object.get_absolute_url()
        success_message = mark_safe(f'Book updated successfully <a href="{book_url}">View Book</a>')
        messages.add_message(self.request, messages.SUCCESS, success_message)
        return reverse('update_book', args=[self.object.slug])
        # return reverse('book_details', args=[self.object.slug])
