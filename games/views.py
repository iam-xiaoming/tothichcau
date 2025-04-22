from django.shortcuts import render, get_object_or_404, redirect
from .models import Game, Category, Comment
from django.views.generic import DetailView

# Create your views here.
class GameDetailView(DetailView):
    model = Game
    template_name = 'games/game_details.html'
    context_object_name = 'game'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game = self.get_object()
        if game.keys.filter(status='available').exists():
            context['status'] = 'Available'
        else:
            context['status'] = 'Stockout'
            
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
        
        