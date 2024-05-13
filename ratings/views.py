from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView

from books.models import Book
from ratings.forms import RatingForm
from ratings.models import Rating


# Create your views here.

class CreateRatingView(CreateView):
    model = Rating
    form_class = RatingForm
    template_name = 'ratings/add_rating.html'

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

class UpdateRatingView(UpdateView):
    model = Rating
    form_class = RatingForm
    template_name = 'ratings/update_rating.html'

    def get_object(self, queryset=None):
        return Rating.objects.get(user=self.request.user, book__slug=self.kwargs['book_slug'],slug=self.kwargs['slug'])

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Rating updated successfully')
        return reverse('book_details', kwargs={'slug': self.kwargs['book_slug']})

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)

class DeleteRatingView(DeleteView):
    model = Rating
    template_name = 'ratings/delete_rating.html'

    def get_object(self, queryset=None):
        return Rating.objects.get(user=self.request.user, book__slug=self.kwargs['book_slug'],slug=self.kwargs['slug'])
    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Rating deleted successfully')
        return reverse('book_details', kwargs={'slug': self.kwargs['book_slug']})