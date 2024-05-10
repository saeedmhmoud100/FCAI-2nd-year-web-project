from django.urls import path

from . import views

urlpatterns = [

    path('list/', views.BookListView.as_view(), name='book_list'),
    path('<slug:slug>/', views.BookDetailView.as_view(), name='book_details'),
    path('borrowed', views.BorrowedBookListView.as_view(), name='borrowed_books'),

]