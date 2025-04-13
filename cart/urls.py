from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart_view, name='cart'), 
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path('create-checkout-session/', views.CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
    path("success/", views.success, name="success"),
    path("cancel/", views.cancel, name="cancel"),
    # path('webhook/stripe/', views.webhook_view, name='webhook_stripe'),
    path('api/cart/count/', views.get_cart_count, name='cart_count'),
    path('api/cart/add/', views.add_to_cart, name='add_to_cart'),
    path('api/cart/game_ids/', views.get_cart_game_ids, name='get_cart_game_ids'),

]