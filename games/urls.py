from django.urls import path
from . import views

urlpatterns = [
    path('game-details/<int:pk>/', views.GameDetailView.as_view(), name='game_details'),
    path('api/game/<int:pk>/media/review/', views.game_media_review, name='game-media-review')
]