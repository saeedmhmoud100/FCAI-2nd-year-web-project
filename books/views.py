from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core import serializers
from django.db.models import Q, Avg, Sum, Value
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from books.forms import CreateBookForm, UpdateBookForm
from books.models import Book
from django.db.models import CharField
from project.permissions import check_authenticated, check_user


# Create your views here.

class BookListViewAPI(ListView):
    queryset = Book.objects.active()
    context_object_name = 'books'

    def get_queryset(self):
        queryset = self.queryset

        queryset = self.apply_search(queryset)
        queryset = self.apply_filter(queryset)
        queryset = self.apply_ordering(queryset)

        return queryset

    def apply_ordering(self, queryset):
        ordering = self.request.GET.get('order_by', '?')
        if ordering == 'price_desc':
            queryset = queryset.order_by('-price')
        elif ordering == 'price_acs':
            queryset = queryset.order_by('price')
        elif ordering == 'rating_desc':
            queryset = queryset.annotate(avg_rating=Avg('ratings__rating')).order_by('-avg_rating')
        elif ordering == 'rating_acs':
            queryset = queryset.annotate(avg_rating=Avg('ratings__rating')).order_by('avg_rating')
        elif ordering == 'views_desc':
            queryset = queryset.annotate(total_views=Sum('user_viewers__count')).order_by('-total_views')
        elif ordering == 'views_acs':
            queryset = queryset.annotate(total_views=Sum('user_viewers__count')).order_by('total_views')
        elif ordering == 'time_desc':
            queryset = queryset.order_by('-created_at')
        elif ordering == 'time_acs':
            queryset = queryset.order_by('created_at')
        else:
            queryset = queryset.order_by('?')
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
        elif search_by == 'rating':
            queryset = queryset.filter(ratings__review__icontains=q).distinct()
        elif search_by == 'all':
            queryset = queryset.filter(
                Q(title__icontains=q) | Q(author__icontains=q) | Q(category__title__icontains=q) | Q(
                    description__icontains=q) | Q(ratings__review__icontains=q)).distinct()
        return queryset

    def apply_filter(self, queryset):
        available = self.request.GET.get('available', '')
        rating = self.request.GET.get('rating', '')
        price_from = self.request.GET.get('price_from', 0)
        price_to = self.request.GET.get('price_to', 100000000000000000000)
        print(self.request.GET)
        if available != '' and available:
            queryset = queryset.filter(borrower=None)
        if rating != '' and int(rating) > 0:
            queryset = queryset.annotate(avg_rating=Avg('ratings__rating')).filter(avg_rating__gte=rating)
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
        context['order_by'] = self.request.GET.get('order_by', '')
        return context

    def get(self,request,*args,**kwargs):
        queryset = self.get_queryset()
        print(queryset)
        book_list = []
        for book in queryset:
            book_list.append({
                'slug': book.slug,
                'id': book.id,
                'details_url': request.build_absolute_uri(book.get_absolute_url()),
                'update_url': request.build_absolute_uri(reverse('update_book', args=[book.slug])),
                'delete_url': request.build_absolute_uri(reverse('delete_book', args=[book.slug])),
                'title': book.title,
                'author': book.author,
                'category': book.category.title,
                'price': str(book.price),
                'available':  bool(not book.borrower),
                'rating': book.rating,
                'description': book.description,
                'image_url': request.build_absolute_uri(book.image.url),
                'is_admin': request.user.is_authenticated and request.user.is_staff,
            })


        return JsonResponse(book_list, safe=False)
class BookListView(ListView):
    queryset = Book.objects.active()


class BorrowedBookListView(UserPassesTestMixin, ListView):
    queryset = Book.objects.active()
    template_name = 'books/borrowed_books_list.html'

    def test_func(self):
        cond = self.request.user.is_authenticated
        if not cond:
            messages.add_message(self.request, messages.ERROR, 'You need to login to view borrowed books')
        return cond

    def get_queryset(self):
        return self.queryset.get_borrowed_by_user(self.request.user)


class BookDetailView(DetailView):
    model = Book

    def get_queryset(self):
        if self.request.user.is_authenticated:
            Book.objects.active().get(slug=self.kwargs['slug']).increase_views(self.request.user)
        return Book.objects.active().filter(slug=self.kwargs['slug'])


class BookCreateView(UserPassesTestMixin, CreateView):
    model = Book
    form_class = CreateBookForm
    template_name = 'books/add_book.html'

    def test_func(self):
        cond = self.request.user.is_authenticated and self.request.user.is_staff
        print(cond)
        if not cond:
            messages.add_message(self.request, messages.ERROR, 'You need to be admin to add books')
        return cond

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        book = form.save()
        book.set_image(form.cleaned_data['image'])
        book.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)

    def get_success_url(self):
        book_url = self.object.get_absolute_url()
        success_message = mark_safe(f'Book added successfully <a href="{book_url}">View Book</a>')
        messages.add_message(self.request, messages.SUCCESS, success_message)
        return reverse('add_book')
        # return reverse('book_details', args=[self.object.slug])


class BookUpdateView(UserPassesTestMixin, UpdateView):
    model = Book
    form_class = UpdateBookForm
    template_name = 'books/update_book.html'

    def test_func(self):
        cond = self.request.user.is_staff or self.request.user == self.get_object().uploaded_by
        if not cond:
            messages.add_message(self.request, messages.ERROR,
                                 'You need to be admin or the owner of the book to can update books')
        return cond

    def get_queryset(self):
        return Book.objects.all().filter(slug=self.kwargs['slug'])

    def form_valid(self, form):
        book = form.save()
        if form.cleaned_data['image']:
            book.set_image(form.cleaned_data['image'])
        book.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)

    def get_success_url(self):
        book_url = self.object.get_absolute_url()
        success_message = mark_safe(f'Book updated successfully <a href="{book_url}">View Book</a>')
        messages.add_message(self.request, messages.SUCCESS, success_message)
        return reverse('update_book', args=[self.object.slug])
        # return reverse('book_details', args=[self.object.slug])


def delete_book(request, slug):
    book = Book.objects.all().get(slug=slug)
    if request.user.is_superuser or request.user == book.uploaded_by:
        if request.method == 'POST':
            book.delete()
            messages.add_message(request, messages.SUCCESS, 'Book deleted successfully')
            return redirect('book_list')
        return render(request, 'books/delete_book.html', {'object': book})
    else:
        messages.add_message(request, messages.ERROR,
                             'You need to be admin or the owner of the book to can delete books')
        return redirect('book_list')


class BorrowBookView(UserPassesTestMixin, View):

    def test_func(self):
        cond = self.request.user.is_authenticated
        if not cond:
            messages.add_message(self.request, messages.ERROR, 'You need to login to borrow books')
        return cond

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


class ReturnBookView(UserPassesTestMixin, View):

    def test_func(self):

        book = Book.objects.active().get(slug=self.kwargs['slug'])
        cond = self.request.user.is_authenticated and self.request.user == book.uploaded_by
        if not cond:
            messages.add_message(self.request, messages.ERROR, 'You need to login to return books')
        return cond

    def get(self, request, slug):
        book = Book.objects.active().get(slug=slug)
        self.book = book
        if book.borrower == request.user:
            book.borrower = None
            book.save()
            messages.add_message(request, messages.SUCCESS, 'Book returned successfully')
            return redirect('borrowed_books')
        return redirect('book_details', slug=slug)
