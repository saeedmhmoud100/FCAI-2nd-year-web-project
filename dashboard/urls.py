from django.urls import path

from . import views

urlpatterns = [
    path('books', views.AdminBookListView.as_view(), name='dashboard_book_list'),
    path('categories', views.AdminCategoryListView.as_view(), name='dashboard_category_list'),
]