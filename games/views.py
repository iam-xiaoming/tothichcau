from django.shortcuts import render, get_object_or_404, redirect
from .models import Game
from django.views.generic import DetailView
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.response import Response
from .serializers import GameSerializer
from users.forms import UserCommentForm
from django.contrib import messages
from games.forms import UserRating

# Create your views here.
class GameDetailView(DetailView):
    model = Game
    template_name = 'games/game_details.html'
    context_object_name = 'game'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        game = self.get_object()
        user = self.request.user
        
        comment_form = UserCommentForm(user=user, game=game)
        comment = comment_form.save(commit=False)
        scoring_form = UserRating(user=user, game=game, comment=comment)
        
        context['comment_form'] = comment_form
        context['scoring_form'] = scoring_form
        context['games_suggest'] = Game.objects.all()[:3]
        return context
    
    def post(self, request, *args, **kwargs):
        game_id = self.kwargs.get('pk')
        user = request.user
        game = get_object_or_404(Game, pk=game_id)
        
        comment_form = UserCommentForm(request.POST, user=user, game=game)
        
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            
            scoring_form = UserRating(request.POST, user=user, game=game, comment=comment)
            comment_form.save()
            
            if scoring_form.is_valid():
                scoring_form.save()
                
                return redirect('game_details', pk=game.pk)
        
        context = self.get_context_data()
        context['comment_form'] = comment_form
        context['scoring_form'] = scoring_form
        messages.error(request, "There was an error with your comment.")
        return self.render_to_response(context)
        
           
@api_view(['GET'])
def game_media_review(request, pk):
    try:
        game = Game.objects.get(id=pk)
    except Game.DoesNotExist:
        return Response({'error': 'Game not found'}, status=HTTP_404_NOT_FOUND)
    
    serializer = GameSerializer(game)
    return Response(serializer.data)