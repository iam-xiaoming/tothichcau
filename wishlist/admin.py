from django.contrib import admin
from .models import Wishlist
from django.contrib.admin import SimpleListFilter

# Register your models here.
class WishlistTypeFilter(SimpleListFilter):
    title = 'type'
    parameter_name = 'type'

    def lookups(self, request, model_admin):
        return (
            ('game', 'Base Game'),
            ('dlc', 'Downloadable Content'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'game':
            return queryset.filter(game__isnull=False)
        elif self.value() == 'dlc':
            return queryset.filter(dlc__isnull=False)


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    autocomplete_fields = ('game', 'dlc', 'user',)
    list_display = ('pk', 'user', 'object_name', 'type_name', 'created_at')
    list_filter = (WishlistTypeFilter,)
    
    def object_name(self, obj):
        if obj.game:
            return obj.game.name
        return obj.dlc.name
    
    def type_name(self, obj):
        if obj.game:
            return 'Base Game'
        return 'Downloadable Content'
    
    object_name.short_description = 'game'
    type_name.short_description = 'type'
    