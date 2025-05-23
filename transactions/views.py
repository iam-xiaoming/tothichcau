from cart.models import Transaction
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

# Create your views here.
@login_required
def transaction_details(request, pk):
    transaction = get_object_or_404(Transaction, user=request.user, pk=pk)
    return render(request, 'transactions/transaction_details.html', {'transaction': transaction})