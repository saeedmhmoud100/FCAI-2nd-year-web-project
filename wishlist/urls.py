from django.urls import path

from . import views

urlpatterns = [

    path('toggle-book-in-wishlist/<int:book_id>', views.toggle_book_in_wishlist, name='toggle_book_in_wishlist'),
    path('toggle-book-in-wishlist-api/<int:book_id>/<int:user_id>', views.toggle_book_in_wishlist_api, name='toggle_book_in_wishlist_api'),

]