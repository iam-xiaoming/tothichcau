from django.urls import path
from . import views

urlpatterns = [
    path('api/wishlist/count/<str:pk>/', views.get_wishlist_count, name='wishlist-count'),
    path('api/add-to-wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('api/remove-from-wishlist/', views.remove_from_wishlist, name='remove_from_wishlist'),
]