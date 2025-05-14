from django.db import models
from django.core.files.storage import default_storage

# Create your models here.
class GameHero(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='game_hero_images')
    
    def __str__(self):
        return self.name