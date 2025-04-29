from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Key
from games.models import Game, DLC

# Create your views here.
@api_view(['GET'])
def get_game_key_available_count(request, pk):
    try:
        game = Game.objects.get(pk=pk)
    except Game.DoesNotExist:
        return Response({'success': False, 'message': 'Game not found.'}, status=404)
    
    key_available_count = Key.objects.filter(game=game, status='available').count()
    return Response({
        'success': True,
        'key_available_count': key_available_count
    }, status=200)
    
    
@api_view(['GET'])
def get_dlc_key_available_count(request, pk):
    try:
        dlc = DLC.objects.get(pk=pk)
    except DLC.DoesNotExist:
        return Response({'success': False, 'message': 'Game not found.'}, status=404)
    
    key_available_count = Key.objects.filter(dlc=dlc, status='available').count()
    return Response({
        'success': True,
        'key_available_count': key_available_count
    }, status=200)    