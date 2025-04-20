import os
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import Game, Key


@receiver(post_delete, sender=Game)
def delete_game_image(sender, instance, **kwargs):
    if instance.image and os.path.isfile(instance.image.path):
        print('Signal: deleting image:', instance.image.path)
        os.remove(instance.image.path)
        

@receiver(post_save, sender=Key)
def update_game_quantity_on_add(sender, instance, created, **kwargs):
    if created:
        game = instance.game
        game.quantity = game.keys.filter(status='available').count()
        game.save()
        

@receiver(post_delete, sender=Key)
def update_game_quantity_on_delete(sender, instance, **kwargs):
    game = instance.game
    game.quantity = game.keys.filter(status='available').count()
    game.save()