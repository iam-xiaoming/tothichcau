from django.contrib import admin
from .models import Tag, Post, PostLike, PostComment, PostCommentLike
from .forms import PostAdminForm

# Register your models here.
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'frequency',)
    search_fields = ('name',)
    

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'count_view', 'count_comment', 'count_like', 'tags_list', 'category', 'created_at')
    list_filter = ('user__username', 'tags', 'category')
    search_fields = ('user__username', 'user__email', 'title')
    form = PostAdminForm
    
    def tags_list(self, obj):
        return ', '.join([str(tag) for tag in obj.tags.all()])

    tags_list.short_description = 'tags'
    
    
@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'user',)
    search_fields = ('post', 'user',)
    

@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'count_like', 'created_at',)
    search_fields = ('user', 'post',)
    
    
@admin.register(PostCommentLike)
class PostCommentLikeAdmin(admin.ModelAdmin):
    list_display = ('comment', 'user',)
    search_fields = ('user',)