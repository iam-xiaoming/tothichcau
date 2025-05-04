from django.urls import path
from . import views

urlpatterns = [
    path('game-list/', views.GameListView.as_view(), name='game-list'),
    path('category-list/<str:slug>/', views.category_view, name='category-list'),
    path('action/list/<str:action>/', views.action_view, name='action-list')
]