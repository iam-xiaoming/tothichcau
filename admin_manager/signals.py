from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import GameHero

@receiver(post_delete, sender=GameHero)
def delete_game_hero(sender, instance, **kwargs):
    if instance.image:                   
        instance.image.delete(save=False)
        
        
@receiver(pre_save, sender=GameHero)
def save_game_hero(sender, instance, **kwargs):
    if instance.pk:
        old_instance = GameHero.objects.get(pk=instance.pk)
        
        if old_instance.image != instance.image:
            if old_instance.image:
                old_instance.image.delete(save=False)