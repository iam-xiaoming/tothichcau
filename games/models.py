from django.db import models
from django.utils import timezone
import stripe
from django.conf import settings
from decimal import Decimal
from django.core.validators import MaxValueValidator, MinValueValidator
from game_features.models import Category

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your models here.
class Game(models.Model):
    # stripe id
    stripe_product_id = models.CharField(max_length=100, unique=True, editable=False)
    stripe_price_id = models.CharField(max_length=100, unique=True, editable=False)
    
    
    quantity = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.PositiveIntegerField(default=0, validators=[
        MinValueValidator(0),
        MaxValueValidator(100)
    ])
    publisher = models.CharField(max_length=255)
    release_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='game_images')
    categories = models.ManyToManyField(Category, related_name='games')


    def __str__(self):
        return self.name
            
    @property
    def discounted_price(self):
        return self.price * (Decimal(100 - self.discount) / 100)
    
    
class DLC(models.Model):
    pass