from django.urls import path
from . import views

urlpatterns = [
    path('api/get_game_key_available_count/<int:pk>/', views.get_game_key_available_count, name='get_game_key_available_count'),
    path('api/get_dlc_key_available_count/<int:pk>/', views.get_dlc_key_available_count, name='get_game_dlc_available_count'),
]