from django.urls import path
from . import views

urlpatterns = [
    path('transaction-detail/<int:pk>/', views.transaction_details, name='transaction-detail'),
    path('transactions-history/', views.TransactionsHistoryListView.as_view(), name='transaction_history')
]