from django.shortcuts import render, redirect
from recommender.utils import get_aws_recommended_items, aws_validators_recommendation
from django.conf import settings
from games.models import Game, DLC


# Create your views here.
def home(request):
    
    context = dict()
    
    if request.user.is_authenticated:
        items = get_aws_recommended_items(settings.RECOMMENDER, request.user.id, 20,                                  settings.FILTERING)
        if items:
            recommended = aws_validators_recommendation(list(map(lambda x: int(x['itemId']), items)))
              
        items = get_aws_recommended_items(settings.RECOMMENDER_MOST_VIEW, request.user.id, 20)
        if items:
            most_view = aws_validators_recommendation(
                items = list(map(lambda x: int(x['itemId']), items))
            )
            
        if recommended and most_view:
            n, m = len(recommended), len(most_view)
        
            if n < 20:
                recommended += list(Game.objects.all()[:20 - n // 2])
                recommended += list(DLC.objects.all()[:20 - n // 2])
                
            if m < 20:
                most_view += list(Game.objects.all()[:20 - m // 2])
                most_view += list(DLC.objects.all()[: 20 - m // 2])
            
            context = {
                'recommended': recommended,
                'most_view': most_view
            }
            return render(request, 'homepage/home.html', context)
            
        else:
            items = list(Game.objects.all()[:10]) + list(DLC.objects.all()[:10])
        
            context = {
                'recommended': items,
                'most_view': items
            }
            return render(request, 'homepage/home.html', context)
        
    else:
        items = list(Game.objects.all()[:10]) + list(DLC.objects.all()[:10])
        context = {
            'recommended': items,
            'most_view': items
        }
    
    return render(request, 'homepage/home.html', context)