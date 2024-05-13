from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from categories.forms import CategoryForm
from categories.models import Category


# Create your views here.

class CategoryListView(ListView):
    model = Category


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Category'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm


class CategoryDeleteView(DeleteView):
    model = Category

