from django.shortcuts import render, get_object_or_404
from games.models import Game, DLC
from django.views.generic import ListView
from game_features.models import Category
from django.http import HttpResponse
from homepage.utils import get_trendings, get_sales, get_mostplay, get_coming_soon, get_free_games
from django.core.paginator import Paginator

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
        context['games'] = list(context['games']) + list(DLC.objects.all())
        return context
        
        
def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)

    games = list(Game.objects.filter(categories=category))
    dlcs = list(DLC.objects.filter(categories=category))

    game_list = games + dlcs
    context = {
        'genres': genres,
        'games': games + dlcs 
    }
    paginator = Paginator(game_list, 21)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj

    return render(request, 'list/games-list.html', context)


def action_view(request, action):
    if action not in ['trending', 'sale', 'most-played', 'upcoming', 'free-games']:
        return HttpResponse('<h1>404</h1>')
    
    context = {
        'genres': genres, 
    }
    
    if action == 'trending':
        context['games'] = get_trendings(status='all')
    elif action == 'sale':
        context['games'] = get_sales(status='all')
    elif action == 'most-played':
        context['games'] = get_mostplay(status='all')
    elif action == 'upcoming':
        context['games'] = get_coming_soon(status='all')
    else:
        context['games'] = get_free_games(status='all')
        
    game_list = context['games']
    paginator = Paginator(game_list, 21)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj
    
    return render(request, 'list/games-list.html', context)