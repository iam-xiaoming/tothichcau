from django.db import models

# Create your models here.
class Stream(models.Model):
    name = models.CharField(max_length=100)
    stream_id = models.CharField(max_length=100, unique=True)
    rtmp_url = models.CharField(max_length=255)
    stream_key = models.CharField(max_length=100)
    playback_url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    
class ChatMessage(models.Model):
    stream_id = models.CharField(max_length=100)
    username = models.CharField(max_length=150)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)