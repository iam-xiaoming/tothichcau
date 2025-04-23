from django.urls import path
from search.views import GameSearchAPIView, UserGameSearchAPIView

urlpatterns = [
    path("api/search/games/", GameSearchAPIView.as_view(), name="game-search"),
    path('api/search/user-games/', UserGameSearchAPIView.as_view(), name='user-game-search')
]