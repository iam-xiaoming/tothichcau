from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='categories/img/')
    slug = models.SlugField(unique=True, blank=True, editable=False)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


def validate_video_size(value):
    max_size = 50 * 1024 * 1024
    if value.size > max_size:
        raise ValidationError(f"Video is too large in order to upload (total size): {value.size / (1024 * 1024):.2f})/{(max_size / 1024 * 1024):.2f}MB")
    
    

def get_image_upload_to(instance, filename):
    if instance.dlc:
        return f'game_image_reviews/{instance.dlc.name}/dlc_images/{filename}'
    return f'game_image_reviews/{instance.game.name}/images/{filename}'

def get_video_upload_to(instance, filename):
    if instance.dlc:
        return f'game_video_reviews/{instance.dlc.name}/dlc_videos/{filename}'
    return f'game_video_reviews/{instance.game.name}/videos/{filename}'

    

class GameImageReview(models.Model):
    game = models.ForeignKey('games.Game', on_delete=models.CASCADE, related_name='game_image_reviews', null=True, blank=True)
    dlc = models.ForeignKey('games.DLC', on_delete=models.CASCADE, related_name='dlc_image_reviews', null=True, blank=True)
    
    image = models.ImageField(upload_to=get_image_upload_to)
    
    def __str__(self):
        if self.game:
            return f'Video Reviews of {self.game.name}'
        return f'Image Reviews of DLC: {self.dlc.name} for {self.dlc.game.name}'
    
    def clean(self):
        super().clean()
        if not (self.game or self.dlc):
            raise ValidationError('Game or DLC must be not none.')
    
    
class GameVideoReview(models.Model):
    game = models.ForeignKey('games.Game', on_delete=models.CASCADE, related_name='game_video_reviews', null=True, blank=True)
    dlc = models.ForeignKey('games.DLC', on_delete=models.CASCADE, related_name='dlc_video_reviews', null=True, blank=True)
    video = models.FileField(upload_to=get_video_upload_to)
    
    def __str__(self):
        if self.game:
            return f'Video Reviews of {self.game.name}'
        return f'Video Reviews of {self.dlc.name}'
    
    def clean(self):
        super().clean()
        if not (self.game or self.dlc):
            raise ValidationError('Game or DLC must be not none.')
        
        
class GameStory(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='game_story/')
    url = models.URLField()
    
    def __str__(self):
        return self.title
    
    
class FeatureHighlight(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='feature_highlight/img/')
    video = models.FileField(upload_to='feature_highlight/video/')
    
    def __str__(self):
        return self.title