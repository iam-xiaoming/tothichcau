from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


def validate_video_size(value):
    max_size = 100 * 1024 * 1024
    if value.size > max_size:
        raise ValidationError(f"Video is too large in order to upload (total size): {value.size / (1024 * 1024):.2f})/{(max_size / 1024 * 1024):.2f}MB")
    
    

def get_image_upload_to(instance, filename):
    return f'game_image_reviews/{instance.game.name}/images/{filename}'

def get_video_upload_to(instance, filename):
    return f'game_video_reviews/{instance.game.name}/videos/{filename}' 
    

class GameImageReview(models.Model):
    game = models.ForeignKey('games.Game', on_delete=models.CASCADE, related_name='game_image_reviews')
    
    image = models.ImageField(upload_to=get_image_upload_to)
    
    def __str__(self):
        return f'Image Reviews of {self.game.name}'
    
    
class GameVideoReview(models.Model):
    game = models.ForeignKey('games.Game', on_delete=models.CASCADE, related_name='game_video_reviews')
    video = models.FileField(upload_to=get_video_upload_to)
    
    def __str__(self):
        return f'Video Reviews of {self.game.name}'