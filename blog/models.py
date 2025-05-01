from django.db import models
from users.models import MyUser
from game_features.models import Category

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=128, unique=True)
    
    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='posts')
    title = models.CharField(max_length=128)
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now=True)
    count_view = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.title