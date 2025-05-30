from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import PostLike, PostCommentLike, PostComment
from notification.models import Notification
from django.db.models import F

# post like
@receiver(post_save, sender=PostLike)
def save_post_like(sender, instance, created, **kwargs):
    if created:
        instance.post.count_like += 1
        instance.post.save()
        
        
@receiver(pre_delete, sender=PostLike)
def decrease_post_like_count(sender, instance, **kwargs):
    post = instance.post

    # Dùng F để giảm count_like, nhưng không để giá trị âm
    if post.count_like > 0:
        post.count_like = F('count_like') - 1
        post.save(update_fields=['count_like'])
    

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
def decrease_comment_like_count(sender, instance, **kwargs):
    comment = instance.comment
    
    # Dùng F để giảm count_like, nhưng không để giá trị âm
    if comment.count_like > 0:
        comment.count_like = F('count_like') - 1
        comment.save(update_fields=['count_like'])
    

# notification
@receiver(post_save, sender=PostComment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        sender_user = instance.user
        parent = instance.parent
        
        if parent:
            recipient = parent.user
            if recipient != sender_user:
                Notification.objects.create(
                    recipient=recipient,
                    sender=sender_user,
                    post=post,
                    comment=instance,
                    message=f"{sender_user.username} has replied on your comment."
                )
            return
        
        recipient = post.user
        if recipient != sender_user:
            Notification.objects.create(
                recipient=recipient,
                sender=sender_user,
                post=post,
                message=f"{sender_user.username} has commented on your post."
            )
            
            
@receiver(post_save, sender=PostLike)
def create_like_notification(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        recipient = post.user
        sender_user = instance.user
        
        if recipient != sender_user:
            Notification.objects.create(
                recipient=recipient,
                sender=sender_user,
                post=post,
                message=f"{sender_user.username} has liked your post."
            )