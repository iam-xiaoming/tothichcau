from django.urls import path
from . import views

urlpatterns = [
    path('musics/', views.embed_spotify, name='embed_spotify'),
    path('spotify/home/', views.spotify_home, name='spotify_home'),
    path('spotify/login/', views.spotify_login, name='spotify-login'),
    path('callback/', views.spotify_callback, name='spotify-callback'),
    path('refresh/', views.spotify_refresh, name='spotify-refresh'),
    path('spotify/search/', views.spotify_search, name='spotify_search'),
]
