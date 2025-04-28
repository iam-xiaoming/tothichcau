from django.db import models
from games.models import Game

# Create your models here.
class Key(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('sold', 'Sold')
    )
    
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='keys')
    key = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    
    def __str__(self):
        return self.key