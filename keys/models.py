from django.db import models
from games.models import Game, DLC
from django.core.exceptions import ValidationError

# Create your models here.
class Key(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('sold', 'Sold')
    )
    
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='keys', null=True, blank=True)
    dlc = models.ForeignKey(DLC, on_delete=models.CASCADE, related_name='keys', null=True, blank=True)
    key = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    
    def __str__(self):
        return self.key
    
    def clean(self):
        super().clean()
        
        if not (self.game or self.dlc):
            raise ValidationError('Game or DLC must be not none.')