from django.urls import path
from search.views import GameSearchAPIView

urlpatterns = [
    path("api/search/games/", GameSearchAPIView.as_view(), name="game-search"),
]