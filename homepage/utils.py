from games.models import Game, DLC

def get_trendings(n=20):
    games = list(Game.objects.all().order_by('-release_date', '-average_score'))
    dlcs = list(DLC.objects.all().order_by('-release_date', '-average_score'))
    
    combined = games + dlcs
    
    return combined[:n]


def get_sales(n=20):
    games = list(Game.objects.filter(discount__gt=0).all())
    dlcs = list(DLC.objects.filter(discount__gt=0).all())
    
    combined = games + dlcs
    
    return combined[:n]