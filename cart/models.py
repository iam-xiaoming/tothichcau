from django.db import models
from users.models import MyUser
from games.models import Game

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='users')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='games')
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    
    def __str__(self):
        return f"Order #{self.id} - {self.game.title} x{self.quantity} ({self.status})"
    
    
class Transaction(models.Model):
    STATUS_CHOICES = [
        ('complete', 'Complete'),
        ('failed', 'Failed')
    ]
    
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='transactions')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='transactions')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='failed')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction #{self.id} - {self.status.capitalize()}"