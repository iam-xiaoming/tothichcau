from django.shortcuts import render, redirect
from .utils import get_trendings, get_sales, get_mostplay, get_coming_soon
from game_features.models import FeatureHighlight, GameStory
from admin_manager.models import GameHero


# Create your views here.
def home(request):
    sales = get_sales()
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
                'games': sales,
                'id': 'sale'
            }
        ],
        'top_sellers': sorted(sales, key=lambda x: -x.discount),
        'most_played': get_mostplay(),
        'upcoming_games': get_coming_soon(),
        'highlights': FeatureHighlight.objects.all(),
        'stories': GameStory.objects.all()
    }
    return render(request, 'homepage/home.html', context)