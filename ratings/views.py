from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView

from books.models import Book
from ratings.forms import RatingForm
from ratings.models import Rating


# Create your views here.

class CreateRatingView(UserPassesTestMixin, CreateView):
    model = Rating
    form_class = RatingForm
    template_name = 'ratings/add_rating.html'
    raise_exception = False
    def test_func(self):

        if not self.request.user.is_authenticated:
            messages.add_message(self.request, messages.ERROR, 'You need to login to add rating')
            return False
        elif Rating.objects.filter(user=self.request.user,
                                   book=Book.objects.get(slug=self.kwargs['book_slug'])).exists():
            messages.add_message(self.request, messages.ERROR, 'you can only add one rating per book')
            return False
        return True

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        else:
            if not self.request.user.is_authenticated:
                self.login_url = '/login/'
            else:
                self.login_url = reverse('book_details', kwargs={'slug': self.kwargs['book_slug']})
            return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

    def form_valid(self, form):
        print(form.data)
        form.instance.user = self.request.user
        form.instance.book = Book.objects.get(slug=self.kwargs['book_slug'])

        return super().form_valid(form)

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Rating added successfully')
        return reverse('book_details', kwargs={'slug': self.kwargs['book_slug']})

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)


class UpdateRatingView(UserPassesTestMixin, UpdateView):
    model = Rating
    form_class = RatingForm
    template_name = 'ratings/update_rating.html'

    def test_func(self):
        condition = self.request.user == Rating.objects.get(slug=self.kwargs['slug']).user
        if condition:
            return True
        if not condition:
            messages.add_message(self.request, messages.ERROR, 'You are not authorized to access this page')
        return False

    def get_object(self, queryset=None):
        return Rating.objects.get(user=self.request.user, book__slug=self.kwargs['book_slug'], slug=self.kwargs['slug'])

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Rating updated successfully')
        return reverse('book_details', kwargs={'slug': self.kwargs['book_slug']})

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)


class DeleteRatingView(UserPassesTestMixin, DeleteView):
    model = Rating
    template_name = 'ratings/delete_rating.html'

    def test_func(self):
        condition = self.request.user == Rating.objects.get(slug=self.kwargs['slug']).user
        if condition:
            return True
        if not condition:
            messages.add_message(self.request, messages.ERROR, 'You are not authorized to access this page')
        return False

    def get_object(self, queryset=None):
        return Rating.objects.get(user=self.request.user, book__slug=self.kwargs['book_slug'], slug=self.kwargs['slug'])

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Rating deleted successfully')
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        return reverse('book_details', kwargs={'slug': self.kwargs['book_slug']})


def change_active(request, book_slug, slug):
    rating = Rating.objects.get(slug=slug, book__slug=book_slug)
    print(slug)
    rating.change_active()
    return redirect(reverse('dashboard_rating_list'))
