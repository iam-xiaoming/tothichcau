from django.contrib import admin
from .models import Category, GameImageReview, GameVideoReview, GameStory, FeatureHighlight

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name',)
    

admin.site.register(GameImageReview)
admin.site.register(GameVideoReview)

class GameImageReviewInline(admin.StackedInline):
    model = GameImageReview
    extra = 0

    fields = ['image']
    
    def get_max_num(self, request, obj, **kwargs):
        return 5
    

class GameVideoReviewInline(admin.StackedInline):
    model = GameVideoReview
    extra = 0
    
    fields = ['video']
    
    def get_max_num(self, request, obj, **kwargs):
        return 2
    
    
@admin.register(GameStory)
class GameStoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    
    def has_add_permission(self, request):
        max_objects = 3
        if GameStory.objects.count() >= max_objects:
            return False
        return super().has_add_permission(request)
    

@admin.register(FeatureHighlight)
class FeatureHighlightAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    
    def has_add_permission(self, request):
        max_objects = 4
        if GameStory.objects.count() >= max_objects:
            return False
        return super().has_add_permission(request)