from django.db import models

# Create your models here.
# custom hero page
class GameHero(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='game_hero_images')
    
    def __str__(self):
        return self.name