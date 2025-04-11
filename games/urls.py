from django.urls import path
from . import views

urlpatterns = [
    path('game-details/', views.game_details, name='game_details')
]