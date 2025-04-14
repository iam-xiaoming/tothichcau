import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Game

@receiver(post_delete, sender=Game)
def delete_game_image(sender, instance, **kwargs):
    if instance.image and os.path.isfile(instance.image.path):
        print('Signal: deleting image:', instance.image.path)
        os.remove(instance.image.path)
