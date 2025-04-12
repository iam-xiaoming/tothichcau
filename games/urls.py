from django.urls import path
from . import views

urlpatterns = [
    path('game-details/<str:pk>/', views.GameDetailView.as_view(), name='game_details')
]