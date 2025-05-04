from django.shortcuts import render, get_object_or_404
from games.models import Game, DLC
from django.views.generic import ListView
from game_features.models import Category
from django.http import HttpResponse
from homepage.utils import get_trendings, get_sales

# Create your views here.
genres = Category.objects.all()[:4]

class GameListView(ListView):
    model = Game
    template_name = 'list/games-list.html'
    context_object_name = 'games'
    paginate_by = 21    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = genres
        return context
        
        
def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)

    games = list(Game.objects.filter(categories=category))
    dlcs = list(DLC.objects.filter(categories=category))

    context = {
        'genres': genres,
        'games': games + dlcs 
    }

    return render(request, 'list/games-list.html', context)


def action_view(request, action):
    if action not in ['trending', 'sale']:
        return HttpResponse('<h1>404</h1>')
    
    context = {
        'genres': genres, 
    }
    
    if action == 'trending':
        context['games'] = get_trendings()
    elif action == 'sale':
        context['games'] = get_sales()  
    
    return render(request, 'list/games-list.html', context)