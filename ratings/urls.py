from django.urls import path

from . import views

urlpatterns = [
    path('add/', views.CreateRatingView.as_view(), name='add_rating'),
    path('update/<slug:slug>/', views.UpdateRatingView.as_view(), name='update_rating'),
]