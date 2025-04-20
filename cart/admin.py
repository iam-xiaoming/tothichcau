from django.contrib import admin
from .models import Order, Transaction
from django.contrib import admin
from games.models import Key

# Register your models here.
admin.site.register(Order)
# admin.site.register(Transaction)
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'get_user_key_game', 'status', 'total_amount', 'created_at')
    
    def get_user_key_game(self, obj):
        return Key.objects.get(game=obj.game)
    
    get_user_key_game.short_description = 'key'