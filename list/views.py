from django.shortcuts import render
from games.models import Game
from django.views.generic import ListView
from game_features.models import Category

# Create your views here.
class GameListView(ListView):
    model = Game
    template_name = 'list/games-list.html'
    context_object_name = 'games'
    paginate_by = 21    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()[:4]
        return context
        
        