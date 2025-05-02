from django.contrib import admin
from .models import Notification

# Register your models here.
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'sender', 'post', 'is_read', 'timestamp',)
    search_fields = ('recipient', 'sender',)