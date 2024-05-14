from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from categories.forms import CategoryForm
from categories.models import Category


# Create your views here.

class CategoryListView(ListView):
    model = Category


class CategoryCreateView(UserPassesTestMixin, CreateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('dashboard_category_list')

    def test_func(self):
        condition = self.request.user.is_superuser
        if not condition:
            messages.add_message(self.request, messages.ERROR, 'You are not authorized to access this page')
        return condition
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Category'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CategoryUpdateView(UserPassesTestMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('dashboard_category_list')

    def test_func(self):
        condition = self.request.user.is_superuser
        if not condition:
            messages.add_message(self.request, messages.ERROR, 'You are not authorized to access this page')
        return condition

class CategoryDeleteView(UserPassesTestMixin,DeleteView):
    model = Category
    success_url = reverse_lazy('dashboard_category_list')

    def test_func(self):
        condition = self.request.user.is_superuser
        if not condition:
            messages.add_message(self.request, messages.ERROR, 'You are not authorized to access this page')
        return condition
