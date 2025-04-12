from django.shortcuts import render, redirect
from games.models import Game
from django.views.generic import ListView

# Create your views here.
class ListGameView(ListView):
    model = Game
    template_name = 'homepage/home.html'
    context_object_name = 'games'
    
    

