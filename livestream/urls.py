from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_stream, name='create_stream'),
    path('stream/<int:stream_id>/', views.stream_detail, name='stream_detail'),
    path('api/stream/<slug:stream_id>/status/', views.stream_status, name='stream-status'),
]