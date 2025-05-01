from django.contrib import admin
from .models import Category, GameImageReview, GameVideoReview

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