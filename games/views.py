from django.shortcuts import render
from .models import Game
from django.views.generic import DetailView

# Create your views here.
class GameDetailView(DetailView):
    model = Game
    template_name = 'games/game_details.html'
    context_object_name = 'game'