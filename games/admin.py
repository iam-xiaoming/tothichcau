from django.contrib import admin
from .models import Game
from .forms import GameAdminForm
from game_features.models import GameImageReview, GameVideoReview
from game_features.admin import GameImageReviewInline, GameVideoReviewInline
from keys.admin import KeyInline

# Register your models here
@admin.register(Game)  
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'publisher', 'price', 'discount', 'quantity', 'category_list', 'release_date')
    list_filter = ('publisher', 'categories', 'release_date')
    search_fields = ('name', 'publisher', 'categories__name')
    ordering = ('-release_date',)
    form = GameAdminForm
    inlines = [GameImageReviewInline, GameVideoReviewInline, KeyInline]
    
    def category_list(self, obj):
        return ', '.join([category.name for category in obj.categories.all()])
    category_list.short_description = 'Categories'
    
    
