from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

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
