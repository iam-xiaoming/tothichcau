from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from keys.models import Key
from games.models import Game, DLC

# update key and then update game

def update_key_quantity(instance):
    if instance.game_id:
        try:
            Game.objects.filter(pk=instance.game_id).update(
            quantity=Key.objects.filter(game_id=instance.game_id, status='available').count()
        )
        except Game.DoesNotExist as e:
            raise ValueError(str(e))
    else:
        try:
            DLC.objects.filter(pk=instance.dlc_id).update(
            quantity=Key.objects.filter(dlc_id=instance.dlc_id, status='available').count()
        )
        except DLC.DoesNotExist as e:
            raise ValueError(str(e))
        

@receiver(post_save, sender=Key)
def update_game_quantity_on_add(sender, instance, created, **kwargs):
    update_key_quantity(instance)
        

@receiver(post_delete, sender=Key)
def update_game_quantity_on_delete(sender, instance, **kwargs):
    update_key_quantity(instance)