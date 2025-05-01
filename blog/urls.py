from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.PostListView.as_view(), name='posts'),
    path('post-detail/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('create-post/', views.PostCreateView.as_view(), name='create-post'),
    path('posts/<str:pk>/', views.UserPostListView.as_view(), name='user-post-list')
]