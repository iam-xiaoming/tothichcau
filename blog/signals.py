from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import PostLike

@receiver(post_save, sender=PostLike)
def save_post_like(sender, instance, created, **kwargs):
    if created:
        instance.post.count_like += 1
        instance.post.save()
        
        
@receiver(pre_delete, sender=PostLike)
def save_post_like(sender, instance, **kwargs):
    instance.post.count_like -= 1
    instance.post.save()