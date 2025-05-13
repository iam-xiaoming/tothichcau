from django.shortcuts import render, redirect
from .utils import get_trendings, get_sales
from game_features.models import FeatureHighlight, GameStory
from admin_manager.models import GameHero


# Create your views here.
def home(request):
    context = {
        'game_heros': GameHero.objects.all(),
        'sections': [
            {
                'name': 'trending__product',
                'display_name': 'Trending',
                'games': get_trendings(),
                'id': 'trending'
            },
            {
                'name': 'sale__product',
                'display_name': 'Sale',
                'games': get_sales(),
                'id': 'sale'
            }
        ],
        'top_sellers': get_sales(),
        'most_played': get_sales(),
        'upcoming_games': get_sales(),
        'highlights': FeatureHighlight.objects.all(),
        'stories': GameStory.objects.all()
    }
    return render(request, 'homepage/home.html', context)