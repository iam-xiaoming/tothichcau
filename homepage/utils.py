from games.models import Game, DLC
from django.utils.timezone import now
from datetime import timedelta

def get_trendings(status='limit'):
    games = list(Game.objects.all().order_by('-release_date', '-average_score'))
    dlcs = list(DLC.objects.all().order_by('-release_date', '-average_score'))
    
    combined = games + dlcs
    if status == 'all':
        return combined
    
    return combined[:21]


def get_sales(status='limit'):
    games = list(Game.objects.filter(discount__gt=0).all())
    dlcs = list(DLC.objects.filter(discount__gt=0).all())
    
    combined = games + dlcs
    if status == 'all':
        return combined
    
    return combined[:21]


def get_mostplay(status='limit'):
    games = list(Game.objects.all().order_by('-number_of_buy'))
    dlcs = list(DLC.objects.all().order_by('-number_of_buy'))
    
    combined = games + dlcs
    if status == 'all':
        return combined
    
    return combined[:4]


def get_coming_soon(status='limit'):
    games = list(Game.objects.filter(release_date__gt=now()))
    dlcs = list(DLC.objects.filter(release_date__gt=now()))
    
    combined = games + dlcs
    if status == 'all':
        return combined
    
    return combined[:4]


def get_free_games(status='limit'):
    games = list(Game.objects.filter(discount=100).all())
    dlcs = list(DLC.objects.filter(discount=100).all())
    
    combined = games + dlcs
    if status == 'all':
        return combined
    
    return combined[:4]


def get_new_release(status='limit'):
    thirty_days_ago = now() - timedelta(days=30)
    
    games = list(Game.objects.filter(release_date__gt=thirty_days_ago).order_by('-release_date'))
    dlcs = list(DLC.objects.filter(release_date__gt=thirty_days_ago).order_by('-release_date'))
    
    combined = sorted(games + dlcs, key=lambda x: x.release_date, reverse=True)
    if status == 'all':
        return combined
    
    return combined[:21]