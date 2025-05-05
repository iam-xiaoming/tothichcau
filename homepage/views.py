from django.shortcuts import render, redirect
from .utils import get_trendings, get_sales


# Create your views here.
def home(request):
    context = {
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
        ]
    }
    return render(request, 'homepage/home.html', context)