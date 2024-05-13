from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.CategoryCreateView.as_view(), name='add_category'),
    path('<slug:slug>/update/', views.CategoryUpdateView.as_view(), name='update_category'),
    path('<slug:slug>/delete/', views.CategoryDeleteView.as_view(), name='delete_category'),
]