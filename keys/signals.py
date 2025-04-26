from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from keys.models import Key

# update key and then update game
@receiver(post_save, sender=Key)
def update_game_quantity_on_add(sender, instance, created, **kwargs):
    game = instance.game
    game.quantity = game.keys.filter(status='available').count()
    game.save()
        

@receiver(post_delete, sender=Key)
def update_game_quantity_on_delete(sender, instance, **kwargs):
    game = instance.game
    game.quantity = game.keys.filter(status='available').count()
    game.save()