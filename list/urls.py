from django.urls import path
from . import views

urlpatterns = [
    path('game-list/', views.game_list, name='game-list')
]