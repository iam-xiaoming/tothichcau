from django.shortcuts import render, redirect
from games.models import Game
from game_features.models import Category
from admin_manager.models import GameHero
from django.views.generic import ListView

# Create your views here.
class ListGameView(ListView):
    model = Game
    template_name = 'homepage/home.html'
    context_object_name = 'games'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gameheros'] = GameHero.objects.all()
        context['categories'] = Category.objects.all()
        return context