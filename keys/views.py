from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Key
from games.models import Game

# Create your views here.
@api_view(['GET'])
def get_key_available_count(request, pk):
    try:
        game = Game.objects.get(pk=pk)
    except Game.DoesNotExist:
        return Response({'success': False, 'message': 'Game not found.'}, status=404)
    
    key_available_count = Key.objects.filter(game=game, status='available').count()
    return Response({
        'success': True,
        'key_available_count': key_available_count
    }, status=200)    