from django.urls import path
from .import views

urlpatterns = [
    path("setup/", views.stream_setup, name="stream_setup"),
    path("api/check_stream/", views.check_stream, name="check_stream"),
    path('livestream/', views.livestream, name='livestream'),
]