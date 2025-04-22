from django.db import models
from users.models import MyUser
from games.models import Game, Key

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='orders')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Order #{self.id} - {self.game.name}"
    
    
class Transaction(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ]
    
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='transactions')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='transactions')
    key = models.ForeignKey(Key, on_delete=models.CASCADE, related_name='transactions')
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='failed')
    created_at = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=255)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    customer_email = models.EmailField()
    brand = models.CharField(max_length=255)
    last4 = models.PositiveIntegerField()
    phone = models.CharField(max_length=255, blank=True, null=True)
    exp_month = models.PositiveIntegerField()
    exp_year = models.PositiveIntegerField()

    def __str__(self):
        return f"Transaction #{self.id} - {self.status.capitalize()}"