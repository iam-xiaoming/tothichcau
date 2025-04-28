from django.contrib import admin
from .models import Game, Rating
from .forms import GameAdminForm
from game_features.admin import GameImageReviewInline, GameVideoReviewInline
from keys.admin import KeyInline

# Register your models here
@admin.register(Game)  
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'publisher', 'price', 'discount', 'quantity', 'category_list', 'average_score', 'rating', 'release_date')
    list_filter = ('price', 'categories', 'rating', 'release_date',)
    search_fields = ('name', 'publisher', 'categories__name', 'rating')
    ordering = ('-release_date',)
    form = GameAdminForm
    inlines = [GameImageReviewInline, GameVideoReviewInline, KeyInline]
    
    def category_list(self, obj):
        return ', '.join([category.name for category in obj.categories.all()])
    category_list.short_description = 'Categories'
    

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'game', 'comment__title', 'score', 'weighted',)
    search_fields = ('id', 'user', 'game', 'comment__title',)
    list_filter = ('score', 'comment__title', 'comment__created_at')
    
