from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart_view, name='cart'), 
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path('create-checkout-session/', views.CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
    path("success/", views.success, name="success"),
    path("cancel/", views.cancel, name="cancel"),
    # path('webhook/stripe/', views.webhook_view, name='webhook_stripe'),
]