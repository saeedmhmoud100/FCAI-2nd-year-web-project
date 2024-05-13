from django.contrib import messages
from django.shortcuts import render, redirect

from books.models import Book


# Create your views here.

def toggle_book_in_wishlist(request,book_id):
    user = request.user
    book = Book.objects.get(id=book_id)
    item , created = user.wishlist.get_or_create(book=book,user=user)
    if not created:
        messages.add_message(request, messages.INFO, 'This book is deleted from your wishlist.')
        item.delete()
    else:
        messages.add_message(request, messages.INFO, 'This book is added to your wishlist.')
    return redirect(request.META.get('HTTP_REFERER'))
