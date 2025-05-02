from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import PostLike, PostCommentLike, PostComment

# post like
@receiver(post_save, sender=PostLike)
def save_post_like(sender, instance, created, **kwargs):
    if created:
        instance.post.count_like += 1
        instance.post.save()
        
        
@receiver(pre_delete, sender=PostLike)
def save_post_like(sender, instance, **kwargs):
    instance.post.count_like -= 1
    instance.post.save()
    

# post comment count
@receiver(post_save, sender=PostComment)
def count_post_comment(sender, instance, created, **kwargs):
    if created:
        instance.post.count_comment += 1
        instance.post.save()


# comment like  
@receiver(post_save, sender=PostCommentLike)
def save_post_like(sender, instance, created, **kwargs):
    if created:
        instance.comment.count_like += 1
        instance.comment.save()
        
        
@receiver(pre_delete, sender=PostCommentLike)
def save_post_like(sender, instance, **kwargs):
    instance.comment.count_like -= 1
    instance.comment.save()