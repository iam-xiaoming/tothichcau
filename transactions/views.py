from rest_framework.response import Response
from .serializers import TransactionSerializer
from cart.models import Transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_404_NOT_FOUND

# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_detail(request, pk):
    try:
        transaction = Transaction.objects.get(id=pk)
    except Transaction.DoesNotExist:
        return Response({'error': 'Transaction not found'}, status=HTTP_404_NOT_FOUND)
    
    serializer = TransactionSerializer(transaction)
    return Response(serializer.data)
    