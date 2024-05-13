from django.urls import path

from . import views

urlpatterns = [

    path('list/', views.BookListView.as_view(), name='book_list'),
    path('borrowed/', views.BorrowedBookListView.as_view(), name='borrowed_books'),
    path('add/', views.BookCreateView.as_view(), name='add_book'),
    path('<slug:slug>/', views.BookDetailView.as_view(), name='book_details'),
    path('update/<slug:slug>/', views.BookUpdateView.as_view(), name='update_book'),
    path('delete/<slug:slug>/', views.delete_book, name='delete_book'),
    path('borrow/<slug:slug>/', views.BorrowBookView.as_view(), name='borrow_book'),
    path('return/<slug:slug>/', views.ReturnBookView.as_view(), name='return_book'),

]