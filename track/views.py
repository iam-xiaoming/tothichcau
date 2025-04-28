from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import UserInteraction
from rest_framework.permissions import IsAuthenticated

# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_interaction_api(request):
    user_id = request.data.get('user_id')
    items = request.data.get('items', [])
    
    for item in items:
        UserInteraction.objects.create(
            user_id=user_id,
            item_id=item['item_id'],
            timestamp=item['timestamp'],
            event_type=item['event_type']
        )
    
    return Response({
        "success": True,
        "message": "Interaction recorded successfully"
    }, status=200)
    