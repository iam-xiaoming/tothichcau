from django.shortcuts import render
from games.models import Game

# Create your views here.
def game_list(request):
    games = list(Game.objects.all()) * 11
    context = {
        'games': games
    }
    return render(request, 'list/games-list.html', context)