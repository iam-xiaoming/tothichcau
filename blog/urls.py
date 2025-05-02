from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.PostListView.as_view(), name='posts'),
    path('post-detail/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('create-post/', views.PostCreateView.as_view(), name='create-post'),
    path('posts/<str:pk>/', views.UserPostListView.as_view(), name='user-post-list'),
    path('posts/category/<slug:slug>/', views.CategoryPostListView.as_view(), name='category-post-list'),
    path('posts/tag/<slug:slug>/', views.TagPostListView.as_view(), name='tag-post-list'),
    path('post/reaction/', views.post_reaction, name='post-reaction'),
    path('post/comment/reaction/', views.post_comment_reaction, name='post-comment-reaction')
]