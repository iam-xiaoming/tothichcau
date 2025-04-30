from django.shortcuts import render, redirect
from games.models import Game, DLC
from admin_manager.models import GameHero
from django.views.generic import ListView

# Create your views here.
class ListGameView(ListView):
    model = Game
    template_name = 'homepage/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        games_and_dlcs = list(Game.objects.all()) + list(DLC.objects.all())
        
        items = {
            'games': games_and_dlcs,
            'game_heros': GameHero.objects.all()
        }
        
        context['items'] = items
        return context