from django.shortcuts import render, get_object_or_404, redirect
from .models import Game, Category
from users.models import Comment
from django.views.generic import DetailView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.response import Response
from .serializers import GameSerializer

# Create your views here.
class GameDetailView(DetailView):
    model = Game
    template_name = 'games/game_details.html'
    context_object_name = 'game'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game = self.get_object()
            
        context['categories'] = Category.objects.all()
        context['games_suggest'] = Game.objects.all()[:3]
        return context
    
    def post(self, request, *args, **kwargs):
        user = request.user
        game_id = self.kwargs.get('pk')
        game = get_object_or_404(Game, pk=game_id)
        title = request.POST.get('title')
        content = request.POST.get('content')
        # save comment
        Comment.objects.create(user=user, game=game, title=title, content=content)
        
        return redirect('game_details', pk=game.pk)
        
           
@api_view(['GET'])
def game_media_review(request, pk):
    try:
        game = Game.objects.get(id=pk)
    except Game.DoesNotExist:
        return Response({'error': 'Game not found'}, status=HTTP_404_NOT_FOUND)
    
    serializer = GameSerializer(game)
    return Response(serializer.data)