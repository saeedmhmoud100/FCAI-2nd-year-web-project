from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.views.generic import ListView

from books.models import Book
from categories.views import CategoryListView
from ratings.models import Rating

# Create your views here.

User = get_user_model()


class AdminDashboardListViewPermissionMixin(UserPassesTestMixin):
    raise_exception = False
    def test_func(self):
        cond = self.request.user.is_staff
        return cond

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        else:
            if not self.request.user.is_authenticated:
                self.login_url = reverse('login')
            else:
                self.login_url = reverse('profile')
            messages.add_message(self.request, messages.ERROR, 'You are not authorized to view this page.')
            return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())


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
