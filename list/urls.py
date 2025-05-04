from django.urls import path
from . import views

urlpatterns = [
    path('game-list/', views.GameListView.as_view(), name='game-list')
]