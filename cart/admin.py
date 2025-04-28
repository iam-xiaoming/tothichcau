from django.contrib import admin
from .models import Order, Transaction
from django.contrib import admin

# Register your models here.
admin.site.register(Order)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'get_user_key_game', 'status', 'total_amount', 'created_at')
    
    def get_user_key_game(self, obj):
        return obj.key
    
    get_user_key_game.short_description = 'key'