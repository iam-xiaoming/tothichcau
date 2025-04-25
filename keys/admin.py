from django.contrib import admin
from .models import Key

# Register your models here.
@admin.register(Key)
class KeyAdmin(admin.ModelAdmin):
    autocomplete_fields = ['game']
    list_display = ('key', 'game', 'status',)
    list_filter = ('status', 'game__name')
    search_fields = ('key', 'game__name')
