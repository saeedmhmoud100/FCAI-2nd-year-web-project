from django.urls import path

from . import views

urlpatterns = [
    path('add', views.CreateRatingView.as_view(), name='add_rating'),
    path('update/<slug:slug>', views.UpdateRatingView.as_view(), name='update_rating'),
    path('delete/<slug:slug>', views.DeleteRatingView.as_view(), name='delete_rating'),
    path('chang_active/<slug:slug>', views.change_active, name='rating_change_active')
]