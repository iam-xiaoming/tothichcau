from django.urls import path
from . import views

urlpatterns = [
    path('api/notifications/', views.notification_list, name='notification-list'),
    path('api/notifications/mark-read/', views.mark_as_read, name='mark-as-read')
]