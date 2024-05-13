from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.CategoryCreateView.as_view(), name='category-create'),
    path('<slug:slug>/update/', views.CategoryUpdateView.as_view(), name='category-update'),
    path('<slug:slug>/delete/', views.CategoryDeleteView.as_view(), name='category-delete'),
]