from django.db import models
from django.utils import timezone
import stripe
from django.conf import settings
from decimal import Decimal
from django.core.validators import MaxValueValidator, MinValueValidator
from game_features.models import Category
from users.models import Comment
from django.core.exceptions import ValidationError

stripe.api_key = settings.STRIPE_SECRET_KEY

class BaseGame(models.Model):
    RATING_CHOICES = [
        ('overwhelmingly positive', 'Overwhelmingly Positive'),
        ('very positive', 'Very Positive'),
        ('mostly positive', 'Mostly Positive'),
        ('mixed', 'Mixed'),
        ('mostly negative', 'Mostly Negative'),
        ('overwhelmingly negative', 'Overwhelmingly Negative'),
        ('no review', 'No Review')
    ]
    
    GAME_TYPES = [
        ('base', 'Base Game'),
        ('dlc', 'Downloadable Content')
    ]
    
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
    average_score = models.DecimalField(null=True, blank=True, editable=False, max_digits=3, decimal_places=1)
    rating = models.CharField(max_length=255, default='no review', choices=RATING_CHOICES)
    
    publisher = models.CharField(max_length=255)
    categories = models.ManyToManyField(Category, related_name='%(class)s_set')
    status = models.CharField(default='base', choices=GAME_TYPES)
    
    
    class Meta:
        abstract = True
    
    def __str__(self):
        return self.name
            
    @property
    def discounted_price(self):
        return self.price * (Decimal(100 - self.discount) / 100)



class Game(BaseGame):
    pass
    

class DLC(BaseGame):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='dlc')
    
    def save(self, *args, **kwargs):
        if self.game:
            self.publisher = self.game.publisher
            self.status = 'dlc'

        super().save(*args, **kwargs)

        if self.game:
            self.categories.set(self.game.categories.all())



class Rating(models.Model):
    
    user = models.ForeignKey('users.MyUser', on_delete=models.CASCADE, related_name='user_rating')
    
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game_rating', blank=True, null=True, editable=False)
    dlc = models.ForeignKey(DLC, on_delete=models.CASCADE, related_name='dlc_rating', blank=True, null=True, editable=False)
    
    comment = models.OneToOneField(Comment, on_delete=models.CASCADE, related_name='comment_rating')
    
    
    score = models.PositiveSmallIntegerField(default=10, validators=[
        MinValueValidator(0),
        MaxValueValidator(10)
    ])
    weighted = models.PositiveSmallIntegerField(default=1, validators=[
        MinValueValidator(1)
    ])
    
    def __str__(self):
        return f'{self.score}'