import os
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from .models import Game
from keys.models import Key


@receiver(post_delete, sender=Game)
def delete_game(sender, instance, **kwargs):
    if instance:
        instance.image.delete(save=False)
        

@receiver(pre_save, sender=Game)
def save_game(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Game.objects.get(pk=instance.pk)
        
        if old_instance.image != instance.image:
            if old_instance.image:
                old_instance.image.delete(save=False)


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