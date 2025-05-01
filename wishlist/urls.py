from django.urls import path
from . import views

urlpatterns = [
    path('api/wishlist/count/<str:pk>/', views.get_wishlist_count, name='wishlist-count'),
    path('api/add-to-wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    # path('api/add-game-to-wishlist/<str:user_pk>/<int:game_pk>/', views.add_game_to_wishlist, name='add_game_to_wishlist'),
    # path('api/add-dlc-to-wishlist/<str:user_pk>/<int:game_pk>/', views.add_dlc_to_wishlist, name='add_dlc_to_wishlist')
]