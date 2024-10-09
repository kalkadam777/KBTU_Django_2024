from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/<str:username>/follow', views.follow_user, name='follow_user'),
    path('profile/<str:username>/unfollow', views.unfollow_user, name='unfollow_user'),
]
