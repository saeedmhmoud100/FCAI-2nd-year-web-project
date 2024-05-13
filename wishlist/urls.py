from django.urls import path

from . import views

urlpatterns = [

    path('toggle-book-in-wishlist/<int:book_id>', views.toggle_book_in_wishlist, name='toggle_book_in_wishlist'),

]