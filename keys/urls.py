from django.urls import path
from . import views

urlpatterns = [
    path('api/get_key_available_count/<int:pk>/', views.get_key_available_count, name='get_key_available_count'),
]