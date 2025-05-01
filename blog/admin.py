from django.contrib import admin
from .models import Tag, Post
from .forms import PostAdminForm

# Register your models here.
admin.site.register(Tag)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'tags_list', 'category', 'created_at')
    list_filter = ('user__username', 'tags', 'category')
    search_fields = ('user__username', 'user__email', 'title')
    form = PostAdminForm
    
    def tags_list(self, obj):
        return ', '.join([str(tag) for tag in obj.tags.all()])

    tags_list.short_description = 'tags'