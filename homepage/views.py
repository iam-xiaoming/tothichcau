from django.shortcuts import render, redirect
from games.models import Game
from django.views.generic import ListView

# Create your views here.
# def home(request):
#     return render(request, 'homepage/home.html')

class ListGameView(ListView):
    model = Game
    template_name = 'homepage/home.html'
    context_object_name = 'games'
    
    

