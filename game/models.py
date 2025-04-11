from django.db import models

# Create your models here.

class Game(models.Model):
    id = models.AutoField(primary_key=True)
    price_id = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    publisher = models.CharField(max_length=255)
    release_date = models.DateField()
    image_url = models.URLField()
    category = models.CharField(max_length=255)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    