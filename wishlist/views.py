from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Wishlist
from users.models import MyUser
from rest_framework.response import Response
from games.models import Game, DLC

# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_wishlist_count(request, pk):
    try:
        wishlist_count =  Wishlist.objects.filter(user__pk=pk).count()
    except MyUser.DoesNotExist:
        return Response({'error': 'User not found.'}, status=404)
    
    return Response({'message': 'success', 'wishlist_count': wishlist_count}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_wishlist(request):
    item_type = request.data.get('type')
    item_id = request.data.get('id')
    user = request.user

    if item_type not in ['base', 'dlc']:
        return Response({'error': 'Invalid type.'}, status=400)

    try:
        if item_type == 'base':
            game = Game.objects.get(pk=item_id)
            existed = Wishlist.objects.filter(user=user, game=game).exists()
            if existed:
                return Response({'message': 'Already in wishlist'}, status=200)
            Wishlist.objects.create(user=user, game=game)
        else:
            dlc = DLC.objects.get(pk=item_id)
            existed = Wishlist.objects.filter(user=user, dlc=dlc).exists()
            if existed:
                return Response({'message': 'Already in wishlist'}, status=200)
            Wishlist.objects.create(user=user, dlc=dlc)

        return Response({'success': True, 'message': 'Added to wishlist'}, status=200)

    except (Game.DoesNotExist, DLC.DoesNotExist):
        return Response({'error': 'Item does not exist'}, status=400)
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_from_wishlist(request):
    item_type = request.data.get('type')
    item_pk = request.data.get('item_pk')
    user = request.user

    if not item_type or not item_pk:
        return Response({'error': 'Missing parameters.'}, status=400)

    try:
        if item_type == 'base':
            wishlist_item = Wishlist.objects.get(user=user, pk=item_pk)
        elif item_type == 'dlc':
            wishlist_item = Wishlist.objects.get(user=user, pk=item_pk)
        else:
            return Response({'error': 'Invalid type.'}, status=400)

        wishlist_item.delete()
        return Response({'success': True, 'message': 'Removed from wishlist'}, status=200)

    except Wishlist.DoesNotExist:
        return Response({'error': 'Wishlist item not found.'}, status=404)