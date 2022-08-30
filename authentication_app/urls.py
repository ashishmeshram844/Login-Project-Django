"""Urls for authentication_app"""
from django.urls import path
from authentication_app.views import LoginView, LogoutView,dashboard,RegisterView


urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('dashboard', dashboard, name='dashboard'),
    path('register', RegisterView.as_view(), name='register'),
]
