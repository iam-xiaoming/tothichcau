from django.contrib import admin
from .models import Game, Rating, DLC
from .forms import GameAdminForm, DLCAdminForm
from game_features.admin import GameImageReviewInline, GameVideoReviewInline
from keys.admin import KeyInline
from wishlist.admin import WishlistTypeFilter

# Register your models here
@admin.register(Game)  
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'publisher', 'price', 'discount', 'quantity', 'number_of_buy', 'category_list', 'average_score', 'rating', 'release_date',)
    list_filter = ('price', 'categories', 'rating', 'release_date',)
    search_fields = ('name', 'publisher', 'categories__name', 'rating',)
    ordering = ('-release_date',)
    form = GameAdminForm
    inlines = [GameImageReviewInline, GameVideoReviewInline, KeyInline]
    
    def category_list(self, obj):
        return ', '.join([category.name for category in obj.categories.all()])
    category_list.short_description = 'Categories'
    
    
@admin.register(DLC)  
class DLCAdmin(admin.ModelAdmin):
    autocomplete_fields = ['game']
    list_display = ('id', 'name', 'game__name', 'publisher', 'price', 'discount', 'quantity', 'category_list', 'average_score', 'rating', 'release_date',)
    list_filter = ('price', 'game__categories', 'rating', 'release_date',)
    search_fields = ('name', 'publisher', 'game__categories__name', 'rating',)
    ordering = ('-release_date',)
    form = DLCAdminForm
    inlines = [GameImageReviewInline, GameVideoReviewInline, KeyInline]
    
    def category_list(self, obj):
        return ', '.join([category.name for category in obj.game.categories.all()])
    category_list.short_description = 'Categories'
    

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_object_name', 'get_type', 'comment__title', 'score', 'weighted',)
    search_fields = ('id', 'user__name', 'game', 'dlc', 'comment__title',)
    list_filter = ('score', WishlistTypeFilter, 'comment__title', 'comment__created_at')
    
    def get_object_name(self, obj):
        if obj.game:
            return obj.game.name
        return obj.dlc.name
    
    def get_type(self, obj):
        if obj.game:
            return 'Base Game'
        return 'Downloadable Content'
    
    get_object_name.short_description = 'game'
    get_type.short_description = 'type'
    
