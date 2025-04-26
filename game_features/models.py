from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


def validate_video_size(value):
    max_size = 50 * 1024 * 1024
    if value.size > max_size:
        raise ValidationError(f"Video is too large in order to upload (total size): {value.size / (1024 * 1024):.2f})/{max_size}MB")

class GameImageReview(models.Model):
    game = models.ForeignKey('games.Game', on_delete=models.CASCADE, related_name='game_image_reviews')
    
    image = models.ImageField(upload_to=f'game_image_reviews/{game.name}/')
    
    def __str__(self):
        return f'Image Reviews of {self.game.name}'
    
    
class GameVideoReview(models.Model):
    game = models.ForeignKey('games.Game', on_delete=models.CASCADE, related_name='game_video_reviews')
    video = models.FileField(upload_to=f'videos/{game.name}/', validators=[validate_video_size])
    
    def __str__(self):
        return f'Video Reviews of {self.game.name}'