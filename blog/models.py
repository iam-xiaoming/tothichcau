from django.db import models
from users.models import MyUser
from game_features.models import Category

# Create your models here.
# class Post(models.Model):
#     user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='posts')
#     categories = models.ManyToManyField(Category, related_name='posts')
#     title = models.CharField(max_length=128)
#     excerpt = models.TextField(max_length=255)
#     content = 