from django.shortcuts import render
from .models import Game, Key, Category
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