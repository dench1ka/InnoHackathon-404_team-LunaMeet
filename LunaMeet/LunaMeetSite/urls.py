from django.urls import path
from . import views

urlpatterns = [
    path('sign-up', views.show_sign_up),
    path('user-sign-up'),
]