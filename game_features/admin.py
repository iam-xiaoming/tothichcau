from django.contrib import admin
from .models import Category, GameImageReview, GameVideoReview

# Register your models here.
admin.site.register(Category)
admin.site.register(GameImageReview)
admin.site.register(GameVideoReview)