from games.models import Game, DLC
from django.utils.timezone import now

def get_trendings(status='get'):
    games = list(Game.objects.all().order_by('-release_date', '-average_score'))
    dlcs = list(DLC.objects.all().order_by('-release_date', '-average_score'))
    
    combined = games + dlcs
    if status == 'all':
        return combined
    
    return combined[:21]


def get_sales(status='get'):
    games = list(Game.objects.filter(discount__gt=0).all())
    dlcs = list(DLC.objects.filter(discount__gt=0).all())
    
    combined = games + dlcs
    if status == 'all':
        return combined
    
    return combined[:21]


def get_mostplay(status='get'):
    games = list(Game.objects.all().order_by('-number_of_buy'))
    dlcs = list(DLC.objects.all().order_by('-number_of_buy'))
    
    combined = games + dlcs
    if status == 'all':
        return combined
    
    return combined[:4]


def get_coming_soon(status='get'):
    games = list(Game.objects.filter(release_date__gt=now()))
    dlcs = list(DLC.objects.filter(release_date__gt=now()))
    
    combined = games + dlcs
    if status == 'all':
        return combined
    
    return combined[:4]


def get_free_games(status='get'):
    games = list(Game.objects.filter(discount=100).all())
    dlcs = list(DLC.objects.filter(discount=100).all())
    
    combined = games + dlcs
    if status == 'all':
        return combined
    
    return combined[:4]