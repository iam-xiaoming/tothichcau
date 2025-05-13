from .models import GameStory, FeatureHighlight
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

@receiver(post_delete, sender=GameStory)
def delete_game_story(sender, instance, **kwargs):
    if instance.image:                   
        instance.image.delete(save=False)
        
        
@receiver(post_delete, sender=FeatureHighlight)
def delete_game_story(sender, instance, **kwargs):
    if instance.image:           
        instance.image.delete(save=False)
    if instance.video:
        instance.video.delete(save=False)