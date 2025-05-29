from django.urls import path
from search.views import GameSearchAPIView, UserGameSearchAPIView, TransactionHistorySearchAPIView

urlpatterns = [
    path("api/search/games/", GameSearchAPIView.as_view(), name="game-search"),
    path('api/search/user-games/', UserGameSearchAPIView.as_view(), name='user-game-search'),
    path('api/search/transactions-history/', TransactionHistorySearchAPIView.as_view(), name='transactions-history-search')
]