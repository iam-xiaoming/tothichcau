from django.db.models.signals import post_delete, post_save, pre_save, pre_delete
from django.dispatch import receiver
from .models import Game, Rating, DLC
from .utils import stripe_create, instance_scoring

# Game
@receiver(post_delete, sender=Game)
def post_delete_game(sender, instance, **kwargs):
    if instance:
        instance.image.delete(save=False)    

@receiver(pre_save, sender=Game)
def pre_save_game(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Game.objects.get(pk=instance.pk)
        
        if old_instance.image != instance.image:
            if old_instance.image:
                old_instance.image.delete(save=False)           
                
@receiver(post_save, sender=Game)
def post_save_game(sender, instance, created, **kwargs):
    stripe_create(created=created, instance=instance)
    

# DLC 
@receiver(post_delete, sender=DLC)
def delete_dlc(sender, instance, **kwargs):
    if instance:
        instance.image.delete(save=False)    

@receiver(pre_save, sender=DLC)
def pre_save_dlc(sender, instance, **kwargs):
    if instance.pk:
        old_instance = DLC.objects.get(pk=instance.pk)
        
        if old_instance.image != instance.image:
            if old_instance.image:
                old_instance.image.delete(save=False)           
                
@receiver(post_save, sender=DLC)
def post_save_dlc(sender, instance, created, **kwargs):
    stripe_create(created=created, instance=instance)


# rating
@receiver(post_save, sender=Rating)
def scoring(sender, instance, created, **kwargs):
    if created:
        score = instance.score
        weighted = instance.weighted
        if instance.game:
            game_instance = instance_scoring(instance.game, score, weighted)
            game_instance.save()
        else:
            dlc_instance = instance_scoring(instance.dlc, score, weighted)
            dlc_instance.save()
        
        
        
        