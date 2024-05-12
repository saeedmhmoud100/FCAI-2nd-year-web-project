from django.contrib import messages
from django.db.models import Q
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

    def get_queryset(self):
        queryset = self.queryset

        queryset = self.apply_search(queryset)
        queryset = self.apply_filter(queryset)

        return queryset
    def apply_search(self, queryset):
        q = self.request.GET.get('q', '')
        search_by = self.request.GET.get('search_by', 'all')
        if not q:
            return queryset

        if search_by == 'title':
            queryset = queryset.filter(title__icontains=q)
        elif search_by == 'author':
            queryset = queryset.filter(author__icontains=q)
        elif search_by == 'description':
            queryset = queryset.filter(description__icontains=q)
        elif search_by == 'category':
            queryset = queryset.filter(category__title__icontains=q)
        elif q == 'all':
            queryset = queryset.filter(
                Q(title__icontains=q) | Q(author__icontains=q) | Q(category__title__icontains=q))
        return queryset
    def apply_filter(self, queryset):
        available = self.request.GET.get('available', '')
        rating = self.request.GET.get('rating', '')
        price_from = self.request.GET.get('price_from', 0)
        price_to = self.request.GET.get('price_to', 100000000000000000000)
        if available != '' and available:
            queryset = queryset.filter(borrower=None)
        # if rating:
        #     queryset = queryset.filter(ratings=rating)
        if price_from < price_to:
            queryset = queryset.filter(price__range=(price_from, price_to))
        return queryset



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['search_by'] = self.request.GET.get('search_by', 'all')
        context['available'] = self.request.GET.get('available', '')
        context['rating'] = int(self.request.GET.get('rating', 0))
        context['price_from'] = self.request.GET.get('price_from', '')
        context['price_to'] = self.request.GET.get('price_to', '')
        return context



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
        return render(request, 'books/borrow_book.html', {'object': book})

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
