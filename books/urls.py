from django.urls import path

from . import views

urlpatterns = [

    path('books/list', views.BookListView.as_view(), name='book_list'),
    path('books/<slug:slug>', views.BookDetailView.as_view(), name='book_details'),

]