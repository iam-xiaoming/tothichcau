from django.contrib import admin
from .models import Game
from .forms import GameAdminForm
from game_features.models import GameImageReview, GameVideoReview

# Register your models here
class GameImageReviewInline(admin.StackedInline):
    model = GameImageReview
    extra = 1

    fields = ['image']
    
    def get_max_num(self, request, obj, **kwargs):
        return 5
    

class GameVideoReviewInline(admin.StackedInline):
    model = GameVideoReview
    extra = 1
    
    fields = ['video']
    
    def get_max_num(self, request, obj, **kwargs):
        return 2
    
@admin.register(Game)  
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'publisher', 'price', 'discount', 'quantity', 'category_list', 'release_date')
    list_filter = ('publisher', 'categories', 'release_date')
    search_fields = ('name', 'publisher', 'categories__name')
    ordering = ('-release_date',)
    form = GameAdminForm
    inlines = [GameImageReviewInline, GameVideoReviewInline]
    
    def category_list(self, obj):
        return ', '.join([category.name for category in obj.categories.all()])
    category_list.short_description = 'Categories'
    
    
