from django.contrib import admin
from .models import Game, Key, UserGame

# Register your models here.
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'price', 'discount', 'category', 'release_date', 'quantity')
    list_filter = ('publisher', 'category', 'release_date')
    search_fields = ('title', 'publisher', 'category')
    ordering = ('-release_date',)
    
    
@admin.register(Key)
class KeyAdmin(admin.ModelAdmin):
    list_display = ('key', 'game', 'status', 'game_price_id')
    list_filter = ('status', 'game__title')
    search_fields = ('key', 'game__title', 'game_price_id')


@admin.register(UserGame)
class UserGameAdmin(admin.ModelAdmin):
    list_display = ('user', 'game')
    list_filter = ('game',)
    search_fields = ('user__email', 'user__username', 'game__title')
    autocomplete_fields = ('user', 'game')  # Makes large foreign key dropdowns faster
