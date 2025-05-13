from games.models import Game, DLC
from django.utils.timezone import now

def get_trendings(n=21):
    games = list(Game.objects.all().order_by('-release_date', '-average_score'))
    dlcs = list(DLC.objects.all().order_by('-release_date', '-average_score'))
    
    combined = games + dlcs
    
    return combined[:n]


def get_sales(n=21):
    games = list(Game.objects.filter(discount__gt=0).all())
    dlcs = list(DLC.objects.filter(discount__gt=0).all())
    
    combined = games + dlcs
    
    return combined[:n]


def get_mostplay():
    games = list(Game.objects.all().order_by('-number_of_buy'))
    dlcs = list(DLC.objects.all().order_by('-number_of_buy'))
    
    combined = games + dlcs
    if len(combined) > 4:
        return combined[:4]
    return combined


def get_coming_soon():
    games = list(Game.objects.filter(release_date__gt=now()))
    dlcs = list(DLC.objects.filter(release_date__gt=now()))
    
    combined = games + dlcs
    if len(combined) > 4:
        return combined[:4]
    return combined