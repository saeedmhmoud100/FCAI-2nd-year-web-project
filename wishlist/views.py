from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect

from books.models import Book
from project.permissions import check_authenticated, check_user
from wishlist.models import UserWishList


# Create your views here.

@check_authenticated(check_user)
def toggle_book_in_wishlist(request, book_id):
    user = request.user
    book = Book.objects.get(id=book_id)
    item, created = user.wishlist.get_or_create(book=book, user=user)
    if not created:
        messages.add_message(request, messages.INFO, 'This book is deleted from your wishlist.')
        item.delete()
    else:
        messages.add_message(request, messages.INFO, 'This book is added to your wishlist.')
        if (request.GET.get('HTTP_REFERER')):
            return redirect(request.META.get('HTTP_REFERER'))
    return redirect('book_details', slug=Book.objects.get(id=book_id).slug)


def toggle_book_in_wishlist_api(request, book_id,user_id):
    user = request.user
    book = Book.objects.get(id=book_id)
    item, created = user.wishlist.get_or_create(book=book, user=user)
    if not created:
        item.delete()
    return JsonResponse({'status': 200})
