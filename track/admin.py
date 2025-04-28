from django.contrib import admin
from .models import UserInteraction

# Register your models here.

@admin.register(UserInteraction)
class UserInteractionAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'item_id', 'timestamp', 'event_type')
    list_filter = ('event_type',)
    search_fields = ('user_id', 'item_id')