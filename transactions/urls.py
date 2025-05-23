from django.urls import path
from . import views

urlpatterns = [
    path('transaction-detail/<int:pk>/', views.transaction_details, name='transaction-detail'),
]