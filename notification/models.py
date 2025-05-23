from django.db import models
from users.models import MyUser
from blog.models import Post, PostComment

# Create your models here.
class Notification(models.Model):
    recipient = models.ForeignKey(MyUser, related_name='notifications', on_delete=models.CASCADE) # who receive notification
    sender = models.ForeignKey(MyUser, related_name='sent_notifications', on_delete=models.CASCADE) # who send
    post = models.ForeignKey(Post, on_delete=models.CASCADE) # on post
    comment = models.ForeignKey(PostComment, on_delete=models.CASCADE, null=True, blank=True) # which comment
    message = models.CharField(max_length=255) # message
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} commented on {self.post} (to {self.recipient})"