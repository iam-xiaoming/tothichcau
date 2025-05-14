from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'), 
    
    path('create-checkout-session/', views.CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
    path("success/", views.success, name="success"),
    path("cancel/", views.cancel, name="cancel"),
    
    path('webhook/stripe/', views.webhook_view, name='webhook_stripe'),

    path('api/cart/count/<str:pk>/', views.get_cart_count, name='cart_count'),
    
    # game and dlc
    path('api/cart/game/add/<str:pk>/<int:game_pk>/', views.add_game_to_cart, name='add_to_cart'),
    path('api/cart/dlc/add/<str:pk>/<int:game_pk>/', views.add_dlc_to_cart, name='add_to_cart'),
    
    path('cart/delete/<int:pk>/', views.CartDeleteView.as_view(), name='cart-delete'),
    path('api/check-stock/', views.check_stock, name='check_stock'),
]