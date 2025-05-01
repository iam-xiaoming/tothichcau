from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.PostListView.as_view(), name='posts'),
    path('post-detail/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('create-post/', views.create_blog, name='create-post')
]