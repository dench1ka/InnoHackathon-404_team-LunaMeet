from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('sign-up', views.show_sign_up),
    path('sign-in', views.show_sign_in, name='login'),
    path('user-sign-up', views.register),
    path('user-sign-in', views.login),
    path('eventpage/<int:event_id>', views.show_eventpage, name='eventpage'),
    path('confirm_email/<uidb64>/<token>/', views.confirm_email, name='confirm_email'),
    path('add-event', views.show_add_event),
    path('api-add-event', views.add_event),
    path('api-user-by-username', views.get_user_by_username),
    path('users/<str:token>', views.user),
    path('search', views.search),
    path('eventpage/user-details-by-token', views.get_user_details_by_token),
    path('eventpage/add-comment', views.add_comment),
    path('eventpage/mark-event', views.mark_event),
    path('', views.main_page)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)