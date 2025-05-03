from django.shortcuts import render, redirect
from games.models import Game, DLC


# Create your views here.
def home(request):
    context = {
        'recommended': Game.objects.all()[:10],
        'most_view': DLC.objects.all()[:10]
    }
    return render(request, 'homepage/home.html', context)