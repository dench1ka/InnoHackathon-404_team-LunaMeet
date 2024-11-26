from django.urls import path
from . import views

urlpatterns = [
    path('profile', views.show_profile),
    path('sign-up', views.show_sign_up),
    path('sign-in', views.show_sign_in, name='login'),
    path('user-sign-up', views.register),
    path('user-sign-in', views.login),
    path('eventpage', views.show_eventpage),
    path('confirm_email/<uidb64>/<token>/', views.confirm_email, name='confirm_email'),
    path('add-event', views.show_add_event),
    path('', views.main_page)
]