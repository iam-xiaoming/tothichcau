from django.db import models
from django.utils import timezone
from users.models import MyUser

# Create your models here.

# Game:
# - id: PK(stripe)
# - price_id: string (stripe) (update)
# - title: string
# - desc: text
# - price: decimal
# - discount: decimal (optional)
# - publisher: string
# - release_date: datetime
# - img_url: string
# - category: string
# - quantity: interger

class Game(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    price_id = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    publisher = models.CharField(max_length=255)
    release_date = models.DateTimeField(default=timezone.now)
    image_url = models.URLField()
    category = models.CharField(max_length=255)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
    
    
# Key:
# - id: PK
# - game_id: FK (update)
# - game_price_id: string  (stripe product price id)
# - key: string, unique
# - status: Enum [available, sold]

class Key(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('sold', 'Sold'),
    )
    
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='keys')
    game_price_id = models.CharField(max_length=255, unique=True)
    key = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    
    def __str__(self):
        return f"{self.key} ({self.status})"
    

# User_game:
# - id: PF
# - user_id: FK
# - game_id: FK

class UserGame(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='owned_games')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='owned_by_users')
    
    
    def __str__(self):
        return f"{self.user.email} owns {self.game.title}"
