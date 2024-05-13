from django.urls import path

from . import views

urlpatterns = [

    path('profile', views.UserProfileView.as_view(), name='profile'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('add_user', views.CreateUserView.as_view(), name='add_user'),
    path('change_active_status/<int:user_id>/', views.change_active_status, name='change_active_status'),
    path('change_user_rule/<int:user_id>/', views.change_user_rule, name='change_user_rule'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),

]