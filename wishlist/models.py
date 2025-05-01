from django.db import models
from games.models import Game, DLC
from users.models import MyUser
from django.core.exceptions import ValidationError

# Create your models here.
class Wishlist(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True, related_name='wishlist')
    dlc = models.ForeignKey(DLC, on_delete=models.CASCADE, related_name='wishlist', null=True, blank=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='wishlist', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.game:
            return self.game.name
        return self.dlc.name
    
    
    def clean(self):
        if not (self.game or self.dlc):
            raise ValidationError('Game or DlC must provided.')
        return super().clean()