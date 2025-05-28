from django.contrib import admin
from .models import Stream, ChatMessage

# Register your models here.
@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    list_display = ('pk', 'stream_id', 'name', 'stream_key', 'created_at')
    search_fields = ('stream_id', 'stream_key',)
    
@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('stream_id', 'username', 'message',)