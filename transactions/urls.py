from django.urls import path
from . import views

urlpatterns = [
    path('api/transaction-detail/<int:pk>', views.transaction_detail, name='transaction-detail'),
]