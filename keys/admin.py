from django.contrib import admin
from .models import Key

# Register your models here.
@admin.register(Key)
class KeyAdmin(admin.ModelAdmin):
    autocomplete_fields = ('game', 'dlc',)
    list_display = ('id', 'key', 'get_object_name', 'get_type', 'status',)
    list_filter = ('status',)
    search_fields = ('key', 'game__name', 'dlc_name')
    
    def get_object_name(self, obj):
        if obj.game:
            return obj.game.name
        return obj.dlc.name
    
    def get_type(self, obj):
        if obj.game:
            return 'Base Game'
        return 'Downloadable Content'
    
    get_object_name.short_description = 'game'
    get_type.short_description = 'type'
    
    


class KeyInline(admin.StackedInline):
    model = Key
    extra = 0
    fields = ['key', 'status']