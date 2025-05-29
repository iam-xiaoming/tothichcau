from cart.models import Transaction
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
import numpy as np
from users.models import MyUser
from django.http import JsonResponse

# Create your views here.
@login_required
def transaction_details(request, pk):
    transaction = get_object_or_404(Transaction, user=request.user, pk=pk)
    return render(request, 'transactions/transaction_details.html', {'transaction': transaction})

class TransactionsHistoryListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transactions/transactions-history.html'
    context_object_name = 'transactions'
    paginate_by = 20
    
    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        transactions = self.get_queryset()
        number_of_transaction = len(transactions)
        total_amount = np.sum([transaction.total_amount for transaction in transactions])
        
        context['number_of_transactions'] = number_of_transaction
        context['total_amount'] = total_amount
        
        return context