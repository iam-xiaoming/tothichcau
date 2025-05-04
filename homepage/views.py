from django.shortcuts import render, redirect
from games.models import Game, DLC
from .utils import get_trendings, get_sales


# Create your views here.
def home(request):
    context = {
        'trendings': get_trendings(),
        'sales': get_sales()
    }
    return render(request, 'homepage/home.html', context)