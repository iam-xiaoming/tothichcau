from django.contrib import admin
from .models import Tag, Post
from .forms import PostAdminForm

# Register your models here.
admin.site.register(Tag)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'categories_list', 'tags_list', 'created_at')
    list_filter = ('user__username', 'tags', 'categories')
    search_fields = ('user__username', 'user__email', 'title')
    form = PostAdminForm
    
    def categories_list(self, obj):
        return ', '.join([str(category) for category in obj.categories.all()])
    
    def tags_list(self, obj):
        return ', '.join([str(tag) for tag in obj.tags.all()])
    
    categories_list.short_description = 'categories'
    tags_list.short_description = 'tags'