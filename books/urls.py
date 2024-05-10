from django.urls import path

from . import views

urlpatterns = [

    path('book_list/', views.BookListView.as_view(), name='book_list'),

]