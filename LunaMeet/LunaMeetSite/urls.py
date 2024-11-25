from django.urls import path
from . import views

urlpatterns = [
    path('sign-up', views.show_sign_up),
    path('sign-in', views.show_sign_in),
    path('user-sign-up', views.register),
    path('user-sign-in', views.login),
    path('confirm_email/<uidb64>/<token>/', views.confirm_email, name='confirm_email'),
    path('', views.main_page)
]