from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from books.forms import CreateBookForm, UpdateBookForm
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
        if (self.request.user.is_authenticated):
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

    def get_success_url(self):
        book_url = self.object.get_absolute_url()
        success_message = mark_safe(f'Book updated successfully <a href="{book_url}">View Book</a>')
        messages.add_message(self.request, messages.SUCCESS, success_message)
        return reverse('update_book', args=[self.object.slug])
        # return reverse('book_details', args=[self.object.slug])


def delete_book(request, slug):
    book = Book.objects.active().get(slug=slug)
    print(book, slug)
    if request.method == 'POST':
        book.delete()
        messages.add_message(request, messages.SUCCESS, 'Book deleted successfully')
        return redirect('book_list')
    return render(request, 'books/delete_book.html', {'object': book})


class BorrowBookView(View):
    def get(self, request, slug):
        book = Book.objects.active().get(slug=slug)
        if book.is_borrowed:
            messages.add_message(request, messages.ERROR, 'Book is already borrowed')
            return redirect(reverse('book_details', args=[slug]))
        return render(request, 'books/borrow_book.html',{'object': book})

    def post(self, request, slug):
        book = Book.objects.active().get(slug=slug)
        book.borrower = request.user
        book.save()
        messages.add_message(request, messages.SUCCESS, 'Book borrowed successfully')
        return redirect('borrowed_books')

class ReturnBookView(View):
    def get(self, request, slug):
        book = Book.objects.active().get(slug=slug)
        if book.borrower == request.user:
            book.borrower = None
            book.save()
            messages.add_message(request, messages.SUCCESS, 'Book returned successfully')
            return redirect('borrowed_books')
        return redirect('book_details', slug=slug)
