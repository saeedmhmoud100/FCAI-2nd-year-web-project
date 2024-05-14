from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView

from books.models import Book
from books.views import BookListView
from categories.views import CategoryListView
from ratings.models import Rating


# Create your views here.

User = get_user_model()

class AdminDashboardListViewPermissionMixin(UserPassesTestMixin):
    def test_func(self):
        cond = self.request.user.is_staff
        if not cond:
            messages.add_message(self.request, messages.ERROR, 'You are not authorized to view this page.')
        return cond


class AdminBookListView(AdminDashboardListViewPermissionMixin, ListView):
    model = Book
    template_name = 'dashboard/book_list.html'

    def get_queryset(self):
        return Book.objects.all().order_by('id')


class AdminCategoryListView(AdminDashboardListViewPermissionMixin, CategoryListView):
    template_name = 'dashboard/categories_list.html'

class AdminRatingListView(AdminDashboardListViewPermissionMixin, ListView):
    model = Rating
    template_name = 'dashboard/ratings_list.html'

    def get_queryset(self):
        return Rating.objects.all().order_by('id')


class AdminUserListView(AdminDashboardListViewPermissionMixin, ListView):
    model = User
    template_name = 'dashboard/users_list.html'

    def get_queryset(self):
        return User.objects.all().order_by('id')