from django.urls import path
from . import views

urlpatterns = [
    path('game-details/<int:pk>/', views.GameDetailView.as_view(), name='base-game-details'),
    path('game-details/dlc/<int:pk>/', views.DLCDetailView.as_view(), name='dlc-game-details'),
    
    path('api/game/<int:pk>/media/review/', views.game_media_review, name='game-media-review'),
    path('api/game/dlc/<int:pk>/media/review/', views.dlc_media_review, name='dlc-media-review'),
]