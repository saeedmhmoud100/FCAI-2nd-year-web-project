from django.urls import path

from . import views

urlpatterns = [
    path('books', views.AdminBookListView.as_view(), name='dashboard_book_list'),
    path('categories', views.AdminCategoryListView.as_view(), name='dashboard_category_list'),
    path('ratings', views.AdminRatingListView.as_view(), name='dashboard_rating_list'),
    path('users', views.AdminUserListView.as_view(), name='dashboard_user_list'),
]